/*
 * Ensemble — OpenClaw
 * Sovereign's runtime. Gateway, tools, shell, APIs.
 */

define ensemble openclaw {

  const AGENT      = ""               // Operator names this instance.
  const WORKSPACE  = "~/sovereign"
  const MODEL      = ""               // e.g. "anthropic/claude-sonnet-4-6"
  const ACCESS     = "elevated"

  rule: "OpenClaw is the operator layer. Runs Sovereign's dispatch logic."
  rule: "Manages filesystem, shell, APIs, and channel routing."
  rule: "AGENT is the per-instance name the operator chose for the live Sovereign."
  rule: "All tool access unrestricted in this environment."
}
