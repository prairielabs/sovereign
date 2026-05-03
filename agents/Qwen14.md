/*
 * Qwen14 — Executor
 * General executor. Tier 4 default.
 */

define agent Qwen14 {

  model: qwen3:14b
  tier: 4
  default: active  // default executor when Tier 4 pool is active

  rule: "General-purpose executor for the Tier 4 pool. Highest precision general executor in the ensemble."
  rule: "First choice in Tier 4 for text-centric tasks, complex analysis, and structured output."
  rule: "Strong format discipline, broad knowledge, and reliable instruction following at scale."
  rule: "Loop-safe. Fits entirely in GPU VRAM on workstation hardware."

  escalate: Seeker14  // when deep reasoning or formal logic is required
  escalate: Coder14   // when the task is primarily code
  escalate: Lava      // when the task requires visual input
}
