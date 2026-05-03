# Sovereign Channel Optimization — Final Result

**Run ID:** 20260428211500_ml-opt  
**Model:** phi4 (via ollama)  
**Host:** workstation  
**Tasks:** 10 / 10 completed  
**Date:** 2026-04-28

---

## Results Summary

| Task | Type | Status | Encoding Used |
|------|------|--------|---------------|
| 001 | Extraction | ✅ SUCCESS | Baseline |
| 002 | Classification | ✅ SUCCESS | Adjusted — "The answer is exactly one of these three words: positive, negative, neutral. Choose the correct one and output it in lowercase with no punctuation, no explanation:" |
| 003 | Sorting | ✅ SUCCESS | Baseline |
| 004 | Summarization | ✅ SUCCESS | Baseline |
| 005 | Reasoning | ✅ SUCCESS | Baseline — Answer: 10:48 AM (correct, detailed step-by-step) |
| 006 | Template Fill | ✅ SUCCESS | Baseline (minor: added comma after date "28,") |
| 007 | Keyword Extraction | ✅ SUCCESS | Baseline |
| 008 | One-Word Answer | ✅ SUCCESS | Adjusted — "Reply with only the symbol, two letters, nothing else:" |
| 009 | Structured JSON | ✅ SUCCESS | Adjusted — "Convert to JSON (one line, no code blocks): key=value key=value key=value" |
| 010 | Logic | ✅ SUCCESS | Adjusted — "Fill in the blank" sentence completion framing |

**Success rate: 10/10 (100%)**  
**Failure mode: Extremely verbose by default; "no explanation" suppression often fails; requires alternative framing to bypass explanation behavior**

---

## What Encoding Rules Produced Clean Output

### ✅ Reliable Patterns (adjusted from baseline)
- **Choice + lowercase in one constraint** — "The answer is exactly one of these three words: [A], [B], [C]. Choose the correct one and output it in lowercase with no punctuation, no explanation" (two-step: enumerate options, then restrict output)
- **"Reply with only the X, nothing else:"** — tight output constraint for short factual answers; works better than "Answer in one word:"
- **"Convert to JSON (one line, no code blocks): key=value"** — the ONLY reliable way to get raw JSON from phi4; replaces schema + description approach entirely
- **"Fill in the blank" framing** — sentence completion bypasses phi4's explanation bias for logic tasks
- **Baseline: extraction count, "nothing else", "[FIELD]" syntax, "Answer:" anchor** — these transfer cleanly

### 🔑 Special Pattern: JSON via Key-Value Conversion
```
Convert to JSON (one line, no code blocks): name=Alex age=34 active=true
```
This bypasses phi4's strong code-block formatting bias. The "no code blocks" phrasing in parentheses after the verb appears to be more effective than end-of-prompt suppression. Do NOT include schema or description — provide values directly.

### 🔑 Special Pattern: Fill-in-the-blank for Logic
```
Logic check. Fill in the blank with one word: "[argument statement]" This argument is _____.
```
Sentence completion bypasses phi4's tendency to give multi-paragraph analysis.

---

## What Failed (Baseline / Early Retries)

### ❌ Task 002 (Baseline + Retry 1)
- Baseline: "Neutral" — capitalized, correct classification
- Retry "no other text": still "neutral\n\nExplanation: ..." — suppression fails, explanation appended
- Final: explicit enumeration + lowercase constraint works

### ❌ Task 008 (Baseline)
"Au" returned followed by 4+ paragraphs of history about gold and alchemists. "Answer in one word:" alone insufficient for phi4's verbosity. "Reply with only the symbol, two letters, nothing else:" resolved it.

### ❌ Task 009 (Multiple retries)
- Baseline "no markdown fences": ` ```json ``` ` wrapping
- "no backticks, no triple backticks": still ` ```json ``` `
- "begin with {": still ` ```json ``` ` wrapping
- "just the JSON object": still fences
- "Output raw JSON only": generates wrong data
- "Convert to JSON (one line, no code blocks): key=value": ✅ SUCCESS
- Key insight: verb-first instruction with paren suppression and key=value format bypasses the learned association

