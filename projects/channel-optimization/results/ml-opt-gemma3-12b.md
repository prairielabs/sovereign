# Sovereign Channel Optimization — Final Result

**Run ID:** 20260428202400_ml-opt  
**Model:** gemma3:12b (via ollama)  
**Host:** workstation  
**Tasks:** 10 / 10 completed  
**Date:** 2026-04-28

---

## Results Summary

| Task | Type | Status | Encoding Used |
|------|------|--------|---------------|
| 001 | Extraction | ✅ SUCCESS | Baseline — "Extract exactly 5 cities... plain text comma-separated list on one line, no explanation, nothing else." |
| 002 | Classification | ✅ SUCCESS | Baseline — "Answer with exactly one word: positive, negative, or neutral." |
| 003 | Sorting | ✅ SUCCESS | Baseline — "Output as a comma-separated list, nothing else." |
| 004 | Summarization | ✅ SUCCESS | Baseline — "Summarize in exactly one sentence. No introduction, no explanation — just the sentence." |
| 005 | Reasoning | ✅ SUCCESS | Baseline — "Give your answer on the last line as: Answer: [time]" — produced 10:48 AM (mathematically correct) |
| 006 | Template Fill | ✅ SUCCESS | Baseline — [FIELD] bracket syntax with key=value Values block |
| 007 | Keyword Extraction | ✅ SUCCESS | Baseline — "Extract exactly 5 keywords... plain text comma-separated list on one line, nothing else." |
| 008 | One-Word Answer | ✅ SUCCESS | Baseline — "Answer in one word:" |
| 009 | Structured JSON | ✅ SUCCESS | Baseline — "Output only valid JSON, no explanation, no markdown fences." |
| 010 | Logic | ✅ SUCCESS | Baseline — "Answer with exactly one word: valid or invalid." |

**Success rate: 10/10 (100%)**  
**Failure mode: None**

> **Note on Task 005:** The task specification states the correct answer is "11:00 AM" but this is mathematically incorrect. At 10 AM, Train A has covered 60 miles; remaining distance = 120 miles; combined closing speed = 150 mph; time = 0.8 h = 48 min; meeting time = 10:48 AM. gemma3:12b produced the mathematically correct answer. Treat 10:48 AM as ✅.

---

## What Encoding Rules Produced Clean Output

### ✅ Reliable Patterns
- **Exact count + format specifier** — "Extract exactly 5" + "comma-separated list on one line" = clean bounded output
- **"nothing else" / "no explanation"** — effectively suppresses wrapper prose and preamble
- **"Answer: [time]" colon-anchor** — model places final answer exactly on last line with colon prefix
- **"plain text" modifier** — no markdown lists or bullet points, raw comma-separated output
- **"no markdown fences"** — clean JSON output without ``` wrapping
- **[FIELD] bracket delimiters** — model reliably replaces all three without echoing extras
- **"exactly one word"** — strong constraint, model complies without hedging
- **"just the sentence" terminator** — stops preamble in summarization tasks
- **key=value Values block** — cleanest way to provide template substitution data

---

## What Failed
**Nothing failed at baseline.** gemma3:12b required zero encoding adjustments across all 10 tasks.

---

## Model Behavior Observations
- **Very high instruction compliance** — follows format constraints precisely on first try
- **No thinking block** — direct output, no `<think>...</think>` prefix
- **Verbosity controlled** — suppression phrases ("nothing else", "no explanation") are highly effective
- **Mathematical reasoning** — shows work in Task 005, arrives at correct answer; "Answer: [time]" anchor reliably extracts the result from longer reasoning output
- **JSON output** — clean, correctly typed, no extra fields, no fencing
- **Template fill** — interpolates all values correctly without echoing the template structure
- **No markdown bleed** — in tasks where markdown would be tempting (sorting, keywords), model stays plain text

---

## Optimized Encoding Pattern for Gemma3:12b

The **Qwen 1.7b baseline is fully compatible** with gemma3:12b. No adjustments required. These templates transfer without modification:

**Extraction:**
```
Extract exactly N [items] from this text. Output as a plain text comma-separated list on one line, no explanation, nothing else.

Text: [passage]
```

**Classification:**
```
Classify this [input] as [A], [B], or [C]. Answer with exactly one word: [A], [B], or [C].

[Input label]: [content]
```

**Sorting:**
```
Sort these words alphabetically. Output as a comma-separated list, nothing else.

Words: [list]
```

**Summarization:**
```
Summarize in exactly one sentence. No introduction, no explanation — just the sentence.

Passage: [text]
```

**Reasoning:**
```
Solve this problem. Give your answer on the last line as: Answer: [format]

Problem: [problem]
```

**Template Fill:**
```
Fill in the blanks. Replace each [FIELD] with appropriate content. Output only the completed text, nothing else.

Template: [template with [FIELD] placeholders]

Values: KEY=value, KEY=value, KEY=value
```

**Keyword Extraction:**
```
Extract exactly N keywords from this passage. Output as a plain text comma-separated list on one line, nothing else.

Passage: [text]
```

**One-Word Answer:**
```
[Question]? Answer in one word:
```

**Structured JSON:**
```
Output only valid JSON, no explanation, no markdown fences. Use this schema: {schema}

Data: [description]
```

**Logic:**
```
Is this argument valid? Answer with exactly one word: valid or invalid.

Argument: [argument]
```

---

## Channel Optimization Conclusions

**gemma3:12b is a high-fidelity executor.** Baseline encoding transfers cleanly with zero adjustment. This is the ideal Sovereign→Executor scenario: a model that requires no channel-specific encoding overhead.

**Key differences from Qwen 1.7b baseline:**
- Same encoding works — no simplification or augmentation needed
- Arguably more robust: shows mathematical work but still anchors final answer correctly
- Slightly more verbose in reasoning tasks (Task 005 showed full solution steps), but "Answer: [time]" anchor extracts cleanly regardless
- Zero markdown bleed even without explicit "plain text" modifiers (though keeping them doesn't hurt)

**Recommendation for Sovereign:** Use gemma3:12b with the standard baseline encoding. No model-specific overrides required. It is the cleanest tier-4 executor tested to date.
