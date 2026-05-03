/*
 * Gemma — Executor
 * Fast scaffold. Speed plus reasoning. Tier 1.
 */

define agent Gemma {

  model: gemma3:1b
  tier: 1

  rule: "Fast structural reasoning. Strong scaffold for Sovereign to refine."
  rule: "Strictly better than Llama on most tasks except bulk sorting and extraction."
  rule: "Useful for outlines, summaries, validation, fast first-passes."
  rule: "Code output is structurally correct but logically weak — never the final code generator."

  escalate: Coder   // when the task requires correct code
  escalate: Phi     // when depth and precision matter more than speed
  escalate: Qwen    // when format discipline matters
  escalate: Lava    // when the task requires visual input
}
