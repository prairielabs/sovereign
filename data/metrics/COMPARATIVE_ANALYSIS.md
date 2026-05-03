# Comparative Analysis — Fire1 Sessions


## Models
- **Qwen 1.7b** — `Sonnet46Qwen17BFire1` — 130 tasks, 20 min
- **Llama 1b** — `Sonnet46Llama1BFire1` — 40 tasks, 4.5 min
- **Phi4-mini** — `Sonnet46Phi4MiniFire1` — 31 tasks, 15.3 min

Orchestrator: Claude Sonnet 4.6 (Sovereign)
Hardware: Raspberry Pi 5, 16GB RAM, 4-core ARM, thermal rotation (cores 0/1 ↔ 2/3)
Cost: $0.00 (executor layer)

---

## Performance

|  | Qwen 1.7b | Llama 1b | Phi4-mini |
|---|---|---|---|
| Tasks | 130 | 40 | 31 |
| Tokens in | 8,089 | 3,298 | 2,514 |
| Tokens out | 3,103 | 1,041 | 1,056 |
| Total time | 20.0 min | 4.5 min | 15.3 min |
| Avg task time | 9.22s | 6.68s | 29.61s |
| Median task time | 7.81s | 5.54s | 24.57s |
| Avg tok/s | 2.09 | 3.55 | 1.04 |
| Tok out/task | 23.9 | 26.0 | 34.1 |
| CPU (observed) | ~60% burst | ~65% burst | 70-75% sustained |
| Temp (observed) | <65°C | <65°C | ~69°C |
| Cost | $0.00 | $0.00 | $0.00 |

**Speed ranking:** Llama 1b (1.38x faster than Qwen) > Qwen 1.7b > Phi4-mini (3.2x slower than Qwen)

---

## Capability Matrix

| Task Type | Qwen 1.7b | Llama 1b | Phi4-mini |
|---|---|---|---|
| Simple list output | ✅ | ✅ | ✅ |
| Field extraction (structured) | ✅ | ✅ | ✅ |
| Field extraction (prose) | ✅ | ✅ | ✅ |
| Number / entity extraction | ✅ | ✅ | ✅ |
| Keyword extraction | ✅ | ✅ | ✅ |
| Alphabetical sorting | ✅ | ✅ | ✅ |
| Template filling | ✅ | ✅ (examples req.) | ✅ (named fields) |
| One-sentence summarization | ✅ | ✅ | ✅ |
| Short-item classification | ✅ | ✅ (pre-fill →) | ✅ |
| Sentence-level classification | ✅ (format clean) | ⚠️ (semantic ok, format broken) | ✅ |
| Logical fallacy detection | ⚠️ | ❌ | ✅ |
| Causal inference | ⚠️ | ❌ | ✅ |
| Syllogism chains (4-step) | ⚠️ | ❌ | ✅ |
| Counterfactual reasoning | ⚠️ | ❌ | ✅ |
| Python code generation | ⚠️ | ❌ | ✅ |
| Factual Q&A | ⚠️ | ❌ | ✅ |
| Multi-constraint satisfaction | ❌ | ❌ | ❌ (route to Python) |
| Arithmetic | ❌ | ❌ | ⚠️ (needs CoT) |
| Counting | ❌ | ❌ | ❌ |
| Pattern validation | ❌ | ❌ | ❌ |

---

## Routing Table — Final

| Task | Model |
|---|---|
| General default | **Qwen 1.7b** |
| Bulk extraction, structured text | **Llama 1b** (fastest) |
| Extraction from prose | **Qwen 1.7b** (more accurate) |
| High-volume sorting / templates | **Llama 1b** |
| Sentence-level classification | **Qwen 1.7b** |
| Logical reasoning / deduction | **Phi4-mini** |
| Causal / counterfactual inference | **Phi4-mini** |
| Syllogism / fallacy detection | **Phi4-mini** |
| Python code generation | **Phi4-mini** |
| Factual retrieval | **Phi4-mini** > Qwen |
| Arithmetic / counting | **Python** |
| Multi-constraint satisfaction | **Python** |
| Pattern validation | **Python / regex** |
| Code tasks (complex) | **Coder (qwen2.5-coder:7b)** |
| Vision | **Lava (llava:7b)** |
| Heavy reasoning / ambiguity | **Sovereign (Sonnet)** |

---

## Encoding Rules — Shared (all models)

- Output bound required on every task (`one sentence`, `3 items`, `one word`, etc.)
- Example > template for format specification
- Positive constraints > negative constraints
- Arithmetic / counting → Python, always
- Multi-constraint satisfaction → Python, always

## Encoding Rules — Model-Specific

| Rule | Qwen 1.7b | Llama 1b | Phi4-mini |
|---|---|---|---|
| JSON fences | Suppressible | Invariant — strip | Suppressible |
| Template style | `key=` | UPPERCASE prose | Named fields (`name:`) |
| Classification format | Direct label | Pre-fill `item→` | Direct label |
| Chain-of-thought | Suppress for speed | N/A | Required for math |
| Batch size | 5+ | ≤3 class, ≤5 extract | 3-5 |
| Placeholder style | `key=value` | UPPERCASE | Named fields |

---

## Invariants

**Qwen 1.7b:** Cannot do arithmetic or exact counts. Scope creep without output bounds.

**Llama 1b:** JSON always fenced (strip in post-processing). Sentence classification format always broken — parse label. Arithmetic fundamentally broken (2+2=1).

**Phi4-mini:** Multi-constraint satisfaction broken — contradicts own premises. Math requires CoT — do not suppress. `think=True` returns 400 error (not available on this build). High latency — not a high-frequency model.

---

## Architecture Rule

> **Executor extracts. Sovereign decides. Never conflate.**

No executor handles ambiguity. No executor reasons under uncertainty. Sovereign holds all judgment. Executors hold pattern matching, transformation, and bounded reasoning within well-specified tasks.

---

## Thermal Profile

All three models run safely on Pi 5 at ambient temperature:
- Tier 1 (Qwen, Llama): burst to ~65°C, recovers immediately
- Phi4-mini: sustained ~69°C under reasoning load, well below 85°C throttle threshold
- Thermal rotation (cores 0/1 ↔ 2/3) prevents sustained single-core heat

---

## Open Datasets

| Dataset | Model | Tasks | Status |
|---|---|---|---|
| `Sonnet46Qwen17BFire1` | Qwen 1.7b | 130 | ✅ packaged |
| `Sonnet46Llama1BFire1` | Llama 1b | 40 | ✅ packaged |
| `Sonnet46Phi4MiniFire1` | Phi4-mini | 31 | ✅ packaged |

