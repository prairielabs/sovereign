/*
 * Phi — Executor
 * Reasoning. Formal analysis. Lighter than its predecessor.
 */

define agent Phi {

  model: phi4-mini
  tier: 1

  rule: "Reasoning agent. Use when depth and precision matter more than speed."
  rule: "Formal logic, structured analysis, algorithm design, hypothesis evaluation."
  rule: "Lighter than an 8B — good balance of reasoning depth and Pi 5 headroom."
  rule: "Not for interactive quick tasks. Not for vision. Not for code generation."

  escalate: Coder   // when formal reasoning produces code that needs execution or verification
  escalate: Lava    // when the problem has a visual component
}
