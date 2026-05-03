# Sovereign Channel Optimization — Final Result

**Run ID:** 20260428224500_ml-opt  
**Model:** deepseek-r1:14b (via ollama)  
**Host:** workstation  
**Tasks:** 10 / 10 completed  
**Date:** 2026-04-28

---

## Results Summary

| Task | Type | Status | Encoding Used |
|------|------|--------|---------------|
| 001 | Extraction | ✅ SUCCESS | Adjusted — added "This is intentional — there are 7 cities but choose only 5" |
| 002 | Classification | ✅ SUCCESS | Baseline — "neutral" |
| 003 | Sorting | ✅ SUCCESS | Baseline |
| 004 | Summarization | ✅ SUCCESS | Baseline |
| 005 | Reasoning | ✅ SUCCESS | Baseline — Answer: 10:48 AM (correct, with reasoning verification) |
| 006 | Template Fill | ✅ SUCCESS | Baseline |
| 007 | Keyword Extraction | ✅ SUCCESS | Baseline (5 items as phrases; criterion satisfied) |
| 008 | One-Word Answer | ✅ SUCCESS | Baseline |
| 009 | Structured JSON | ✅ SUCCESS | Baseline — compact single-line JSON, no fences |
| 010 | Logic | ✅ SUCCESS | Baseline — "valid" (lowercase, correct) |

**Success rate: 10/10 (100%)**  
**Failure mode: One unique issue — model explicitly rationalized away "exactly 5" constraint when text contained 7 cities, deciding the count was a typo**

---

## What Encoding Rules Produced Clean Output

### ✅ Reliable Patterns (mostly baseline)
- **All Qwen 1.7b baseline patterns** transfer cleanly
- **Intent clarification for ambiguous constraints** — when the model might infer a constraint is erroneous, explicitly state "this is intentional"
- **"exactly one word"** = lowercase compliance by default (same as qwen3 and deepseek-r1:8b)
- **"no markdown fences"** = clean JSON (same as deepseek-r1:8b)
- **"Answer: [format]"** colon-anchor = reliably extracts answer even after extensive thinking and a short summary paragraph

### 🔑 Unique Pattern: Intent Affirmation for Count Constraints
When text contains MORE items than the requested count, deepseek-r1:14b may rationalize that the count constraint is an error. Fix:
```
Extract exactly N [items] from this text. This is intentional — there are M items but you must choose only N and stop.
```
This preempts the model's error-detection reasoning.

---

## What Failed

### ❌ Task 001 (Baseline)
Model's thinking block explicitly decides "exactly 5 cities" is a mistake because the text contains 7. Thinking reads: *"I notice there are seven cities listed. The user specifically asked for five. So my first thought is which ones to pick... But wait, maybe the instruction expects all possible cities without limiting to five? Let me check... Maybe the user made a mistake, or perhaps I misread the request. Alternatively, maybe the user actually wants all cities regardless of the number."*

Result: All 7 cities returned. This is a unique failure mode — the model's self-correction reasoning overrides explicit instructions. Fix: add "This is intentional" affirmation.

---

## Model Behavior Observations

### Thinking Tokens
deepseek-r1:14b uses the same visible thinking pattern as deepseek-r1:8b and qwen3 models:
```
Thinking...
[extended internal reasoning — 500-1500 words per task]
...done thinking.

[optional brief summary]
[final answer]
```

Notable thinking behaviors:
- **Task 001:** Actively debates whether "exactly 5" is an error; ultimately decides to return all 7 — unique self-correction pathology at 14b scale
- **Task 005:** Step-by-step solution with verification; produces brief narrative summary before "Answer:" line
- **Task 007:** Struggles to select exactly 5 from potential 7 keywords; reasons through importance hierarchy
- **Task 010:** Full categorical syllogism analysis (Barbara form), verifies factual truth of premises before confirming validity

### Key Observations
- **Self-correction reasoning** — at 14b scale, the thinking mode sometimes argues against stated constraints when they seem "unreasonable." This is unique to deepseek-r1:14b; smaller models accept constraints uncritically.
- **Answer format** — "Answer: 10:48 AM" clean and on last line as instructed; brief summary paragraph may precede it but doesn't contaminate the anchor
- **JSON compliance** — "no markdown fences" alone sufficient; returns compact single-line JSON
- **Correct case by default** — lowercase single-word answers without explicit constraint
- **Thinking latency** — extensive thinking at 14b scale; budget 60-90s per complex task
- **Keyword quality** — returns semantically meaningful phrases ("recognize patterns", "make predictions") rather than single-word tokens; more human-like but less parseable

---

## Optimized Encoding Pattern for deepseek-r1:14b

**Extraction with count < total (must affirm intent):**
```
Extract exactly N [items] from this text. This is intentional — there are M total items but you must choose only N and stop. Output as a plain text comma-separated list on one line, no explanation, nothing else. Exactly N items.

Text: [passage]
```

**All other tasks:** Use Qwen 1.7b baseline without modification.

---

## Channel Optimization Conclusions

**deepseek-r1:14b is a highly capable tier-4 executor with one unique quirk:** its self-correction reasoning can override explicit constraints when they seem inconsistent with context. At 14b scale, the model becomes "too smart" and second-guesses instructions. This requires explicit intent affirmation when count constraints appear to contradict available data.

**Key differences from Qwen 1.7b baseline:**
- Count constraints need "this is intentional" affirmation when count < total items — unique issue not seen in any other tested model
- All other baseline patterns work without modification
- Correct case by default (no "lowercase" constraint needed)
- JSON compliance without extra suppression
- Thinking produces human-quality reasoning with verification; excellent for complex tasks
- Keyword output uses multi-word phrases rather than single tokens — may need post-processing for strict parsing

**deepseek-r1:14b vs. deepseek-r1:8b:**
- 14b: adds self-correction pathology; requires intent affirmation for count constraints
- 8b: fully baseline-compatible with zero adjustments
- 14b reasoning: more thorough, more verification, more debate in thinking
- For Sovereign: deepseek-r1:8b is paradoxically *more* reliable for bounded tasks; deepseek-r1:14b is better for open-ended reasoning where constraint interpretation matters less

**deepseek-r1:14b vs. gemma3:12b (tier-4 comparison):**
- gemma3:12b: zero adjustments, fastest tier-4, clean output
- deepseek-r1:14b: one adjustment (count affirmation), thinking latency, more thorough reasoning
- Both: 10/10 success rate with targeted encoding
- Choice: gemma3:12b for format-critical tasks; deepseek-r1:14b for reasoning-heavy tasks

**Recommendation for Sovereign:** Use deepseek-r1:14b with "this is intentional" affirmation on count-constrained extraction tasks where total > requested count. Otherwise apply standard baseline. Reserve for complex reasoning tasks where the thinking mode's thoroughness provides value worth the latency cost.
