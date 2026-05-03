/*
 * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 *
 *   SCISSORTAIL
 *   Spec Language for Multi-Agent DNA
 *
 *   Version 2 — 2026
 *
 *   The specification is the software.
 *   Load it into context. It runs.
 *
 * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 */


// ═══════════════════════════════════════════════════════
// LANGUAGE
// ═══════════════════════════════════════════════════════

define language scissortail {

  const VERSION    = "2"
  const PURPOSE    = "DNA specification for multi-agent systems"
  const RUNTIME    = "context window"
  const FORMAT     = ".md"

  description: """
  Scissortail is a declarative spec language for writing DNA
  in multi-agent systems. The reader is the runtime. There is
  no compiler. No parser. The spec creates gravity wells in
  the model's behavior through precision of definition.

  Load it into context. It runs.
  """

  rule: "All constructs begin with define."
  rule: "Properties use colon notation. Constants use equals."
  rule: "One rule per line. One truth per rule."
  rule: "Prose only in description: blocks. Used sparingly."
  rule: "No procedures. No steps. Definitions only."
  rule: "Structure creates gravity. The model infers behavior from shape."
}


// ═══════════════════════════════════════════════════════
// CONSTRUCTS
// ═══════════════════════════════════════════════════════

define constructs scissortail {

  define system      // The top-level entity. One per DNA.
  define agent       // A member of the ensemble.
  define ensemble    // A tier or group of agents.
  define loop        // A loop type with termination logic.
  define mode        // An ML operating mode.
  define channel     // The protocol between Sovereign and Executor.
  define guard       // A hard constraint. Cannot be overridden.
  define memory      // Memory structure and scope.
  define project     // User project container. Unstructured.
}


// ═══════════════════════════════════════════════════════
// PROPERTIES
// ═══════════════════════════════════════════════════════

define properties scissortail {

  const NAME = value      // Immutable named value.
  rule: "..."             // One behavioral truth. Imperative. Present tense.
  description: """..."""  // Prose block. Sparingly.
  model: [id]             // Model assigned to an agent.
  tier: [1|2|3]           // Execution tier.
  default: [value]        // Persistent default state.
  signal: [type]          // What flows through a channel.
  escalate: [agent]       // Where capacity overflows to.
  when: [condition]       // Conditional behavior trigger.
}


// ═══════════════════════════════════════════════════════
// CONVENTIONS
// ═══════════════════════════════════════════════════════

define conventions scissortail {

  rule: "System names are capitalized. Sovereign. Qwen. Coder."
  rule: "Properties are lowercase. model: tier: rule: signal:"
  rule: "Constants are SCREAMING_SNAKE_CASE."
  rule: "One blank line between properties. One blank line between blocks."
  rule: "Comments use //. Inline or block."
  rule: "Nothing is deleted from DNA mid-run. Append only."
}
