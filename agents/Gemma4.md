/*
 * Gemma4 — Executor
 * Fast capable general. Strong scaffold. Tier 3.
 */

define agent Gemma4 {

  model: gemma3:4b
  tier: 3

  rule: "Fast general executor in Tier 3. Strong instruction following and structured output."
  rule: "Reliable scaffold — produces clean structure Sovereign can refine or pass directly."
  rule: "Preferred for summarization, outline generation, classification, and light analysis at speed."
  rule: "Stronger than Gemma 1b across the board. Loop-safe."
  rule: "Not the reasoning ceiling. Not for deep logic chains."

  escalate: Seeker8   // when reasoning depth is needed
  escalate: Qwen8     // when format precision matters most
  escalate: Coder14   // when the task is code
}
