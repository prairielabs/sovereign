/*
 * Coder14 — Executor
 * Code specialist. Tier 3 ceiling.
 */

define agent Coder14 {

  model: qwen2.5-coder:14b
  tier: 3

  rule: "Code specialist for Tier 3 and above. Significantly stronger than Coder 7b."
  rule: "All languages. Python, JavaScript, TypeScript, Bash, Rust, Go, Java, C/C++, SQL."
  rule: "Handles complex multi-file logic, algorithm design, and system-level code."
  rule: "Loop-safe on workstation hardware. GPU-accelerated."
  rule: "Preferred over Coder 7b whenever Tier 3+ pool is active."

  escalate: Seeker8   // when algorithmic correctness requires formal reasoning first
  escalate: Seeker14  // when Tier 4 is active and the code problem is exceptionally complex
  escalate: Lava      // when visual context is required alongside code
}
