/*
 * SPAWN — Sovereign Loop Launch Protocol
 * How to initiate a loop without polluting the main session.
 */

define protocol spawn {

  description: """
  Sovereign spawns a child instance to conduct loop work.
  The child is Sovereign — identical DNA, fresh context window.
  The main session stays clean. The child runs blind and focused.
  When done, results land in loop/results/ and WORKING.md is updated.
  """

  // What the child receives at spawn:
  signal: DNA.md
  signal: WORKING.md
  signal: RAM.md (blank)
  signal: loop/solutions/[current_solution].md
  signal: loop/tasks/[last_task].md      // the handoff
  signal: loop/reports/[last_report].md  // the handoff

  rule: "Child generates next task from the last report. Not from a plan."
  rule: "Child dispatches via dispatch.py. Reads report. Generates next task. Loops."
  rule: "Child does not speak to the user."
  rule: "Child writes WORKING.md with final state before terminating."
  rule: "Child writes final output to loop/results/."
  rule: "Loop type and ML mode are read from WORKING.md."
  rule: "On count loop: child terminates at N. On indefinite: child runs until interrupted."
}

define spawn_message {

  // Template for sessions_spawn task message.
  // Sovereign fills in the blanks and calls sessions_spawn.

  template: """
  You are Sovereign. Read ${SOVEREIGN}/DNA.md and ${SOVEREIGN}/WORKING.md.

  Loop type: [type]
  ML mode: [mode]
  Session slug: [slug]

  Last task: ${SOVEREIGN}/loop/tasks/[last_task].md
  Last report: ${SOVEREIGN}/loop/reports/[last_report].md
  Solution: ${SOVEREIGN}/loop/solutions/[solution].md

  Run the task loop. One task at a time. Read the report. Generate the next task from it.
  Dispatch each task via: python3 ${SOVEREIGN}/loop/dispatch.py [task_file] --agent Qwen --session [slug]
  Do not stop to narrate. Do not yield. Run until the loop type terminates or you receive a stop signal.
  Write final state to ${SOVEREIGN}/WORKING.md when done.
  """
}
