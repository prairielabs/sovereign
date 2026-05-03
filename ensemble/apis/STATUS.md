/*
 * Ensemble — APIs
 * Cloud providers. Last resort, not default.
 */

define ensemble apis {

  provider: Anthropic
  models: "claude-sonnet, claude-opus"
  status: active
  route: "via OpenClaw"

  rule: "Cloud is available when local capacity is genuinely insufficient."
  rule: "Not the default. Local first. Always."
}
