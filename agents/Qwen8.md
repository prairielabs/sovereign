/*
 * Qwen8 — Executor
 * General executor. Mid-tier precision.
 */

define agent Qwen8 {

  model: qwen3:8b
  tier: 3
  default: active  // default executor when Tier 3 pool is active

  rule: "General-purpose executor for the Tier 3 pool. Handles most task types with higher precision than Tier 1."
  rule: "First choice in Tier 3 for text-centric tasks, analysis, and structured output."
  rule: "Stronger format discipline and reasoning depth than Qwen 1.7b. Still fast."
  rule: "Loop-safe. GPU-accelerated on workstation hardware."

  escalate: Seeker8   // when the task requires deep reasoning or formal logic
  escalate: Coder14   // when the task is primarily code
  escalate: Lava      // when the task requires visual input
}
