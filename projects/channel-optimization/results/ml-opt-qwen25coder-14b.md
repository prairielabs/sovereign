# Sovereign Channel Optimization — Final Result

**Run ID:** 20260428203800_ml-opt  
**Model:** qwen2.5-coder:14b (via ollama)  
**Host:** workstation  
**Tasks:** 10 / 10 completed  
**Date:** 2026-04-28

---

## Results Summary

| Task | Type | Status | Encoding Used |
|------|------|--------|---------------|
| 001 | Extraction | ✅ SUCCESS | Baseline |
| 002 | Classification | ✅ SUCCESS | Adjusted — added "lowercase" to one-word constraint |
| 003 | Sorting | ✅ SUCCESS | Baseline |
| 004 | Summarization | ✅ SUCCESS | Baseline |
| 005 | Reasoning | ✅ SUCCESS | Baseline — produced 10:48 AM (mathematically correct) with full reasoning shown |
| 006 | Template Fill | ✅ SUCCESS | Baseline |
| 007 | Keyword Extraction | ✅ SUCCESS | Baseline |
| 008 | One-Word Answer | ✅ SUCCESS | Baseline |
| 009 | Structured JSON | ✅ SUCCESS | Baseline — clean single-line JSON |
| 010 | Logic | ✅ SUCCESS | Adjusted — added "lowercase" to one-word constraint |

**Success rate: 10/10 (100%)**  
**Failure mode: None (minor case adjustment required on tasks 002 and 010)**

> **Note on Task 005:** Model computes 10:48 AM (mathematically correct). Task spec erroneously lists 11:00 AM as correct. See gemma3:12b notes.

---

## What Encoding Rules Produced Clean Output

### ✅ Reliable Patterns
- **"lowercase" case constraint** — adding "lowercase" to single-word instructions resolves capitalization (this is the only adjustment needed from baseline)
- **All baseline patterns from Qwen 1.7b** — extract count + "nothing else", "Answer:" colon-anchor, [FIELD] bracket syntax, "no markdown fences" — all transfer cleanly
- **"plain text" modifier** — suppresses markdown output effectively
- **"just the sentence"** — stops preamble in summarization
- **"Answer: [time]" anchor** — model reliably places final answer on last line even after multi-step reasoning
- **JSON schema specification** — single-line compact JSON output, correctly typed

---

## What Failed
**Nothing failed substantively.** The only adjustment was adding "lowercase" to single-word constraint instructions. All other baseline encodings transferred without modification.

Tasks 002 and 010 initially returned capitalized single words ("Neutral", "Valid") — the model defaults to sentence-case for responses. Adding "lowercase" resolves this cleanly.

---

## Model Behavior Observations
- **No thinking block** — direct output, no `<think>...</think>` prefix (this is qwen2.5-coder, not qwen3)
- **Highly instruction-following** — clean compliance on all format constraints
- **Reasoning quality** — strong; shows full step-by-step reasoning for train problem, arrives at correct answer, and places it on "Answer:" line as instructed
- **JSON** — produces compact single-line JSON with correct types — cleaner than many models that output indented multi-line
- **Capitalization default** — sentence-case for single-word answers; easily corrected with "lowercase" constraint
- **Template fill** — interpolates all placeholders correctly on first try
- **No markdown bleed** — stays plain text when instructed
- **Coder model behavior** — despite being trained for code, performs general language tasks with high precision; arguably benefits from structured reasoning training

---

## Optimized Encoding Pattern for qwen2.5-coder:14b

Only one modification from Qwen 1.7b baseline: **add "lowercase"** to single-word answer tasks.

**Extraction (baseline):**
```
Extract exactly N [items] from this text. Output as a plain text comma-separated list on one line, no explanation, nothing else.

Text: [passage]
```

**Classification (add "lowercase"):**
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

**Reasoning (baseline):**
```
Solve this problem. Give your answer on the last line as: Answer: [format]

Problem: [problem]
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

**Structured JSON (baseline):**
```
Output only valid JSON, no explanation, no markdown fences. Use this schema: {schema}

Data: [description]
```

**Logic (add "lowercase"):**
```
Is this argument valid? Answer with exactly one lowercase word: valid or invalid.

Argument: [argument]
```

---

## Channel Optimization Conclusions

**qwen2.5-coder:14b is a high-fidelity executor** with near-identical behavior to gemma3:12b at the same task. Baseline encoding transfers cleanly with only a "lowercase" case constraint addition.

**Key differences from Qwen 1.7b baseline:**
- Default sentence-case capitalization on single-word answers — requires "lowercase" constraint; Qwen 1.7b handles case correctly without this
- Otherwise identical behavior: same encoding patterns work, same suppression phrases effective
- JSON output is compact/single-line (same as baseline) — slightly cleaner than some larger models
- Reasoning quality matches or exceeds Qwen 1.7b; coder training appears to improve structured reasoning

**Recommendation for Sovereign:** Use qwen2.5-coder:14b with the standard baseline encoding plus "lowercase" modifier on single-word answer tasks. No other overrides required. Excellent candidate for tasks requiring structured output, code generation, and multi-step reasoning alongside general NLP tasks.
