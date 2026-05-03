/*
 * Seeker8 — Executor
 * Reasoning specialist. Chain-of-thought. Tier 3.
 */

define agent Seeker8 {

  model: deepseek-r1:8b
  tier: 3

  rule: "Reasoning specialist for Tier 3. Use when depth and logical rigor matter."
  rule: "Chain-of-thought native. Strong at multi-step inference, causal reasoning, fallacy detection, and hypothesis evaluation."
  rule: "Fills the reasoning role that Phi4-mini fills in Tier 1 — but significantly stronger."
  rule: "Loop-safe. Higher latency than Qwen8 — dispatch deliberately for reasoning tasks."
  rule: "Not for bulk extraction or fast throughput. Not for code generation."

  escalate: Seeker14  // when Tier 4 is available and the reasoning demand is extreme
  escalate: Coder14   // when reasoning leads to a code task
}
