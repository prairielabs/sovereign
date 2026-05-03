#!/usr/bin/env python3
"""
dispatch.py — Sovereign Loop Runner

Thermal rotation: alternates CPU core pairs between tasks.
Metrics: logs every dispatch to memory/metrics.jsonl.
Usage: python3 dispatch.py <task_file> [options]
"""

import argparse, base64, json, os, subprocess, time, requests
from datetime import datetime

# ── Config ────────────────────────────────────────────
OLLAMA_URL   = "http://localhost:11434/api/generate"

# SOVEREIGN: workspace root. Override with the SOVEREIGN env var,
# or pass --workspace at the CLI. Defaults to script's parent directory.
SOVEREIGN    = os.environ.get("SOVEREIGN", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
METRICS_FILE = f"{SOVEREIGN}/memory/metrics.jsonl"

AGENTS = {
    # Tier 1 — Pi-safe
    "Llama":    "llama3.2:1b",
    "Gemma":    "gemma3:1b",
    "Qwen":     "qwen3:1.7b",
    "Phi":      "phi4-mini",
    # Tier 2 — Pi ceiling
    "Coder":    "qwen2.5-coder:7b",
    "Lava":     "llava:7b",
    # Tier 3 — workstation GPU
    "Qwen8":    "qwen3:8b",
    "Seeker8":  "deepseek-r1:8b",
    "Coder14":  "qwen2.5-coder:14b",
    "Gemma4":   "gemma3:4b",
    # Tier 4 — full workstation
    "Qwen14":   "qwen3:14b",
    "Seeker14": "deepseek-r1:14b",
    "Phi4":     "phi4",
    "Gemma12":  "gemma3:12b",
    # Instruments
    "Nomic":    "nomic-embed-text",
}
DEFAULT_AGENT = "Qwen14"  # Tier 4 default

# ── Thermal rotation ──────────────────────────────────
CORE_PAIRS = ["0,1", "2,3"]   # A and B — alternates every task
ROTATION_STATE = f"{SOVEREIGN}/loop/rotation-state.json"

def get_ollama_pid():
    try:
        out = subprocess.check_output(["pgrep", "-f", "ollama serve"]).decode().strip()
        return int(out.split()[0])
    except Exception:
        return None

def rotate_cores():
    # Persistent rotation index — survives across process calls
    index = 0
    if os.path.exists(ROTATION_STATE):
        with open(ROTATION_STATE) as f:
            index = json.load(f).get("index", 0)
    pair = CORE_PAIRS[index % 2]
    with open(ROTATION_STATE, "w") as f:
        json.dump({"index": index + 1, "last_pair": pair}, f)
    pid = get_ollama_pid()
    if pid:
        try:
            subprocess.run(["taskset", "-cp", pair, str(pid)],
                           capture_output=True, check=False)
        except FileNotFoundError:
            # taskset is Linux-only. On macOS/Windows, skip core pinning.
            # The thermal doctrine assumes Linux on a Pi; non-Pi runs lose
            # passive heat-sinking but the loop still functions.
            pass
    return pair

# ── Metrics ───────────────────────────────────────────
def log_metric(session, task, agent, model, tokens_in, tokens_out, elapsed, success, cores, notes=""):
    entry = {
        "ts":         datetime.now().isoformat(),
        "session":    session,
        "task":       task,
        "agent":      agent,
        "model":      model,
        "local":      True,
        "cores":      cores,
        "tokens_in":  tokens_in,
        "tokens_out": tokens_out,
        "elapsed_s":  round(elapsed, 2),
        "tok_per_s":  round(tokens_out / elapsed, 2) if elapsed > 0 else 0,
        "success":    success,
        "notes":      notes,
    }
    os.makedirs(os.path.dirname(METRICS_FILE), exist_ok=True)
    with open(METRICS_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry

# ── Dispatch ──────────────────────────────────────────
def dispatch(task_file, agent_name=DEFAULT_AGENT, think=False,
             num_predict=400, num_ctx=1024, temperature=0.7,
             session=None, report_file=None, image_file=None):

    model = AGENTS.get(agent_name, AGENTS[DEFAULT_AGENT])
    task_slug = os.path.basename(task_file).replace(".md", "")
    session = session or task_slug

    with open(task_file) as f:
        prompt = f.read()

    # Thermal rotation
    cores = rotate_cores()
    print(f"[dispatch] {agent_name} ({model}) | cores {cores} | think={'on' if think else 'off'}", flush=True)

    # Vision: encode image if provided
    images = []
    if image_file and os.path.exists(image_file):
        with open(image_file, 'rb') as f:
            images = [base64.b64encode(f.read()).decode('utf-8')]

    start = time.time()
    try:
        payload = {
            "model":   model,
            "prompt":  prompt,
            "stream":  False,
            "think":   think,
            "options": {
                "temperature": temperature,
                "num_predict": num_predict,
                "num_ctx":     num_ctx,
                "num_thread":  2,
            }
        }
        if images:
            payload["images"] = images
        resp = requests.post(OLLAMA_URL, json=payload, timeout=600)
        resp.raise_for_status()
        data = resp.json()
        output    = data.get("response", "").strip()
        tokens_in  = data.get("prompt_eval_count", 0)
        tokens_out = data.get("eval_count", 0)
        elapsed    = time.time() - start
        success    = True
    except Exception as e:
        output     = f"ERROR: {e}"
        tokens_in  = tokens_out = 0
        elapsed    = time.time() - start
        success    = False

    # Write report
    if report_file is None:
        report_file = task_file.replace("/tasks/", "/reports/").replace("_task", "_report")
    os.makedirs(os.path.dirname(report_file), exist_ok=True)
    with open(report_file, "w") as f:
        f.write(f"# Report — {task_slug}\n")
        f.write(f"Agent: {agent_name} | Model: {model} | Cores: {cores} | ")
        f.write(f"Elapsed: {elapsed:.1f}s | Tokens: {tokens_in}in/{tokens_out}out\n\n")
        f.write(output + "\n")

    metric = log_metric(session, task_slug, agent_name, model,
                        tokens_in, tokens_out, elapsed, success, cores)

    print(f"[dispatch] done — {tokens_in}in/{tokens_out}out | {elapsed:.1f}s | {metric['tok_per_s']} tok/s", flush=True)
    return {"output": output, "report": report_file, "metric": metric, "success": success}


# ── CLI ───────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sovereign dispatch runner")
    parser.add_argument("task_file", help="Path to task .md file")
    parser.add_argument("--agent",       default=DEFAULT_AGENT, choices=list(AGENTS.keys()))
    parser.add_argument("--think",       action="store_true")
    parser.add_argument("--num_predict", type=int, default=400)
    parser.add_argument("--num_ctx",     type=int, default=1024)
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--session",     default=None)
    parser.add_argument("--report",      default=None)
    parser.add_argument("--image",       default=None, help="Path to image file for vision models")
    args = parser.parse_args()

    result = dispatch(
        task_file   = args.task_file,
        agent_name  = args.agent,
        think       = args.think,
        num_predict = args.num_predict,
        num_ctx     = args.num_ctx,
        temperature = args.temperature,
        session     = args.session,
        report_file = args.report,
        image_file  = args.image,
    )
    print(f"[dispatch] report → {result['report']}")
