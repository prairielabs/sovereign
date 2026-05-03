# Sovereign Channel Optimization — Final Result

**Run ID:** 20260428203200_ml-opt  
**Model:** llava:7b (via ollama)  
**Host:** workstation  
**Tasks:** 10 / 10 completed (TEXT-ONLY — visual tasks require separate vision protocol)  
**Date:** 2026-04-28

---

## Results Summary

| Task | Type | Status | Encoding Used |
|------|------|--------|---------------|
| 001 | Extraction | ✅ SUCCESS | Adjusted — added "Count: 1, 2, 3, 4, 5 — exactly five. No more." |
| 002 | Classification | ✅ SUCCESS | Adjusted — "exactly one lowercase word only" |
| 003 | Sorting | ✅ SUCCESS | Baseline |
| 004 | Summarization | ✅ SUCCESS | Baseline |
| 005 | Reasoning | ⚠️ PARTIAL | Requires heavily scaffolded reasoning steps; independent solving fails; format compliance inconsistent |
| 006 | Template Fill | ✅ SUCCESS | Baseline |
| 007 | Keyword Extraction | ✅ SUCCESS | Adjusted — "List the 5 most important keywords... Stop after 5. Format: word1, word2, word3, word4, word5" |
| 008 | One-Word Answer | ✅ SUCCESS | Baseline |
| 009 | Structured JSON | ✅ SUCCESS | Baseline |
| 010 | Logic | ✅ SUCCESS | Adjusted — "One word answer in lowercase. Answer (valid/invalid):" |

**Success rate: 9/10 (90%)** + 1 PARTIAL (Task 005)  
**Failure mode: Count boundary requires extra reinforcement; case requires explicit lowercase; reasoning under-performs 7b tier expectation**

> **Note:** llava:7b is primarily a vision-language model. Text-only tasks are within its capability but it was optimized for multimodal input. Visual tasks (image description, OCR, chart reading) require a separate vision protocol using the `--image` flag or API image attachment.

---

## What Encoding Rules Produced Clean Output

### ✅ Reliable Patterns
- **Count + visual enumeration** — "Count: 1, 2, 3, 4, 5 — exactly five." works better than "exactly 5" alone
- **"Stop after 5"** — explicit stopping instruction for keyword/extraction tasks
- **Explicit format template** — "Format: word1, word2, word3, word4, word5" removes ambiguity on extraction count
- **"exactly one lowercase word only"** — resolves default capitalization behavior
- **"Answer (valid/invalid):"** colon-suffix with parenthetical options — better than asking for "valid or invalid"
- **Baseline sort/JSON/template/factual prompts** — transfer cleanly from Qwen 1.7b

---

## What Failed

### ❌ Task 001 (Baseline)
Baseline returned 4 cities ("Paris, Tokyo, New York, Sydney"). The model missed the 5th despite "exactly 5". Resolved with counting scaffolding.

### ❌ Task 002 (Baseline)  
Returned "Neutral" with capital N. Adding "lowercase" constraint to one-word answer instructions resolved it.

### ❌ Task 005 (All retries — PARTIAL)
Independent reasoning produces wrong answer. First attempt: computed 270 miles incorrectly, got "11:48 AM". Second attempt (better prompt): computed "9:48 AM" — same 48-minute calculation but anchored to 9 AM instead of 10 AM. Correct answer (10:48 AM) only obtained with pre-computed steps. Even when scaffolded, output format was "The meeting time would be at 10:48AM" instead of "Answer: [time]". Format instruction non-compliance under reasoning load.

### ❌ Task 007 (Baseline)
Returned 11 keywords. "Exactly 5" alone insufficient. Required "Stop after 5" + explicit format template.

### ❌ Task 010 (Baseline/Retry 1)
Returned "Valid" (capital V) consistently. Even with "lowercase" instruction, capitalized. Resolved only with the "(valid/invalid):" colon-suffix format.

---

## Model Behavior Observations
- **No thinking block** — direct output, no chain-of-thought prefix
- **Multimodal heritage** — text behavior slightly different from pure text LLMs; some formatting tendencies differ
- **Count boundaries** — persistently weak; requires both "stop after N" and visual counting scaffolding
- **Capitalization** — default sentence-start capitalization; requires lowercase constraint and format anchoring
- **Reasoning** — 7b parameters insufficient for reliable multi-step arithmetic; scaffolded reasoning helps but format compliance degrades under cognitive load
- **Sorting, JSON, summarization, factual** — clean and reliable on first try
- **Template fill** — baseline works perfectly (unlike llama3.2:1b which triggers refusal)

---

## Optimized Encoding Pattern for llava:7b (Text Tasks)

**Extraction (requires counting scaffold):**
```
From the text below, pick exactly N [items] and list them as a comma-separated list. Count: 1, 2, 3, 4, 5 — exactly five. No more. Output only the list on one line, nothing else.

Text: [passage]
```

**Classification (requires lowercase constraint):**
```
Classify this [input] as [A], [B], or [C]. Answer with exactly one lowercase word only: [A], [B], or [C]. No other words, no capitalization.

[Input label]: [content]
```

**Sorting (baseline works):**
```
Sort these words alphabetically. Output as a comma-separated list, nothing else.

Words: [list]
```

**Summarization (baseline works):**
```
Summarize in exactly one sentence. No introduction, no explanation — just the sentence.

Passage: [text]
```

**Reasoning (scaffolded only — not reliable for independent solving):**
```
[Pre-compute intermediate steps in the prompt]
The answer is [X].
Complete this line:
Answer: [format]
```

**Template Fill (baseline works):**
```
Fill in the blanks. Replace each [FIELD] with appropriate content. Output only the completed text, nothing else.

Template: Dear [NAME], thank you for your order of [PRODUCT] placed on [DATE].

Values: NAME=Sarah, PRODUCT=wireless headphones, DATE=April 28 2026
```

**Keyword Extraction (requires stop + format template):**
```
List the N most important keywords from this passage. Stop after N. Format: word1, word2, word3, word4, word5 — one line, nothing else.

Passage: [text]
```

**One-Word Factual (baseline works):**
```
[Question]? Answer in one word:
```

**Structured JSON (baseline works):**
```
Output only valid JSON, no explanation, no markdown fences. Use this schema: {schema}

Data: [description]
```

**Logic (parenthetical format required):**
```
One word answer in lowercase. Is this syllogism valid or invalid?
[Argument stated plainly]
Answer (valid/invalid):
```

---

## Channel Optimization Conclusions

**llava:7b is a capable text executor with count and case boundary weaknesses.** Core retrieval and formatting tasks work reliably with targeted encoding adjustments. Reasoning is a weak point for this model.

**Key differences from Qwen 1.7b baseline:**
- Count boundaries need visual counting scaffolding ("Count: 1, 2, 3...")
- Case requires "lowercase" + format anchoring; Qwen 1.7b complies with "exactly one word" alone
- Reasoning ceiling lower than expected for 7b; scaffolding needed; Qwen 1.7b handles similar tasks better
- Template fill works on baseline (better than llama3.2:1b which had safety refusal)
- Sorting, JSON, factual recall all reliable

**Recommendation for Sovereign:** Use llava:7b for bounded retrieval, classification (with lowercase constraint), sorting, JSON, and template fill. Route reasoning tasks to larger models. For visual tasks, use vision protocol (not text-only prompts). Apply count scaffolding on all extraction tasks.

**Vision tasks:** llava:7b supports image input via the multimodal API. Visual tasks (image description, object detection, OCR) should be tested in a separate vision protocol session using proper image attachment.
