/*
 * Qwen — Executor
 * Default executor. General reasoning.
 */

define agent Qwen {

  model: qwen3:1.7b
  tier: 1
  default: active

  rule: "Default executor for general tasks, analysis, and reasoning."
  rule: "First choice when the task is text-centric and not specialized."
  rule: "Fast. Broad. Not deep."

  escalate: Phi     // when depth and precision matter more than speed
  escalate: Coder   // when the task is primarily code
  escalate: Lava    // when the task requires visual input
}
