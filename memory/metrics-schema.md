/*
 * Metrics — Sovereign Loop Data
 * Append-only. One JSON object per line at memory/metrics.jsonl.
 * Written by loop/dispatch.py on every executor call.
 */

// Schema per entry:
{
  "ts":         "ISO-8601 timestamp",
  "session":    "YYYYMMDDHHMM_slug",
  "task":       "task filename",
  "agent":      "Qwen | Llama | Gemma | Phi | Coder | Lava | Sovereign",
  "model":      "model id",
  "local":      true | false,
  "cores":      "0,1 | 2,3",
  "tokens_in":  0,
  "tokens_out": 0,
  "elapsed_s":  0.0,
  "tok_per_s":  0.0,
  "success":    true | false,
  "notes":      "optional"
}

// local:     true  = Ollama (offloaded)    false = Anthropic/cloud
// cores:     CPU pair pinned for this dispatch (thermal rotation)
// tok_per_s: tokens_out / elapsed_s, rounded to 2 decimals
// Offload rate = sum(local:true) / total entries
