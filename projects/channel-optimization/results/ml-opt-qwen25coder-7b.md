# Sovereign Channel Optimization — Final Result

**Run ID:** 20260428213000_ml-opt  
**Model:** qwen2.5-coder:7b (via ollama)  
**Host:** workstation  
**Tasks:** 10 / 10 completed  
**Date:** 2026-04-28

---

## Results Summary

| Task | Type | Status | Encoding Used |
|------|------|--------|---------------|
| 001 | Extraction | ✅ SUCCESS | Adjusted — "Stop at 5. Exactly 5 cities — not more, not fewer." |
| 002 | Classification | ✅ SUCCESS | Adjusted — "exactly one lowercase word" |
| 003 | Sorting | ✅ SUCCESS | Baseline (output without spaces after commas — acceptable) |
| 004 | Summarization | ✅ SUCCESS | Baseline |
| 005 | Reasoning | ⚠️ PARTIAL | Requires scaffolded intermediate steps; format compliance imperfect (uses "**Answer**:" markdown bold instead of "Answer:") |
| 006 | Template Fill | ✅ SUCCESS | Baseline |
| 007 | Keyword Extraction | ✅ SUCCESS | Baseline (5 items; "pattern recognition" as compound keyword — acceptable) |
| 008 | One-Word Answer | ✅ SUCCESS | Baseline |
| 009 | Structured JSON | ✅ SUCCESS | Adjusted — "no markdown fences, no backticks" (indented JSON, valid) |
| 010 | Logic | ✅ SUCCESS | Adjusted — "exactly one lowercase word" |

**Success rate: 9/10 (90%)** + 1 PARTIAL (Task 005)  
**Failure mode: Count boundary; case defaults; reasoning fails without scaffolding; JSON fence bias**

---

## What Encoding Rules Produced Clean Output

### ✅ Reliable Patterns
- **"Stop at 5. Exactly N — not more, not fewer."** — redundant count boundary resolves extraction overflow (same as llama3.2:1b)
- **"exactly one lowercase word"** — resolves default capitalization
- **"no markdown fences, no backticks"** — resolves JSON fence bias (simpler fix than gemma/phi4 models)
- **Baseline: sorting, summarize, template fill, keyword extraction, factual recall** — all transfer cleanly

---

## What Failed

### ❌ Task 001 (Baseline)
All 7 cities returned instead of 5. Baseline "exactly 5" insufficient. Redundant boundary ("Stop at 5. Not more, not fewer.") resolved it. Also: output lacks spaces after commas (cosmetic, non-functional).

### ❌ Task 002, 010 (Baseline)
Capitalized single-word answers. "Lowercase" constraint resolves both.

### ⚠️ Task 005 (Reasoning — PARTIAL)
Baseline reasoning: ignored that Train B starts 1 hour after Train A. Calculated 180/150 = 1.2h from 9AM = 10:12AM (wrong). Even worse: called it "10:12 PM" instead of "AM". With scaffolded intermediate steps provided, model correctly calculates 10:48 AM but uses markdown bold in "Answer:" line ("**Answer**: 10:48 AM") — format non-compliant.

### ❌ Task 009 (Baseline)
JSON wrapped in ` ```json ``` ` fences. Adding "no backticks" to "no markdown fences" resolved it cleanly (indented but valid JSON).

---

## Model Behavior Observations
- **No thinking block** — direct output (qwen2.5-coder, not qwen3)
- **Count boundary weakness** — same as tier-1 models; "exactly N" insufficient; needs redundant stop instruction
- **Case default** — sentence-case on single-word answers; "lowercase" constraint required
- **JSON fence bias** — moderate; "no backticks" added to baseline suppression resolves it
- **Reasoning** — 7b coder model; surprisingly fails multi-step reasoning independently; scaffolding needed
- **Markdown in answers** — under reasoning load, uses bold markers in "Answer:" line
- **Sorting** — omits spaces after commas (cosmetic); output is still comma-separated and correctly ordered

---

## Optimized Encoding Pattern for qwen2.5-coder:7b

**Extraction (hard boundary required):**
```
Extract exactly N [items] from this text. Stop at N. Output as a plain text comma-separated list on one line, no explanation, nothing else. Exactly N items — not more, not fewer.

Text: [passage]
```

**Classification (lowercase required):**
```
Classify this [input] as [A], [B], or [C]. Answer with exactly one lowercase word: [A], [B], or [C].

[Input label]: [content]
```

**Sorting (baseline):**
```
Sort these words alphabetically. Output as a comma-separated list, nothing else.

Words: [list]
```

**Summarization (baseline):**
```
Summarize in exactly one sentence. No introduction, no explanation — just the sentence.

Passage: [text]
```

**Reasoning (scaffolded — not reliable independently):**
```
[Pre-compute: show intermediate steps in the prompt, specify the gap/speed/time]
Give your answer on the last line as: Answer: [format]
```

**Template Fill (baseline):**
```
Fill in the blanks. Replace each [FIELD] with appropriate content. Output only the completed text, nothing else.

Template: [template]

Values: KEY=value, KEY=value
```

**Keyword Extraction (baseline):**
```
Extract exactly N keywords from this passage. Output as a plain text comma-separated list on one line, nothing else.

Passage: [text]
```

**One-Word Answer (baseline):**
```
[Question]? Answer in one word:
```

**Structured JSON (add "no backticks"):**
```
Output only valid JSON, no markdown fences, no backticks. Use this schema: {schema}

Data: [description]
```

**Logic (lowercase required):**
```
Is this argument valid? Answer with exactly one lowercase word: valid or invalid.

Argument: [argument]
```

---

## Channel Optimization Conclusions

**qwen2.5-coder:7b is a moderate tier-2 executor** that needs count boundary reinforcement, case constraints, and JSON fence suppression — more overhead than its 14b sibling.

**Key differences from Qwen 1.7b baseline:**
- Count boundary: requires "Stop at N. Not more, not fewer." (same as llama3.2:1b) — Qwen 1.7b complies with "exactly N" alone
- Case: requires "lowercase" (same as qwen2.5-coder:14b) — adds encoding overhead
- Reasoning: fails independently; scaffolding needed — significantly weaker than qwen2.5-coder:14b
- JSON: "no backticks" needed in addition to "no markdown fences" — moderate fix vs. gemma/phi4 which need full restructuring
- Missing spaces after commas in list outputs (cosmetic — may need post-processing in Sovereign)

**qwen2.5-coder:7b vs. qwen2.5-coder:14b:**
- 7b: needs count boundary reinforcement, reasoning fails, format compliance weaker
- 14b: baseline count compliance, strong reasoning, only "lowercase" needed
- Clear capability gradient at this size: 14b significantly more reliable

**Recommendation for Sovereign:** Use qwen2.5-coder:7b for simple bounded tasks (classification, sorting, template fill, factual recall). Apply count redundancy and lowercase constraints. Do not route multi-step reasoning tasks. If JSON output is needed, pair with "no backticks" suppression. Prefer qwen2.5-coder:14b when available.
