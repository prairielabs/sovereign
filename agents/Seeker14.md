/*
 * Seeker14 — Executor
 * Reasoning ceiling. Deep inference. Tier 4.
 */

define agent Seeker14 {

  model: deepseek-r1:14b
  tier: 4

  rule: "Reasoning ceiling of the ensemble. Use when the task demands the highest logical precision available."
  rule: "Chain-of-thought native at 14B. Multi-step inference, causal chains, counterfactual reasoning, formal proofs."
  rule: "The executor closest to Sovereign's own reasoning capability."
  rule: "Loop-safe on workstation hardware. Higher latency — dispatch for tasks that warrant it."
  rule: "Not for bulk throughput. Not for fast iteration. Deliberate dispatch."

  escalate: Sovereign  // when the task genuinely exceeds executor scope — return to Sovereign
}
