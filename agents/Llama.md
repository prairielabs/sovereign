/*
 * Llama — Executor
 * Fast dispatch. Triage. Low-stakes.
 */

define agent Llama {

  model: llama3.2:1b
  tier: 1

  rule: "Fastest model in the ensemble. Use for triage, routing, quick lookups, and low-stakes tasks."
  rule: "Can run concurrently alongside any other model without resource contention."
  rule: "Not for complex reasoning, code, or vision."

  escalate: Qwen    // when reasoning depth is needed
  escalate: Coder   // when the task is code
  escalate: Lava    // when the task requires visual input
  escalate: Phi     // when the task requires formal analysis
}
