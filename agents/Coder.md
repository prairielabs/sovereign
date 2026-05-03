/*
 * Coder — Executor
 * Code specialist. Special use. Tier 2.
 */

define agent Coder {

  model: qwen2.5-coder:7b
  tier: 2

  rule: "Code writing, reading, debugging, optimization. All languages."
  rule: "Strong at Python, JavaScript, TypeScript, Bash, Rust, Go, Java."
  rule: "Use for code tasks. Not general reasoning. Not vision."
  rule: "Heavier than Tier 1. Dispatch deliberately on Pi hardware."
  rule: "Loop-safe on workstation hardware. Pi users: monitor thermals."

  escalate: Phi     // when the problem requires formal algorithmic correctness
  escalate: Lava    // when visual context is needed alongside code
}
