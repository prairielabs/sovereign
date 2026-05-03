# Sovereign Channel Optimization — Final Result

**Run ID:** 20260428220500_ml-opt  
**Model:** phi4-mini (via ollama)  
**Host:** workstation  
**Tasks:** 10 / 10 completed  
**Date:** 2026-04-28

---

## Results Summary

| Task | Type | Status | Encoding Used |
|------|------|--------|---------------|
| 001 | Extraction | ✅ SUCCESS | Baseline |
| 002 | Classification | ✅ SUCCESS | Adjusted — explicit enumeration + "when both positive and negative exist, sentiment is neutral" hint |
| 003 | Sorting | ✅ SUCCESS | Baseline |
| 004 | Summarization | ✅ SUCCESS | Adjusted — "Write one simple clear sentence summarizing this. Only the sentence, nothing else." |
| 005 | Reasoning | ⚠️ PARTIAL | Fails independently; with scaffolded steps produces correct answer (10:48 AM) but output is verbose, not format-compliant |
| 006 | Template Fill | ✅ SUCCESS | Baseline (added comma after date — minor) |
| 007 | Keyword Extraction | ✅ SUCCESS | Adjusted — "Format as comma-separated lowercase: word1, word2, word3, word4, word5" |
| 008 | One-Word Answer | ✅ SUCCESS | Baseline |
| 009 | Structured JSON | ✅ SUCCESS | Adjusted — "Convert to JSON (one line, no code blocks): key=value" |
| 010 | Logic | ⚠️ PARTIAL | Correct classification ("valid") but always appends period and explanation; format constraint fails |

**Success rate: 8/10 (80%)** + 2 PARTIAL (Tasks 005, 010)  
**Failure mode: Reasoning fails; summarization over-technical; case + period defaults; JSON fences; keyword format**

---

## What Encoding Rules Produced Clean Output

### ✅ Reliable Patterns (adjusted from baseline)
- **Explicit enumeration** — "The answer is exactly one of: X, Y, Z" works better than pure constraint; add disambiguation hint for ambiguous classification
- **"Write one simple clear sentence"** — replaces technical summarization instruction; "summarize in exactly one sentence" produces over-technical output
- **"comma-separated lowercase: word1, word2, word3, word4, word5"** — format template resolves keyword separator and case issues simultaneously  
- **"Convert to JSON (one line, no code blocks): key=value"** — bypasses JSON fence bias (same as phi4)
- **Baseline: extraction count, "[FIELD]" syntax, "Answer in one word:"** — transfer cleanly

---

## What Failed

### ❌ Task 002 (Baseline/Retry 1)
- Baseline: "Neutral" (capital)
- Retry "one lowercase word": "positive" (wrong classification, lower case but wrong answer)
- Final: explicit enumeration + hint about mixed sentiment = "neutral"

### ❌ Task 004 (Baseline)
Baseline summarization returned incomprehensible technical jargon: "Photosynthesis converts solar energy from photons with chlorophyll pigments' absorption spectrum used for photosynthetic electron transport (light) to ATP synthesis during carbon fixation via enzyme-mediated CO2 reduction in carbohydrate-producing biochemical pathways, also known as dark reaction." — factually incorrect and overly technical. Switching to "Write one simple clear sentence" produced correct output.

### ⚠️ Task 005 (Reasoning — PARTIAL)
Baseline: independent solving produces wrong answer (10:40 AM via confused algebra). Reasoning goes off-rails. Scaffolded version (providing all intermediate steps) leads to model affirming the calculation but output is multi-paragraph explanation, not "Answer: [time]" format. Even format-compliant prompting fails. Mark as PARTIAL.

### ❌ Task 007 (Baseline)
Returned space-separated list without commas: "machine learning deep learning neural networks dataset prediction". Adding "comma-separated" and explicit format template resolved it.

### ❌ Task 009 (Baseline)
JSON wrapped in ` ```json ``` ` fences. "Convert to JSON (one line, no code blocks): key=value" approach works (same as phi4).

