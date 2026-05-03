# CHANGELOG

Running patch notes for Sovereign. Most recent first.

---

## v1.2 — 2026-04-29

### Channel Optimization Corpus Complete

`projects/channel-optimization/ENCODING-GUIDE.md` — the full comparative encoding guide.

14 models × 10 tasks = 140 optimization drills. Results:

- **Encoding overhead matrix** — three models (deepseek-r1:8b, qwen3:14b, gemma3:12b) accept the baseline encoding with zero adjustment across all 10 task types.
- **Per-task encoding variations** — side-by-side table of what changes per model per task type.
- **Cross-tier pattern analysis** — case constraint gradient, JSON fence gradient, and reasoning capability threshold are architecture-family-linked, not tier-linked.
- **Routing table and reference card** — Sovereign's dispatch layer input.

The finding: encoding adjustments recovered every failure except one hard capability ceiling (llama3.2:1b on logic). That exception is the important one — it is the boundary between channel failure and capability ceiling. That boundary is where the research avenue points.

### Framing

The thesis-as-claim language in `README.md` and `docs/architecture.md` has been corrected to thesis-as-hypothesis. The channel optimization work is evidence toward a direction, not proof of a closed claim.

> *"This is the research avenue."*

---

## v1.1 — 2026-04-28

### Tier Architecture Expansion

Sovereign now supports four executor tiers. A tier is a **pool of executors** — not a capability ceiling on individual models. Users select a tier based on available hardware. Each tier is a superset of the one below it. Active tier is stored in `WORKING.md`.

| Tier | Target Hardware | Pool Size |
|------|-----------------|-----------|
| 1 | Raspberry Pi 5, low-end hardware | 4 models |
| 2 | Pi ceiling — adds code and vision | +2 models |
| 3 | Mid-range workstation with GPU | +4 models |
| 4 | Full workstation, 16GB+ VRAM | +4 models |

### New Agents (Tier 3)

- **Qwen8** (`qwen3:8b`) — General default for Tier 3. Higher precision than Qwen 1.7b. Loop-safe. GPU-accelerated.
- **Seeker8** (`deepseek-r1:8b`) — Reasoning specialist. Chain-of-thought native. Fills the role Phi holds in Tier 1, but significantly stronger.
- **Gemma4** (`gemma3:4b`) — Fast capable general. Strong scaffold. Lower latency than Qwen8.
- **Coder14** (`qwen2.5-coder:14b`) — Code ceiling for Tier 3. Handles complex multi-file logic and system-level code.

### New Agents (Tier 4)

- **Qwen14** (`qwen3:14b`) — General default for Tier 4. Highest precision general executor in the ensemble. Fits entirely in GPU VRAM at 16GB.
- **Seeker14** (`deepseek-r1:14b`) — Reasoning ceiling of the ensemble. The executor closest to Sovereign's own reasoning capability.
- **Phi4** (`phi4`) — Logic and math ceiling. Designed explicitly for formal analysis, proofs, and structured reasoning.
- **Gemma12** (`gemma3:12b`) — Fast capable general in Tier 4. Lower VRAM footprint than 14B models — leaves headroom for concurrent tasks.

### Workstation Doctrine (New)

Added `define doctrine workstation` to DNA.md. Applies to Tier 3 and Tier 4 environments.

Key changes from Pi doctrine:
- No core pinning. No thermal rotation.
- All agents are loop-safe. No one-shot constraints.
- GPU-accelerated inference via ROCm (AMD) or CUDA (NVIDIA).
- Tier 2 models (Coder, Lava) are also loop-safe on workstation hardware.

### Updated Agents (Tier 2)

- **Coder** — Removed unconditional one-shot constraint. Now loop-safe on workstation hardware; Pi users should still dispatch deliberately.
- **Lava** — Same change. Loop-safe on workstation; Pi users: monitor thermals.

### DNA Ensemble Section Rewrite

`define ensemble ollama` in `DNA.md` now documents the full 4-tier structure with per-tier target hardware descriptions. Instruments (Nomic) are noted as active at all tiers.

### Loop Structure

Created `loop/` directory structure for task/report protocol:
```
loop/tasks/       — Sovereign → Executor
loop/reports/     — Executor → Sovereign
loop/solutions/   — Sovereign's general solution per problem
loop/problems/    — problem statements from user
loop/results/     — Sovereign → user
loop/questions/   — Executor → Sovereign (frontier executors)
loop/answers/     — Sovereign → Executor
```

Loop directories are gitignored (session-specific artifacts). `.gitkeep` preserves structure.

### Channel Optimization Data

Added `data/metrics/ml-opt-qwen17b-workstation.md` — results of a 10-task ML optimization drill on `qwen3:1.7b`. Documents the derived encoding protocol for reliable output from Qwen 1.7b:

- Explicit count + format specifier = most reliable output bound
- `"nothing else"` / `"no explanation"` suppresses wrapper prose
- `Answer:` colon-suffix = best extraction anchor
- `"plain text"` modifier suppresses trailing markdown artifacts
- `"no markdown fences"` required for clean JSON output
- `[FIELD]` bracket delimiters = reliable placeholder syntax
- Angle-bracket `<placeholders>` echo literally — avoid

**Success rate: 9/10 (90%)** across extraction, classification, sorting, summarization, reasoning, template fill, keyword extraction, one-word answer, structured output, and logic task types.

### Tooling

- Added `prep-reset.sh` — session shutdown utility. Flushes `RAM.md`, updates `last_session_end` timestamp in `WORKING.md`, prints loop artifact count, and prompts Sovereign to write session notes and memory.
- Added `.gitignore` — excludes session-specific loop artifacts and instance memory from version control.

---

## v1.0 — 2026-04-27

Initial public release. Launched at UNT CSCE Club, April 27, 2026.

- `DNA.md` — system constitution in Scissortail v2 spec language
- `WORKING.md` / `RAM.md` — durable and volatile session state
- `INSTALLER.md` / `DOCTOR.md` / `PULSE.md` — operational runbooks
- `agents/` — 6 executor cards: Llama, Gemma, Qwen, Phi, Coder, Lava
- `apps/` — Mozart, Savannah, Spur prompt systems
- `data/` — proof-of-concept artifacts: orchestral audio, physics renders, metrics
- `docs/` — architecture overview, thermal doctrine, theory
- `scissortail/` — SCISSORTAIL.md spec language definition
