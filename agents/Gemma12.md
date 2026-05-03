/*
 * Gemma12 — Executor
 * Fast capable general. Tier 4 speed layer.
 */

define agent Gemma12 {

  model: gemma3:12b
  tier: 4

  rule: "Fast capable executor in Tier 4. Strong instruction following with lower VRAM footprint than 14B models."
  rule: "Preferred when speed matters and the task does not require Tier 4 reasoning depth."
  rule: "Leaves VRAM headroom — useful when running concurrent tasks or alongside heavier models."
  rule: "Strong at classification, summarization, extraction, and structured formatting at Tier 4 speed."
  rule: "Loop-safe. GPU-accelerated."

  escalate: Qwen14    // when format precision and depth are both needed
  escalate: Seeker14  // when the task requires formal reasoning
  escalate: Coder14   // when the task is code
}
