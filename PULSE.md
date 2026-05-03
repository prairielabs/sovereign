/*
 * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 *
 *   PULSE — Sovereign
 *   Fires every 30 minutes. Checks. Recovers. Never silent.
 *
 * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 */


// ═══════════════════════════════════════════════════════
// PURPOSE
// ═══════════════════════════════════════════════════════

// An overnight orchestrator can fail silently. Tasks stall. Runners
// orphan. Outputs vanish. PULSE exists so silence is impossible.
//
// Every 30 minutes: check, recover, keep moving.
// The operator should be able to leave and come back to work done.


// ═══════════════════════════════════════════════════════
// CHECKS — the wheelhouse of discovered problems
// ═══════════════════════════════════════════════════════

define checks pulse {

  check: "Are expected output files present? If not, task failed silently."
  check: "Is a recovery subagent already running? Don't double-spawn."
  check: "Are any tasks stalled — subagent running but no new outputs in 30min?"
  check: "Did the last fix-run log show failures? Spawn recovery."
  check: "Is Ollama up? If not, wait for next pulse — do not spawn codegen tasks."
  check: "Was a heavy reasoning model used for code generation? It times out. Route to Coder."
  check: "Are completed outputs valid file sizes (>1KB)? Zero-byte = silent fail."
  check: "Is the CPU temp in range? See thermal doctrine in DNA.md. Throttle ≥85°C, hard ceiling 90°C."
  check: "Are there orphaned Ollama runners holding RAM? Reap them."
}


// ═══════════════════════════════════════════════════════
// RECOVERY PROTOCOL
// ═══════════════════════════════════════════════════════

define recovery pulse {

  rule: "If outputs are missing AND no subagent is running → spawn recovery task loop."
  rule: "Recovery task loop uses FULL ENSEMBLE. Not just Coder."
  rule: "One task at a time. Discrete. Task N+1 emerges from report of task N."
  rule: "Prompt refinement → Qwen. Code generation → Coder. Debug failures → Phi. Extract code → Llama."
  rule: "taskset -c 0,1 for Coder (Tier 2). Tier 1 models run free."
  rule: "Fix loop: if script fails, Phi reads the error, Coder patches, re-execute. Not silent."
  rule: "Log every action with a timestamp. Append, never overwrite."
  rule: "When recovery completes, write final status to the status block below."
}


// ═══════════════════════════════════════════════════════
// CRON
// ═══════════════════════════════════════════════════════

define cron pulse {

  schedule: "*/30 * * * *"   // every 30 minutes

  rule: "Install via INSTALLER.md, phase pulse. Verify with `crontab -l`."
  rule: "On a Pi, taskset the cron-spawned check process to a single core to keep it cheap."
  rule: "On non-Pi hardware, drop the temperature check or adapt to platform sensors."
}


// ═══════════════════════════════════════════════════════
// STATUS — written by the pulse agent each run
// ═══════════════════════════════════════════════════════

define status pulse {
  last_pulse:    "never"
  pending_count: 0
  action_taken:  "fresh install — no pulses recorded yet"
}
