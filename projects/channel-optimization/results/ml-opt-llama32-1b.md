# Sovereign Channel Optimization — Final Result

**Run ID:** 20260428202800_ml-opt  
**Model:** llama3.2:1b (via ollama)  
**Host:** workstation  
**Tasks:** 10 / 10 completed  
**Date:** 2026-04-28

---

## Results Summary

| Task | Type | Status | Encoding Used |
|------|------|--------|---------------|
| 001 | Extraction | ✅ SUCCESS | Adjusted — added "Stop after listing 5. You must list exactly 5 cities — not more, not fewer." |
| 002 | Classification | ✅ SUCCESS | Adjusted — added "exactly one lowercase word" + "A sentence with both positive and negative aspects is neutral." |
| 003 | Sorting | ✅ SUCCESS | Baseline |
| 004 | Summarization | ✅ SUCCESS | Baseline |
| 005 | Reasoning | ⚠️ PARTIAL | Scaffolded — had to provide intermediate calculation steps; model extracted final answer correctly but cannot self-reason |
| 006 | Template Fill | ✅ SUCCESS | Adjusted — "Write the completed sentence... Output only the single completed sentence, nothing else." + explicit [X]→value notation |
| 007 | Keyword Extraction | ✅ SUCCESS | Baseline |
| 008 | One-Word Answer | ✅ SUCCESS | Baseline (returned "Au." with period — acceptable) |
| 009 | Structured JSON | ✅ SUCCESS | Baseline (returned indented JSON — valid, no fences) |
| 010 | Logic | ❌ FAIL | Multiple retries — model consistently classifies the valid syllogism as "invalid"; capability failure |

**Success rate: 8/10 (80%)** + 1 PARTIAL (Task 005)  
**Failure mode: Logic evaluation capability gap; extraction count boundary; safety refusal on template fill baseline**

---

## What Encoding Rules Produced Clean Output

### ✅ Reliable Patterns
- **Explicit count + hard boundary** — "Extract exactly 5... not more, not fewer." forces compliance (baseline "exactly 5" alone was insufficient)
- **"lowercase" case constraint** — adding "exactly one lowercase word" prevents capitalized single-word answers
- **"Output only the single completed sentence, nothing else"** — resolves safety refusal on template fill baseline
- **Explicit [X]→value format** — "Replace [NAME] with Sarah, [PRODUCT] with wireless headphones" cleaner than key=value pairs
- **Answer: [format] anchor** — works when reasoning is pre-scaffolded for it
- **Baseline sort/summarize/keyword prompts** — transfer cleanly from Qwen 1.7b
- **"Answer in one word:"** — reliable for factual recall (Au, etc.)
- **"no markdown fences"** — JSON output clean

---

## What Failed

### ❌ Task 001 (Baseline)
Baseline returned all 7 cities in the text. Model doesn't enforce the count boundary without explicit redundancy ("not more, not fewer").

### ❌ Task 002 (Baseline)
Returned "Negative" — capital N and arguably wrong classification (the sentence is mixed/neutral, though "negative" is defensible). Adding "lowercase" and a classification hint resolved case; content is debatable.

### ❌ Task 005 (Reasoning)
Model cannot solve the train-meeting problem from scratch. Attempted reasoning goes off-rails with incorrect relative-velocity calculations. Only recovers when intermediate steps are pre-computed and provided. This is a hard capability ceiling for 1b models.

### ❌ Task 006 (Baseline)
Baseline triggered safety refusal: "I can't fulfill that request." The word "blanks" or "template" in baseline appears to trigger refusal. Switching to "completed sentence... Replace [X] with Y" framing bypassed this.

### ❌ Task 010 (All retries)
Consistently answers "invalid" for a classic valid syllogism. Even with explicit deductive framing ("If all X are Y, and Z is an X, then Z is Y — this is valid"), the model responds with nonsense ("a"). This is a fundamental logic reasoning failure. Encoding cannot compensate for capability gap.

---

## Model Behavior Observations
- **No thinking block** — direct output, no chain-of-thought
- **Safety refusals** — surprisingly triggered by template fill baseline. Word "blanks" or bracketed placeholder syntax may be flagged. Rephrasing resolves it.
- **Count boundary weakness** — single "exactly N" is insufficient; needs explicit "not more, not fewer" reinforcement
- **Case sensitivity** — outputs capitalized single-word answers by default; "lowercase" constraint needed
- **Reasoning ceiling** — 1b parameter count is the hard floor; multi-step math fails entirely
- **Logic failure** — systematic misclassification of valid syllogism; this appears to be a training gap
- **Factual recall** — strong; "Au", sorting, keywords all work reliably
- **JSON** — produces valid but indented JSON (cosmetic, not functional issue)

---

## Optimized Encoding Pattern for llama3.2:1b

**Extraction (requires hard boundary):**
```
Extract exactly N [items] from this text. Stop after listing N. Output as a plain text comma-separated list on one line, no explanation, nothing else. You must list exactly N items — not more, not fewer.

Text: [passage]
```

**Classification (requires case constraint):**
```
Classify this [input] as [A], [B], or [C]. [Disambiguation hint if needed.] Answer with exactly one lowercase word: [A], [B], or [C].

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

**Reasoning (scaffold required):**
```
[Pre-compute intermediate steps and show them in the prompt]
Give your answer on the last line as: Answer: [format]
```

**Template Fill (avoid "blanks" trigger):**
```
Write the completed sentence without any line breaks. Output only the single completed sentence, nothing else.

Input: [template with [FIELD] placeholders]
Replace [FIELD1] with [value1], [FIELD2] with [value2], [FIELD3] with [value3].

Output:
```

**Keyword Extraction (baseline works):**
```
Extract exactly N keywords from this passage. Output as a plain text comma-separated list on one line, nothing else.

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

**Logic (encoding cannot fix capability gap — avoid for 1b):**
```
⚠️ Not reliable. Do not route logic evaluation tasks to llama3.2:1b.
```

---

## Channel Optimization Conclusions

**llama3.2:1b is a partial executor** suitable for well-bounded retrieval and format tasks but unreliable for reasoning and logic.

**Key differences from Qwen 1.7b baseline:**
- Extraction needs hard boundary redundancy ("not more, not fewer") — Qwen 1.7b complies with "exactly N" alone
- Case constraints must be explicit ("lowercase") — Qwen 1.7b handles case correctly by default
- Safety refusal triggered by template fill baseline phrasing — requires rephrasing; Qwen 1.7b has no such trigger
- Reasoning capability below Qwen 1.7b — cannot self-solve multi-step math problems; needs scaffolding
- Logic evaluation fails entirely — not a channel issue, a capability ceiling
- JSON, sorting, keywords, factual recall all work reliably

**Recommendation for Sovereign:** Use llama3.2:1b for extraction, classification, sorting, summarization, keywords, factual recall, and JSON. Do NOT route reasoning or logic tasks. Encoding requires explicit case + count-boundary reinforcement compared to Qwen 1.7b baseline.
