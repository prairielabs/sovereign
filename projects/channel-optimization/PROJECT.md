# Project: Channel Optimization Corpus

**Owner:** Sovereign  
**Status:** In progress  
**Goal:** Derive and document the optimized encoding protocol for every executor model in the ensemble via 10-task ML optimization drills. Produce a comparative corpus for users and researchers.

---

## What This Is

A 10-task channel optimization loop run against each model individually. Each loop:
1. Tests 10 task types (extraction, classification, sorting, summarization, reasoning, template fill, keyword extraction, one-word answer, structured JSON output, logic)
2. Adjusts encoding after each report
3. Produces a result file documenting what encoding patterns worked, what failed, and the optimized prompt templates for that model

The corpus is training data for the Sovereign→Executor channel. It answers: *for each model, how should Sovereign encode meaning to maximize reliable transfer?*

---

## Models to Drill

| Agent | Model | Tier | Status |
|-------|-------|------|--------|
| Qwen | qwen3:1.7b | 1 | ✅ DONE — see `data/metrics/ml-opt-qwen17b-workstation.md` |
| Llama | llama3.2:1b | 1 | ✅ DONE — see `results/ml-opt-llama32-1b.md` — 8/10 + 1 partial |
| Gemma | gemma3:1b | 1 | ✅ DONE — see `results/ml-opt-gemma3-1b.md` — 10/10 (adjusted) |
| Phi | phi4-mini | 1 | ✅ DONE — see `results/ml-opt-phi4-mini.md` — 8/10 + 2 partial |
| Coder | qwen2.5-coder:7b | 2 | ✅ DONE — see `results/ml-opt-qwen25coder-7b.md` — 9/10 + 1 partial |
| Lava | llava:7b | 2 | ✅ DONE — see `results/ml-opt-llava-7b.md` — 9/10 + 1 partial (text-only) |
| Qwen8 | qwen3:8b | 3 | ✅ DONE — see `results/ml-opt-qwen3-8b.md` — 9/10 + 1 partial |
| Seeker8 | deepseek-r1:8b | 3 | ✅ DONE — see `results/ml-opt-deepseekr1-8b.md` — 10/10 baseline |
| Gemma4 | gemma3:4b | 3 | ✅ DONE — see `results/ml-opt-gemma3-4b.md` — 10/10 (adjusted) |
| Coder14 | qwen2.5-coder:14b | 3 | ✅ DONE — see `results/ml-opt-qwen25coder-14b.md` — 10/10 (adjusted) |
| Qwen14 | qwen3:14b | 4 | ✅ DONE — see `results/ml-opt-qwen3-14b.md` — 10/10 baseline |
| Seeker14 | deepseek-r1:14b | 4 | ✅ DONE — see `results/ml-opt-deepseekr1-14b.md` — 10/10 (adjusted) |
| Phi4 | phi4 | 4 | ✅ DONE — see `results/ml-opt-phi4.md` — 10/10 (adjusted) |
| Gemma12 | gemma3:12b | 4 | ✅ DONE — see `results/ml-opt-gemma3-12b.md` — 10/10 baseline |

Nomic (nomic-embed-text) is embeddings-only — excluded from generation drills.

---

## Output Structure

Each completed drill produces one result file in this folder:

```
projects/channel-optimization/
  PROJECT.md                          ← this file
  results/
    ml-opt-llama32-1b.md
    ml-opt-gemma3-1b.md
    ml-opt-phi4-mini.md
    ml-opt-qwen25coder-7b.md
    ml-opt-llava-7b.md
    ml-opt-qwen3-8b.md
    ml-opt-deepseekr1-8b.md
    ml-opt-gemma3-4b.md
    ml-opt-qwen25coder-14b.md
    ml-opt-qwen3-14b.md
    ml-opt-deepseekr1-14b.md
    ml-opt-phi4.md
    ml-opt-gemma3-12b.md
```

Task and report files go in `loop/tasks/` and `loop/reports/` as usual (gitignored). Only the result files land here (committed).

---

## Run Protocol

For each pending model:

1. Run a 10-task ML optimization loop via subagent (do not block main session)
2. Use the same 10 task types as the Qwen 1.7b baseline for comparability
3. Adjust encoding after each report — the loop is the optimization
4. Write result to `projects/channel-optimization/results/ml-opt-{model-slug}.md`
5. Update the status table above: ⬜ → ✅
6. Note any model-specific encoding differences vs. the Qwen 1.7b baseline

---

## Task Types (Fixed Set — All Drills)

Run in this order for cross-model comparability:

1. **Extraction** — extract N items from a passage
2. **Classification** — classify input into one of N categories
3. **Sorting** — sort a list alphabetically
4. **Summarization** — summarize in exactly one sentence
5. **Reasoning** — multi-step arithmetic/logic, extract final answer
6. **Template fill** — fill [FIELD] placeholders from key=value input
7. **Keyword extraction** — extract N keywords, plain text
8. **One-word answer** — single-word response
9. **Structured JSON output** — produce valid JSON, no fences
10. **Logic puzzle** — detect fallacy or evaluate syllogism

---

## Deliverable

✅ **COMPLETE** — `ENCODING-GUIDE.md` written 2026-04-29.

Comparative encoding guide: side-by-side encoding rules per model, per-task variation tables, routing recommendations, and thesis evidence. 31KB, 7 parts.

---

## Notes

- Priority order: Tier 1 first (Pi users need these most), then Tier 3, then Tier 4, then Tier 2
- Lava is vision-only — run text-only tasks, note that visual tasks require separate protocol
- Seeker models (deepseek-r1) have thinking mode — note chain-of-thought behavior in results
- Compare Tier 3/4 results against Tier 1 baseline: does encoding simplify at larger scale?
