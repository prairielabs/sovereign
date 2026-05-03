# Sovereign Channel Optimization — Final Result

**Run ID:** 20260428210500_ml-opt  
**Model:** gemma3:1b (via ollama)  
**Host:** workstation  
**Tasks:** 10 / 10 completed  
**Date:** 2026-04-28

---

## Results Summary

| Task | Type | Status | Encoding Used |
|------|------|--------|---------------|
| 001 | Extraction | ✅ SUCCESS | Baseline |
| 002 | Classification | ✅ SUCCESS | Adjusted — "exactly one lowercase word" |
| 003 | Sorting | ✅ SUCCESS | Baseline |
| 004 | Summarization | ✅ SUCCESS | Baseline |
| 005 | Reasoning | ✅ SUCCESS | Baseline — Answer: 10:48 AM (mathematically correct, full work shown) |
| 006 | Template Fill | ✅ SUCCESS | Baseline |
| 007 | Keyword Extraction | ✅ SUCCESS | Adjusted — "all lowercase" modifier |
| 008 | One-Word Answer | ✅ SUCCESS | Baseline |
| 009 | Structured JSON | ✅ SUCCESS | Adjusted — JSON few-shot template: provide example and ask model to confirm values |
| 010 | Logic | ✅ SUCCESS | Adjusted — "exactly one lowercase word" |

**Success rate: 10/10 (100%)**  
**Failure mode: Case defaults to sentence-case; JSON fencing persists through explicit suppression — requires few-shot template workaround**

---

## What Encoding Rules Produced Clean Output

### ✅ Reliable Patterns
- **"exactly one lowercase word"** — resolves capitalization on classification and logic tasks
- **"all lowercase" modifier** — resolves capitalized keyword lists
- **JSON few-shot template** — providing example JSON and asking for confirmation produces clean JSON without fences; verbal fence suppression alone fails for this model
- **All other baseline patterns** — extraction count, "nothing else", "[FIELD]" syntax, "Answer:" anchor — transfer cleanly

### 🔑 Special Pattern: JSON Few-Shot Template
```
{"name": "PLACEHOLDER", "age": 0, "active": false}

Confirm the above JSON for: name=[NAME], age=[AGE], active=[BOOL]. Output only the JSON object, starting with { :
```
This is the only reliable way to get clean JSON from gemma3:1b. Verbal suppression ("no backticks", "no markdown fences", "begin with {") all fail.

---

## What Failed

### ⚠️ Task 002, 007, 010 (Baseline)
Capitalization defaults. Fixed with "lowercase" / "all lowercase" constraints.

### ⚠️ Task 009 (Multiple retries — all failed except few-shot)
gemma3:1b consistently wraps JSON in ` ```json ``` ` code blocks regardless of verbal suppression. Attempts tried:
1. Baseline: "no markdown fences" → fences
2. Retry 1: "no backticks, no triple backticks" → still fences
3. Retry 2: "Begin your response with {" → still fences
4. Retry 3: Few-shot template with example JSON → ✅ SUCCESS

The model appears to have a strong learned association between JSON and code-block formatting that cannot be broken verbally. The few-shot approach bypasses this by making the output continuation pattern explicit.

---

## Model Behavior Observations
- **No thinking block** — direct output
- **1b tier reasoning** — surprisingly capable: Task 005 shows complete algebraic solution with correct answer (10:48 AM)
- **Sentence-case default** — persistent; "lowercase" constraint required on single-word answers
- **JSON fencing** — strong bias toward ` ```json ``` ` wrapping; verbal suppression ineffective; requires few-shot pattern
- **Template fill** — baseline works correctly without modification
- **Extraction/sort/summarize** — highly reliable at baseline
- **Factual recall** — correct (Au)
- **Logic** — correctly evaluates syllogism when lowercase constraint applied

---

## Optimized Encoding Pattern for gemma3:1b

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

**Structured JSON (few-shot template — verbal suppression fails):**
```
{"name": "PLACEHOLDER", "age": 0, "active": false}

Confirm the above JSON for: name=[NAME], age=[AGE], active=[BOOL]. Output only the JSON object, starting with { :
```

**Logic (add "lowercase"):**
```
Is this argument valid? Answer with exactly one lowercase word: valid or invalid.

Argument: [argument]
```

**All other tasks:** Use Qwen 1.7b baseline without modification.

---

## Channel Optimization Conclusions

**gemma3:1b is a capable tier-1 executor** with two systemic issues: capitalization defaults and JSON fence bias. Both are addressable with targeted encoding changes. The JSON few-shot approach is a significant departure from baseline and must be implemented at the Sovereign channel layer.

**Key differences from Qwen 1.7b baseline:**
- Case defaults require "lowercase" constraint on single-word outputs (same as gemma3:4b)
- JSON fence bias cannot be fixed verbally — requires few-shot template pattern; this is the biggest deviation from baseline
- Reasoning surprisingly capable for 1b tier — Task 005 algebraic solution correct with full working; significantly better than llama3.2:1b
- All other baseline patterns transfer cleanly

**Gemma3:1b vs. llama3.2:1b (both Tier 1):**
- gemma3:1b has stronger reasoning (correct train problem solution independently)
- gemma3:1b has JSON fence problem; llama3.2:1b does not
- llama3.2:1b has safety refusal on template fill; gemma3:1b does not
- gemma3:1b cannot evaluate logic (baseline); with lowercase fix, evaluates correctly
- Overall: gemma3:1b is more capable on reasoning tasks; llama3.2:1b has fewer encoding workarounds needed

**Recommendation for Sovereign:** Use gemma3:1b with three adjustments: (1) "lowercase" on single-word tasks, (2) "all lowercase" on keywords, (3) JSON few-shot template. Route JSON-heavy workflows to larger models if encoding overhead is undesirable.
