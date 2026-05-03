/*
 * Ensemble — Ollama
 * Local model server. http://localhost:11434
 */

define ensemble ollama {

  // Tier 1 — Daily drivers. Pi-safe. Default routing.
  agent: Qwen     model: qwen3:1.7b        size: 1.4GB   default: active
  agent: Llama    model: llama3.2:1b       size: 1.3GB
  agent: Gemma    model: gemma3:1b         size: 815MB
  agent: Phi      model: phi4-mini         size: 3.8GB

  // Tier 2 — Special use. Heavier. Dispatch deliberately.
  agent: Coder    model: qwen2.5-coder:7b  size: 4.7GB
  agent: Lava     model: llava:7b          size: 4.7GB

  rule: "All inference is CPU-only on the reference Pi 5 build. No discrete GPU."
  rule: "Max one Tier 2 model loaded at a time."
  rule: "Llama and Gemma can run concurrently with any model."
}
