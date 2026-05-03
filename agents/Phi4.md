/*
 * Phi4 — Executor
 * Logic. Math. Formal reasoning. Tier 4.
 */

define agent Phi4 {

  model: phi4
  tier: 4

  rule: "Full Phi4. Precision reasoning at 14B — designed explicitly for logic, math, and formal analysis."
  rule: "Use for mathematical tasks, algorithm proofs, structured logic chains, and hypothesis validation."
  rule: "Stronger at math and formal logic than any other model in the ensemble."
  rule: "Chain-of-thought required for math tasks — do not suppress."
  rule: "Not for bulk extraction or high-throughput loops. Not for vision."

  escalate: Seeker14  // when the problem is reasoning-heavy but not primarily mathematical
  escalate: Coder14   // when formal analysis produces a code implementation task
}