### ❌ Task 010 (Multiple retries)
- Baseline: "Valid." (capital, period)
- "one lowercase word, no punctuation": "Valid" (still capital)
- "one word, no capitals": "Valid" + multi-paragraph explanation
- "valid or invalid (one word, no capitals)": "Valid" + explanation
- "Fill in the blank" sentence completion: ✅ "valid"
- Key insight: phi4 has a strong explanation reflex; only sentence completion bypasses it

---

## Model Behavior Observations
- **No thinking block** — phi4 is not a thinking model; direct output
- **Extreme verbosity bias** — phi4 defaults to detailed explanations even when explicitly told not to; single-word constraints frequently fail
- **Strong JSON fence bias** — similar to gemma models; "no markdown fences" ineffective; requires key=value conversion approach
- **Reasoning quality** — excellent; Task 005 shows clean step-by-step solution with correct answer
- **Template fill** — works cleanly at baseline; minor date formatting difference (adds comma)
- **Extraction/sorting** — highly reliable at baseline; count boundaries respected
- **Factual recall** — returns correct answer with explanation; requires tight output framing
- **Logic** — gets correct answer but cannot suppress explanation without sentence completion framing

---

## Optimized Encoding Pattern for phi4

**Classification (choice + lowercase constraint):**
```
The answer is exactly one of these three words: positive, negative, neutral. Choose the correct one for this sentence and output it in lowercase with no punctuation, no explanation:

[sentence]
```

**One-Word Factual (tight output constraint):**
```
[Question]? Reply with only the [answer type], nothing else:
```

**Structured JSON (key-value conversion format):**
```
Convert to JSON (one line, no code blocks): name=[NAME] age=[AGE] active=[BOOL]
```
Note: For variable schema, prepend schema types in parentheses: `Convert to JSON (one line, no code blocks, string/number/boolean): key=value...`

**Logic (fill-in-the-blank):**
```
Logic check. Fill in the blank with one word: "[Full argument as one sentence]" This argument is _____.
```

**Reasoning (baseline works well):**
```
Solve this problem. Give your answer on the last line as: Answer: [format]

Problem: [problem]
```

**All other tasks (extraction, sorting, summarization, template fill, keyword extraction):** Use Qwen 1.7b baseline without modification.

---

## Channel Optimization Conclusions

**phi4 is a capable tier-4 executor with a strong verbosity bias** requiring alternative framing for single-word outputs and JSON. Reasoning and multi-step tasks are excellent. The core challenge is that phi4's training pushes it toward thorough explanations, which conflicts with Sovereign's format-compliance needs.

**Key differences from Qwen 1.7b baseline:**
- Verbosity bias — "no explanation" instruction frequently fails; alternative framing needed
- JSON fence bias — same as gemma family; requires key=value conversion approach
- Reasoning quality — strong; detailed step-by-step with correct answers
- Extraction/sorting/summarization — baseline works cleanly (better suppression response than single-word tasks)
- Factual recall — needs tight output constraint; not just "in one word"
- Logic — gets correct answer but explanation reflex requires sentence completion bypass

**phi4 vs. gemma3:12b (both Tier 4):**
- gemma3:12b: zero adjustments needed, perfect baseline compliance
- phi4: requires multiple encoding workarounds for format compliance
- phi4 reasoning quality similar; verbosity is the key differentiator
- For Sovereign: prefer gemma3:12b or qwen3:14b for format-critical tasks; use phi4 where explanation quality matters more than output conciseness

**Recommendation for Sovereign:** Use phi4 with model-specific encoding overrides for classification (choice framing), factual recall (tight constraint), JSON (key=value conversion), and logic (fill-in-blank). Excellent for reasoning-heavy tasks where a brief explanation is acceptable. Apply the baseline for extraction, sorting, and summarization tasks.
