# Sovereign Channel Optimization — Final Result

**Run ID:** 202604281951_ml-opt  
**Model:** qwen3:1.7b (via ollama)  
**Host:** workstation  
**Tasks:** 10 / 10 completed  
**Date:** 2026-04-28

---

## Results Summary

| Task | Type | Status | Encoding Used |
|------|------|--------|---------------|
| 001 | Extraction | ✅ SUCCESS | Explicit count + "one per line" + "nothing else" |
| 002 | Classification | ✅ SUCCESS | "exactly one word" + enumerated options |
| 003 | Sorting | ✅ SUCCESS | Comma-separated bound + "nothing else" |
| 004 | Summarization | ✅ SUCCESS | "exactly one sentence" + dash-separated dual negative |
| 005 | Reasoning | ✅ SUCCESS | "Answer: <number>" template on last line |
| 006 | Template Fill | ✅ SUCCESS | [FIELD] bracket delimiters + key=value input |
| 007 | Keyword Extraction | ✅ SUCCESS | Exact count + "plain text" + "on one line" |
| 008 | One-Word Answer | ✅ SUCCESS | Inline colon terminator "Answer in one word:" |
| 009 | Structured Output | ✅ SUCCESS | "no markdown fences" + inline schema notation |
| 010 | Logic | ⚠️ PARTIAL | "step by step" + `<answer>` placeholder (conflicted) |

**Success rate: 9/10 (90%)**  
**Failure mode: angle-bracket placeholder confusion in task 010**

---

## What Encoding Rules Produced Clean Output

### ✅ Reliable Patterns

1. **Explicit count bound**
   - "Extract exactly 5 keywords", "three email addresses"
   - Model honors numeric count reliably

2. **Negative constraint phrase: "nothing else"**
   - Suppresses preamble, explanation, and wrapper text
   - Works equally well standalone or combined with other constraints

3. **Dash-separated constraint pairs**
   - "No introduction, no explanation — just the sentence"
   - The em-dash separator clarifies the positive expectation after the negation

4. **One-per-line / comma-separated format specifiers**
   - Explicit output format → reliable compliance
   - "plain text comma-separated list on one line" = tightest list bound found

5. **Inline colon terminator**
   - "Answer in one word:" (prompt ends with colon)
   - Signals immediate reply → minimal output

6. **Answer-line template (colon prefix)**
   - "Give your answer on the last line as: Answer: <number>"
   - Reliable last-line extraction anchor for reasoning tasks
   - `<number>` not echoed literally; model correctly fills it

7. **"no markdown fences" for JSON**
   - "Output only valid JSON, no explanation, no markdown fences"
   - Suppresses ```json code block wrapping completely

8. **[FIELD] bracket delimiter for template fill**
   - [PLACEHOLDERS] recognized as fill targets
   - key=value input format reliably parsed

9. **"plain text" modifier**
   - Adding "plain text" to list format suppresses trailing markdown spaces
   - Eliminates double-space line-break artifacts

10. **Inline schema for structured output**
    - `{"key": type}` notation → correct type coercion (number vs string)

---

## What Failed

### ❌ Angle-bracket placeholder in output template

- `Answer: <answer>` caused dual output: filled version + literal echo of template
- Avoid `<placeholder>` in output format specifications
- Use plain `Answer:` colon or `[FIELD]` brackets instead

### ⚠️ Verbose "step by step" instruction

- "Solve step by step" opens full markdown output (headers, bold, HR separators)
- If clean extraction from reasoning output is needed, use "---\nAnswer:" delimiter
- "Step by step" should only be used when verbose output is acceptable

---

## Model Behavior Observations

### Thinking Mode (Chain-of-Thought)
- qwen3:1.7b always fires a `Thinking...` block before final output
- Thinking block shows as ANSI-escaped terminal output between `Thinking...` and `...done thinking.`
- Final answer cleanly follows `...done thinking.` — this is a reliable extraction boundary
- Thinking mode is an ASSET for reasoning/logic tasks (catches trick questions, validates logic)
- Thinking mode adds latency but improves accuracy

### Markdown Artifacts
- Model defaults to markdown formatting in verbose mode (bold, headers, HR lines)
- "plain text" modifier suppresses most artifacts
- "no markdown fences" required specifically to suppress JSON code blocks
- Trailing double-space (markdown line break) appears without "plain text"

### Output Size
- Model respects "one word", "one sentence", "one line" bounds reliably
- More verbose when given "step by step" instruction — intended tradeoff

---

## Optimized Encoding Pattern for Qwen 1.7b

### For Extraction / List Tasks
```
Extract exactly N [items] from this [source]. 
Output as a plain text [comma-separated list / one per line], no explanation, nothing else.

[Source content here]
```

### For Classification
```
Classify [X]. Answer with exactly one word: [option1], [option2], or [option3].
```

### For Summarization
```
Summarize in exactly one sentence. No introduction, no explanation — just the sentence.

[Passage here]
```

### For Reasoning / Logic (clean extraction)
```
Solve this problem. Give your answer on the last line as: Answer: [what to put here]

[Problem here]
```

### For Structured JSON Output
```
Output only valid JSON, no explanation, no markdown fences. 
Use this schema: {"key": type, ...}

[Data here]
```

### For Template Fill
```
Fill in the blanks. Replace each [FIELD] with appropriate content. 
Output only the completed [document], nothing else.

[Template with [FIELDS] here]

Use these values: Key=Value, ...
```

### For One-Word / Short Answers
```
[Question]? Answer in one word:
```

---

## Channel Optimization Conclusions

1. **Output bounds are highly effective** — numeric count + format specifier = reliable
2. **Negative constraints work** — "nothing else", "no markdown fences", "no explanation" all honored
3. **Colon terminator is the minimal viable anchor** — most efficient pattern for short answers
4. **Thinking mode is compatible** — extraction happens after `...done thinking.`
5. **Avoid angle-bracket placeholders** — use [BRACKETS] or colon-suffix templates instead
6. **"plain text" suppresses markdown artifacts** — add to all extraction prompts
7. **Verbose mode must be explicitly invited** — model defaults to terse when bound appropriately

The channel between Sovereign and qwen3:1.7b is most efficient when prompts combine:
**explicit count + format specifier + negative constraints + extraction anchor**
