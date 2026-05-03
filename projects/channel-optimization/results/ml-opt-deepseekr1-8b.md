# Sovereign Channel Optimization — Final Result

**Run ID:** 20260428215000_ml-opt  
**Model:** deepseek-r1:8b (via ollama)  
**Host:** workstation  
**Tasks:** 10 / 10 completed  
**Date:** 2026-04-28

---

## Results Summary

| Task | Type | Status | Encoding Used |
|------|------|--------|---------------|
| 001 | Extraction | ✅ SUCCESS | Baseline |
| 002 | Classification | ✅ SUCCESS | Baseline — "negative" (model reasons late delivery is the dominant sentiment) |
| 003 | Sorting | ✅ SUCCESS | Baseline |
| 004 | Summarization | ✅ SUCCESS | Baseline |
| 005 | Reasoning | ✅ SUCCESS | Baseline — Answer: 10:48 (correct, full self-verified solution in thinking) |
| 006 | Template Fill | ✅ SUCCESS | Baseline |
| 007 | Keyword Extraction | ✅ SUCCESS | Baseline |
| 008 | One-Word Answer | ✅ SUCCESS | Baseline |
| 009 | Structured JSON | ✅ SUCCESS | Baseline — clean single-line JSON, no fences |
| 010 | Logic | ✅ SUCCESS | Baseline — "valid" (lowercase, correct) |

**Success rate: 10/10 (100%)**  
**Failure mode: None**

> **Note on Task 002:** deepseek-r1:8b returns "negative" (vs. gemma/qwen models which return "neutral") for the mixed sentiment sentence. The reasoning in the thinking block argues late delivery is a service failure that outweighs the undamaged contents. Both "negative" and "neutral" are defensible; the answer is content-valid even if classification differs from other models.

> **Note on Task 005:** Model returns "Answer: 10:48" without "AM" suffix. Time is mathematically correct (10:48 = 10:48 AM). The thinking block contains two independent verification approaches confirming the answer.

---

## What Encoding Rules Produced Clean Output

### ✅ Reliable Patterns (all baseline — zero adjustments needed)
- **"Extract exactly N"** + **"nothing else"** = clean bounded extraction
- **"exactly one word"** = lowercase compliance (deepseek-r1:8b outputs lowercase without explicit constraint)
- **"plain text"** modifier = no markdown
- **"Answer: [format]"** colon-anchor = final answer on last line, correctly formatted after extensive thinking
- **"no markdown fences"** = clean JSON, no code blocks
- **[FIELD] bracket delimiters** = reliable placeholder substitution
- **"just the sentence"** = suppresses summarization preamble

---

## What Failed
**Nothing failed.** All 10 tasks succeeded at baseline on first try. Zero encoding adjustments required.

---

## Model Behavior Observations

### Thinking Tokens
deepseek-r1:8b uses a visible thinking phase, rendered by ollama CLI as:
```
Thinking...
[extended internal reasoning — often 500-1000 words]
...done thinking.

[final answer]
```

The thinking block is extremely detailed:
- **Task 001:** Enumerates all 7 cities, decides to pick first 5 in order
- **Task 002:** Detailed sentiment analysis; reasons late delivery = service failure = negative
- **Task 005:** Two independent derivation approaches (relative speed, then position equation) plus distance verification — all agree on 10:48
- **Task 009:** Notes the exact schema requirements and considers automation context
- **Task 010:** Full categorical syllogism analysis with "All A are B; C is A; therefore C is B" pattern recognition

### Key Observations
- **No case bias** — returns lowercase single-word answers by default; no explicit "lowercase" constraint needed
- **JSON compliance** — "no markdown fences" alone sufficient; returns compact single-line JSON without code block wrapping
- **Thinking quality** — extremely thorough; verifies answers using multiple methods in thinking before committing
- **Format compliance** — format instructions survive thinking phase; output section adheres to all constraints
- **Slower than non-thinking models** — each response takes ~30-60s due to extensive thinking; budget accordingly
- **Task 005 time format** — returns "10:48" instead of "10:48 AM"; minor format deviation but content correct

---

## Optimized Encoding Pattern for deepseek-r1:8b

The **Qwen 1.7b baseline is fully compatible** with deepseek-r1:8b. No adjustments required.

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

Template: [template]

Values: KEY=value, KEY=value
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

**deepseek-r1:8b is a best-in-class tier-3 executor** rivaling tier-4 models. Baseline encoding transfers perfectly with zero adjustment. The thinking mode provides self-verification that makes answers highly reliable.

**Key differences from Qwen 1.7b baseline:**
- **Same encoding works** — no simplification or augmentation needed
- **Better reasoning** — thinking mode with multi-method verification eliminates reasoning errors
- **Correct case by default** — lowercase compliance without explicit constraint (better than qwen2.5-coder:14b)
- **JSON compliance** — "no markdown fences" alone sufficient (better than gemma/phi4)
- **Thinking latency** — each task takes ~30-60s due to extensive reasoning; significant latency cost
- **Time format** — may omit "AM/PM" suffix on time answers; consider specifying format explicitly

**deepseek-r1:8b vs. gemma3:12b (baseline compatibility comparison):**
- Both: zero encoding adjustments, 100% success
- deepseek-r1:8b: slower due to thinking, but self-verifies reasoning
- gemma3:12b: faster, no thinking overhead, equally reliable on bounded tasks
- deepseek-r1:8b advantage: complex reasoning tasks benefit from multi-method verification

**Recommendation for Sovereign:** Use deepseek-r1:8b with the standard Qwen 1.7b baseline encoding — zero modifications needed. Premium executor for reasoning-heavy tasks where latency is acceptable. Apply time format specifier for time-based answers if "AM/PM" is required. The thinking phase provides verification that makes this model the most reliable mid-tier option for complex tasks.
