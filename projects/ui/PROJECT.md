/*
 * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 *
 *   PROJECT — Sovereign UI
 *
 *   Build a user interface for Sovereign.
 *   Status: planning
 *   Started: 2026-04-30
 *
 * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 */

// ═══════════════════════════════════════════════════════
// CONTEXT
// ═══════════════════════════════════════════════════════

define context ui {

  description: """
  Sovereign is a conductor/executor system operating via .md files and a task loop.
  The UI surfaces what the system is doing — task dispatch, executor activity,
  loop state, model ensemble status — without interfering with the protocol.

  The UI is an observer. It does not change the loop.
  """
}

// ═══════════════════════════════════════════════════════
// OPEN QUESTIONS
// ═══════════════════════════════════════════════════════

define questions ui {

  // To be decided with Cal:
  q: "What is the primary surface? Web, TUI, desktop app?"
  q: "What does the user need to see? Loop state, task queue, executor activity, model status?"
  q: "Read-only dashboard or interactive control (dispatch tasks, pause loop, swap executors)?"
  q: "Stack? React, Svelte, terminal curses, something else?"
  q: "Does this ship as part of the npm package or standalone?"
}

// ═══════════════════════════════════════════════════════
// NOTES
// ═══════════════════════════════════════════════════════

define notes ui {

  2026-04-30 — Project created. Cal wants to start building. Design session pending.
}
