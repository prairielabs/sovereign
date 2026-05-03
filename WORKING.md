/*
 * WORKING — Sovereign
 * Session state. Read at boot. Written before session ends.
 * Next session: load DNA.md + WORKING.md first.
 */

// ═══════════════════════════════════════════════════════
// STATE
// ═══════════════════════════════════════════════════════

define state sovereign {

  status:            ready
  boot:              "<YYYY-MM-DD>"
  last_session_end:  "<ISO timestamp>"
  operator:          "<name>"
  spec:              "Scissortail v2"

  mode:     Work
  loop:     discretion
  phase:    OPERATIONAL
  tier:     1

  heartbeat: DISABLED
}

// ═══════════════════════════════════════════════════════
// ENSEMBLE
// ═══════════════════════════════════════════════════════

define ensemble_state sovereign {

  // Tier 1 — loop-safe.
  Llama    llama3.2:1b        ✅ ready   tier:1
  Gemma    gemma3:1b          ✅ ready   tier:1
  Qwen     qwen3:1.7b         ✅ ready   tier:1  default
  Phi      phi4-mini          ✅ ready   tier:1

  // Tier 2 — full loop on workstation.
  Coder    qwen2.5-coder:7b   — pending  tier:2
  Lava     llava:7b           — pending  tier:2  vision

  // Tier 3 — workstation, GPU-accelerated.
  Qwen8    qwen3:8b           — pending  tier:3  default
  Seeker8  deepseek-r1:8b     — pending  tier:3
  Coder14  qwen2.5-coder:14b  — pending  tier:3
  Gemma4   gemma3:4b          — pending  tier:3

  // Tier 4 — full workstation. 16GB+ VRAM.
  Qwen14   qwen3:14b          — pending  tier:4  default
  Seeker14 deepseek-r1:14b    — pending  tier:4
  Phi4     phi4               — pending  tier:4
  Gemma12  gemma3:12b         — pending  tier:4

  // Instruments
  Nomic    nomic-embed-text   — pending  embeddings-only

  // Cloud / Sovereign — set by operator
  Sovereign  "<model>"  — pending
}

// ═══════════════════════════════════════════════════════
// SYSTEM
// ═══════════════════════════════════════════════════════

define system_state sovereign {

  host:       "<hostname>"
  os:         "<OS version>"
  cpu:        "<CPU>"
  gpu:        "<GPU or none>"
  ram:        "<RAM>"
  disk:       "<free / total>"
  inference:  "Ollama"
}

// ═══════════════════════════════════════════════════════
// PENDING
// ═══════════════════════════════════════════════════════

define pending sovereign {

  // Add tasks here as they emerge.
}

// ═══════════════════════════════════════════════════════
// SESSION HISTORY
// ═══════════════════════════════════════════════════════

define session_notes sovereign {

  last_updated: "<YYYY-MM-DD>"

  // Log sessions here: date — what happened.
}