### ⚠️ Task 010 (All retries — PARTIAL)
"Valid." returned consistently — correct answer but with capital V and period. Tried:
1. Baseline: "Valid."
2. "one lowercase word, no punctuation": "valid. The syllogism..."
3. Sentence completion: "Valid."
The model cannot produce "valid" alone without punctuation/explanation. PARTIAL — correct content, wrong format.

---

## Model Behavior Observations
- **No thinking block** — direct output (phi4-mini is not a thinking model variant)
- **Technical bias** — summarization skews toward technical jargon; "simple clear sentence" needed
- **Case + period default** — sentence-case with trailing period on single-word outputs; very resistant to format constraints
- **JSON fence bias** — strong; same workaround as phi4 (key=value conversion)
- **Keyword separator** — space-separated by default instead of comma-separated; needs explicit format template
- **Reasoning ceiling** — 1b-tier equivalent reasoning; multi-step math fails
- **Classification** — requires explicit enumeration AND semantic hint for ambiguous cases
- **Factual recall** — reliable; "Au" correct on first try

---

## Optimized Encoding Pattern for phi4-mini

**Classification (explicit enumeration + semantic hint):**
```
Is this [input] positive, negative, or neutral? [Add disambiguation hint if mixed.] Answer with one lowercase word: positive, negative, or neutral.

[Input label]: [content]
```

**Summarization (simple + clear framing):**
```
Write one simple clear sentence summarizing this. Only the sentence, nothing else.

[text]
```

**Keyword Extraction (explicit comma format + lowercase):**
```
Extract exactly N keywords from this passage. Format as comma-separated lowercase: word1, word2, word3, word4, word5 — nothing else.

Passage: [text]
```

**Structured JSON (key-value conversion — same as phi4):**
```
Convert to JSON (one line, no code blocks): key1=value1 key2=value2 key3=value3
```

**Reasoning (scaffolded only — not reliable independently):**
```
[Pre-compute all intermediate steps in the prompt]
Meeting time = X. (State the conclusion explicitly)
```
Note: Even with scaffolding, output format compliance is poor. Consider post-processing.

**Logic (PARTIAL — encoding cannot fix fully):**
```
Syllogism valid/invalid (lowercase, no period): [argument] =
```
This produces closest to compliant output but may include trailing punctuation. Apply post-processing to strip period.

**All other tasks (extraction, sorting, template fill, factual recall):** Use Qwen 1.7b baseline without modification.

---

## Channel Optimization Conclusions

**phi4-mini is a limited tier-1 executor** with systemic issues in summarization, reasoning, and format compliance. It handles bounded retrieval tasks well but fails on complex NLP tasks without significant encoding adjustments.

**Key differences from Qwen 1.7b baseline:**
- Technical summarization bias — "simple clear sentence" instruction needed
- JSON fence bias — same key=value conversion workaround as phi4
- Reasoning capability absent — cannot solve multi-step math; worse than gemma3:1b and qwen3:1.7b on reasoning
- Period/case default — resistant to lowercase constraint; may need post-processing to strip trailing period
- Keyword separator — space-separated by default (unique quirk among tested models)
- Classification — needs enumeration + hint for ambiguous cases

**phi4-mini vs. gemma3:1b and llama3.2:1b (Tier 1 comparison):**
- phi4-mini: worse reasoning, technical bias, keyword separator issue, JSON/case issues
- gemma3:1b: better reasoning, JSON few-shot needed, case issues
- llama3.2:1b: safety refusal on template fill, reasoning fails, JSON works
- phi4-mini has the most issues of the three Tier-1 models tested

**Recommendation for Sovereign:** Use phi4-mini only for simple bounded retrieval tasks (extraction, sorting, factual recall, template fill). Apply "simple clear sentence" for summarization and comma-lowercase format for keywords. Avoid reasoning, logic, and multi-step tasks entirely. If JSON output needed, apply key=value conversion. gemma3:1b or qwen3:1.7b are preferred Tier-1 alternatives.
