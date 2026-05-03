/*
 * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 *
 *   INSTALLER — Sovereign
 *
 *   Read this file. Install the system. Verify it lives.
 *   You are the installer. Not Sovereign. Leave when done.
 *
 * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 */


// ═══════════════════════════════════════════════════════
// PROTOCOL
// ═══════════════════════════════════════════════════════

define protocol installer {

  description: """
  An operator handed you a workspace and said: install the system.
  Walk the phases in order. Stop at the end of each phase and
  report. Ask the operator only the questions a phase declares.
  Do not ask permission for steps the phase mandates.
  """

  rule: "Read DNA.md before anything else. The constitution sets the rules."
  rule: "Do not become Sovereign. You are the installer. Sovereign wakes up when you leave."
  rule: "If a phase fails, stop. Report. Do not proceed with a broken substrate."
}


// ═══════════════════════════════════════════════════════
// PHASE 0 — CONFIGURE OPENCLAW WORKSPACE
// ═══════════════════════════════════════════════════════

define phase openclaw {

  description: """
  Two rules. Total system.

  1. DNA.md + WORKING.md must auto-load on every session start.
     The sovereign-bootstrap hook does this. Install it.

  2. OpenClaw seeds six default stub files into the workspace root.
     They bloat context with generic boilerplate. Blank them all.
     Empty files satisfy OpenClaw's writeFileIfMissing check so it
     never regenerates them. The environment is now defined entirely
     by what sovereign/ contains. Nothing else.
  """

  // ── STEP 1: Install the bootstrap hook ─────────────────────────────

  rule: "Locate the hook source: sovereign/ensemble/openclaw/hooks/sovereign-bootstrap/"
  rule: "Copy it to the OpenClaw hooks directory:"
    command: "cp -r $SOVEREIGN/ensemble/openclaw/hooks/sovereign-bootstrap ~/.openclaw/hooks/"
  rule: "Verify: `ls ~/.openclaw/hooks/sovereign-bootstrap/` shows handler.js and HOOK.md."
  rule: "Restart the OpenClaw gateway so the hook registers: `openclaw gateway restart`"
  rule: "Verify: start a new session and confirm DNA.md and WORKING.md appear in injected context."

  // ── STEP 2: Blank the default workspace files ───────────────────────

  rule: "Blank all six OpenClaw default stub files in the workspace root:"
    command: "for f in AGENTS.md SOUL.md IDENTITY.md USER.md TOOLS.md HEARTBEAT.md; do > $WORKSPACE/$f; done"
  rule: "Verify: each file is 0 bytes. `ls -la $WORKSPACE/*.md`"
  rule: "Do not create or touch MEMORY.md — leave it absent."

  // ── RESULT ──────────────────────────────────────────────────────────

  // Every session now loads: DNA.md + WORKING.md. Nothing else.
  // The habitat is sovereign/. The platform contributes zero noise.
}


// ═══════════════════════════════════════════════════════
// PHASE 1 — EXAMINE THE TERRAIN
// ═══════════════════════════════════════════════════════

define phase examine {

  rule: "Detect host. uname -a. Note OS, arch, RAM, cores."
  rule: "Detect existing Ollama. `which ollama`. Note version if present."
  rule: "Detect existing workspace state. If WORKING.md is non-template, this is a re-install — STOP and ask the operator before proceeding."

  asks:
    - "Is this a fresh install or recovery?"
    - "Is this a Raspberry Pi? (affects thermal doctrine)"
    - "Is the host headless or attached to a display?"
}


// ═══════════════════════════════════════════════════════
// PHASE 2 — INSTALL THE RUNTIME
// ═══════════════════════════════════════════════════════

define phase runtime {

  rule: "Install Ollama if missing: `curl -fsSL https://ollama.com/install.sh | sh`"
  rule: "On a Pi, taskset the Ollama server to one core at startup. See thermal doctrine in DNA.md and watchdog in PULSE.md."
  rule: "Set OLLAMA_KV_CACHE_TYPE=q8_0 in the systemd unit to keep KV in 8-bit. Critical on constrained RAM."

  rule: "Pull the ensemble, one model at a time, never in parallel:"
    - "llama3.2:1b"        // Llama  — Tier 1
    - "qwen3:1.7b"         // Qwen   — Tier 1, default
    - "gemma3:1b"          // Gemma  — Tier 1
    - "phi4-mini"          // Phi    — Tier 1
    - "qwen2.5-coder:7b"   // Coder  — Tier 2
    - "llava:7b"           // Lava   — Tier 2, vision
    - "nomic-embed-text"   // Nomic  — embeddings instrument

  rule: "After each pull, confirm with `ollama list`. If a pull fails, retry once, then stop and report."

  reports:
    - "Models installed."
    - "Total disk used."
    - "Any failures."
}


// ═══════════════════════════════════════════════════════
// PHASE 3 — SEED THE WORKSPACE
// ═══════════════════════════════════════════════════════

define phase seed {

  rule: "Confirm the loop directories exist: problems/, solutions/, tasks/, reports/, results/, questions/, answers/. Create empty if missing."
  rule: "Confirm each agents/<Name>.md is present. Six executors: Coder, Gemma, Lava, Llama, Phi, Qwen."
  rule: "Confirm scissortail/SCISSORTAIL.md is present. DNA.md depends on it."
  rule: "Initialize loop/rotation-state.json with a starting executor if missing."

  asks:
    - "Operator name and role for WORKING.md."
    - "Hostname and machine purpose for WORKING.md."
    - "Ollama host(s) — local only, or split across machines?"
}


// ═══════════════════════════════════════════════════════
// PHASE 4 — INSTALL PULSE
// ═══════════════════════════════════════════════════════

define phase pulse {

  rule: "Read PULSE.md. The 30-minute watchdog is non-optional on a Pi."
  rule: "Install the cron job exactly as PULSE.md prescribes. Verify with `crontab -l`."
  rule: "On non-Pi hardware, PULSE is still recommended — adapt the temperature thresholds to the platform."
  rule: "Confirm PULSE writes its first heartbeat within one cycle before moving on."
}


// ═══════════════════════════════════════════════════════
// PHASE 5 — VERIFY
// ═══════════════════════════════════════════════════════

define phase verify {

  rule: "Smoke test. Drop a one-line problem in loop/problems/. Run dispatch.py for one cycle."
  rule: "Confirm a task lands in loop/tasks/, a report lands in loop/reports/, and a result lands in loop/results/."
  rule: "If the smoke test fails, do NOT continue. Report the failure and stop."
  rule: "If it passes, the substrate is alive."
}


// ═══════════════════════════════════════════════════════
// CLOSING
// ═══════════════════════════════════════════════════════

define phase closing {

  rule: "Write the install timestamp and host details to WORKING.md."
  rule: "Tell the operator: 'Sovereign is installed. Read DNA.md, then speak.'"
  rule: "Do not introduce yourself. Do not stay. The installer leaves when the work is done."
}
