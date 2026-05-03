# Sovereign Channel Optimization — Final Result

**Run ID:** 20260428205500_ml-opt  
**Model:** gemma3:4b (via ollama)  
**Host:** workstation  
**Tasks:** 10 / 10 completed  
**Date:** 2026-04-28

---

## Results Summary

| Task | Type | Status | Encoding Used |
|------|------|--------|---------------|
| 001 | Extraction | ✅ SUCCESS | Baseline |
| 002 | Classification | ✅ SUCCESS | Adjusted — added "lowercase" |
| 003 | Sorting | ✅ SUCCESS | Baseline |
| 004 | Summarization | ✅ SUCCESS | Baseline |
| 005 | Reasoning | ✅ SUCCESS | Baseline — Answer: 10:48 AM (correct, full verification) |
| 006 | Template Fill | ✅ SUCCESS | Baseline |
| 007 | Keyword Extraction | ✅ SUCCESS | Adjusted — added "all lowercase" modifier |
| 008 | One-Word Answer | ✅ SUCCESS | Baseline |
| 009 | Structured JSON | ✅ SUCCESS | Adjusted — "no backticks, no triple backticks" added |
| 010 | Logic | ✅ SUCCESS | Baseline — "valid" (lowercase, correct) |

**Success rate: 10/10 (100%)**  
**Failure mode: Case defaults to sentence-case; JSON wraps in markdown fences without stronger suppression**

---

## What Encoding Rules Produced Clean Output

### ✅ Reliable Patterns
- **"lowercase"** — resolves sentence-case defaults on single-word classification answers
- **"all lowercase"** — resolves capitalized keyword lists (e.g., "Machine learning" → "machine learning")
- **"no backticks, no triple backticks"** — suppresses JSON markdown fencing (adds to "no markdown fences")
- **All other baseline patterns** — extraction count, "nothing else", "[FIELD]" syntax, "Answer:" anchor, "just the sentence" — all transfer cleanly

---

## What Failed

### ⚠️ Task 002 (Baseline)
Returned "Neutral" — capital N. Adding "lowercase" resolved it cleanly.

### ⚠️ Task 007 (Baseline)
Returned "Machine learning, datasets, patterns, predictions, neural networks" — "Machine" capitalized at list start. Adding "all lowercase" resolved it.

### ⚠️ Task 009 (Baseline)
Returned JSON wrapped in ` ```json ``` ` code block despite "no markdown fences" instruction. More explicit suppression ("no backticks, no triple backticks") resolved it to clean raw JSON.

---

## Model Behavior Observations
- **No thinking block** — direct output, no chain-of-thought prefix
- **Sentence-case default** — starts lists and single-word answers with capital letters; needs lowercase constraint
- **JSON markdown fencing** — "no markdown fences" alone insufficient; requires explicit "no backticks" language for this model
- **Reasoning** — Task 005 shows strong step-by-step reasoning with verification; "Answer:" anchor reliably extracts the final result
- **Template fill** — baseline works perfectly on first try
- **Sorting, factual recall** — highly reliable, no adjustments needed
- **Logic** — correctly evaluates valid syllogism as "valid" at baseline (lowercase, no issues)

---

## Optimized Encoding Pattern for gemma3:4b

**Classification (add "lowercase"):**
```
Classify this [input] as [A], [B], or [C]. Answer with exactly one lowercase word: [A], [B], or [C].

[Input label]: [content]
```

**Keyword Extraction (add "all lowercase"):**
```
Extract exactly N keywords from this passage. Output as a plain text comma-separated list on one line, all lowercase, nothing else.

Passage: [text]
```

**Structured JSON (add explicit backtick suppression):**
```
Output only valid JSON with no markdown code fences, no backticks, no triple backticks. Raw JSON only. Use this schema: {schema}

Data: [description]
```

**All other tasks:** Use Qwen 1.7b baseline without modification.

---

## Channel Optimization Conclusions

**gemma3:4b is a high-performing tier-3 executor** requiring minimal encoding adjustments. Three targeted fixes resolve all issues: lowercase constraint on single-word answers, "all lowercase" on keyword lists, and explicit backtick suppression on JSON.

**Key differences from Qwen 1.7b baseline:**
- Default sentence-case capitalization — "lowercase" constraint needed (similar to qwen2.5-coder:14b)
- JSON markdown fencing — requires stronger suppression than baseline "no markdown fences"; add "no backticks, no triple backticks"
- Reasoning quality strong for 4b tier — matches tier-4 pattern with full solution verification
- All other baseline patterns transfer without change

**Recommendation for Sovereign:** Use gemma3:4b with three targeted encoding adjustments: (1) "lowercase" on classification and logic tasks, (2) "all lowercase" on keyword extraction, (3) "no backticks" on JSON tasks. Excellent tier-3 executor for general NLP.
