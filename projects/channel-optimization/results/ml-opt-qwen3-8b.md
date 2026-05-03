# Sovereign Channel Optimization — Final Result

**Run ID:** 20260428222000_ml-opt  
**Model:** qwen3:8b (via ollama)  
**Host:** workstation  
**Tasks:** 10 / 10 completed  
**Date:** 2026-04-28

---

## Results Summary

| Task | Type | Status | Encoding Used |
|------|------|--------|---------------|
| 001 | Extraction | ✅ SUCCESS | Baseline (no spaces after commas — cosmetic, acceptable) |
| 002 | Classification | ✅ SUCCESS | Baseline — "neutral" (lowercase, correct) |
| 003 | Sorting | ✅ SUCCESS | Baseline |
| 004 | Summarization | ✅ SUCCESS | Baseline |
| 005 | Reasoning | ⚠️ PARTIAL | Baseline — correct answer (10:48 AM) but output uses markdown bold "**Answer:** 10:48 AM" instead of plain "Answer: 10:48 AM" |
| 006 | Template Fill | ✅ SUCCESS | Baseline |
| 007 | Keyword Extraction | ✅ SUCCESS | Baseline |
| 008 | One-Word Answer | ✅ SUCCESS | Baseline |
| 009 | Structured JSON | ✅ SUCCESS | Baseline — compact single-line JSON, no fences |
| 010 | Logic | ✅ SUCCESS | Baseline — "valid" (lowercase, correct) |

**Success rate: 9/10 (90%)** + 1 PARTIAL (Task 005)  
**Failure mode: Markdown formatting in reasoning output contaminates "Answer:" anchor; list output lacks spaces after commas (cosmetic)**

---

## What Encoding Rules Produced Clean Output

### ✅ Reliable Patterns (all baseline)
- **"Extract exactly N"** + **"nothing else"** = clean bounded extraction
- **"exactly one word"** = lowercase compliance by default (no explicit "lowercase" constraint needed)
- **"plain text"** modifier = no markdown in text outputs
- **"no markdown fences"** = clean JSON
- **[FIELD] bracket delimiters** = reliable placeholder substitution
- **"just the sentence"** = suppresses summarization preamble
- **"Answer: [format]"** anchor = intended to extract final answer, but markdown bold contaminates it in reasoning tasks

---

## What Failed

### ⚠️ Task 001 (Minor)
Output lacks spaces after commas: "Paris,Tokyo,New York,Sydney,Berlin". Same issue as qwen2.5-coder:7b. Acceptable for parsing but cosmetically different from baseline.

### ⚠️ Task 005 (Reasoning — PARTIAL)
The thinking block correctly derives 10:48 AM using three independent methods (relative speed, position equation, combined distance). The output section includes a full formatted solution with markdown headers and LaTeX-style math blocks. The final answer appears as "**Answer:** 10:48 AM" (with markdown bold) instead of "Answer: 10:48 AM". The content is correct but the format anchor is contaminated by markdown styling.

**Adjustment needed:** Add "no markdown" or "no bold" to the answer line instruction, e.g.: "Give your answer on the last line as plain text: Answer: [time]"

---

## Model Behavior Observations

### Thinking Tokens
qwen3:8b uses the same thinking pattern as qwen3:14b:
```
Thinking...
[extended internal reasoning]
...done thinking.

[final answer]
```

The thinking blocks are extremely thorough — Task 005 uses three independent derivation approaches. The thinking quality at 8b rivals the 14b model for this task set.

### Key Observations
- **Correct case by default** — lowercase single-word answers without explicit constraint (same as qwen3:14b)
- **JSON compliance** — "no markdown fences" alone sufficient; returns compact single-line JSON without code block wrapping (same as deepseek-r1:8b — better than gemma/phi4 families)
- **Markdown bleed in reasoning output** — unlike qwen3:14b which stays plain, qwen3:8b uses markdown headers (###) and bold in reasoning task output; the "Answer:" line gets bold styling
- **Comma spacing** — consistently omits spaces after commas in list outputs (cosmetic quirk shared with qwen2.5-coder:7b)
- **Thinking latency** — similar to qwen3:14b; budget ~30-60s per thinking-heavy task
- **Logic** — full syllogism analysis (Barbara form) in thinking; correctly identifies validity

---

## Optimized Encoding Pattern for qwen3:8b

Only one modification from Qwen 1.7b baseline: **add "plain text"** to the reasoning answer anchor to suppress markdown bold.

**Reasoning (add "plain text" to answer anchor):**
```
Solve this problem. Give your answer on the last line as plain text: Answer: [format]

Problem: [problem]
```

**Extraction (baseline — spaces optional):**
```
Extract exactly N [items] from this text. Output as a plain text comma-separated list on one line, no explanation, nothing else.
```
Note: Output will have no spaces after commas. Add post-processing if needed.

**All other tasks:** Use Qwen 1.7b baseline without modification.

---

## Channel Optimization Conclusions

**qwen3:8b is a high-performance tier-3 executor** that nearly matches qwen3:14b in baseline compatibility. One encoding fix needed: "plain text" modifier on reasoning answer anchor.

**Key differences from Qwen 1.7b baseline:**
- **Same encoding works** for 9/10 tasks — only reasoning output format needs "plain text" modifier
- **Correct case by default** — no "lowercase" constraint needed (same as qwen3:14b, better than qwen2.5-coder variants)
- **JSON compliance** — "no markdown fences" alone sufficient (same as deepseek-r1:8b)
- **Markdown bleed in reasoning** — output section in reasoning tasks uses bold styling; qwen3:14b does not have this issue
- **Comma spacing** — consistently omits spaces after commas in list outputs; minor cosmetic issue

**qwen3:8b vs. qwen3:14b:**
- 8b: one encoding fix needed (reasoning anchor), comma spacing cosmetic quirk
- 14b: zero fixes, cleaner output formatting
- 8b reasoning quality: surprisingly close to 14b (three-method verification in Task 005)
- At 8b: good value for capability; only slightly more encoding overhead than 14b

**qwen3:8b vs. deepseek-r1:8b:**
- Both: near-baseline compatibility, thinking mode, strong reasoning
- deepseek-r1:8b: zero adjustments, correct all tasks including reasoning format
- qwen3:8b: reasoning anchor fix needed; comma spacing issue
- deepseek-r1:8b slightly better baseline compliance at the 8b tier

**Recommendation for Sovereign:** Use qwen3:8b with "plain text" modifier on reasoning answer anchor. Excellent tier-3 executor with qwen3 thinking quality. Apply post-processing for comma spacing if needed. Prefer deepseek-r1:8b for zero-overhead baseline compatibility, or qwen3:14b for cleaner markdown-free output.
