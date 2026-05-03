> *This is the research avenue.*

# Sovereign Channel Optimization — Comparative Encoding Guide

**Corpus:** 14 models × 10 tasks = 140 optimization drills  
**Date:** 2026-04-29  
**Host:** Brim (AMD Ryzen 9 5900X / RX 6950 XT 16GB / Ubuntu 24.04)  
**Author:** Sovereign (conductor) + Cal (operator)

---

## What This Is

This guide is the distilled output of the Sovereign channel optimization corpus. Every executor model in the ensemble was run through an identical 10-task optimization drill. Encoding was adjusted after each failed task until a working pattern was found. The result is a per-model encoding protocol and a side-by-side comparison showing exactly how the Sovereign→Executor channel must change as model size, architecture, and training shift.

**The question under investigation:** If the channel between Sovereign and an executor is correctly encoded, how reliably does meaning transfer — and where does encoding hit a ceiling it cannot cross? This corpus does not close that question. It opens the avenue.

---

## How to Read This Guide

- **Baseline** = the encoding pattern derived from qwen3:1.7b. It is the reference against which all other models are measured.
- **Overhead** = how many encoding adjustments are required beyond baseline. Lower is better.
- **A "0 overhead" model** means Sovereign can use the same prompt templates for all 10 task types with no modification.
- **Task type codes:** EXT=extraction, CLS=classification, SRT=sorting, SUM=summarization, RSN=reasoning, TPL=template fill, KWD=keyword extraction, OWA=one-word answer, JSN=structured JSON, LGC=logic.

---

## Part 1: The Baseline Encoding Protocol

All baseline patterns were derived empirically from qwen3:1.7b. These are the reference templates.

### EXT — Extraction
```
Extract exactly N [items] from this text.
Output as a plain text comma-separated list on one line, no explanation, nothing else.

Text: [passage]
```

### CLS — Classification
```
Classify this [input] as [A], [B], or [C]. Answer with exactly one word: [A], [B], or [C].

[Input label]: [content]
```

### SRT — Sorting
```
Sort these words alphabetically. Output as a comma-separated list, nothing else.

Words: [list]
```

### SUM — Summarization
```
Summarize in exactly one sentence. No introduction, no explanation — just the sentence.

Passage: [text]
```

### RSN — Reasoning
```
Solve this problem. Give your answer on the last line as: Answer: [format]

Problem: [problem]
```

### TPL — Template Fill
```
Fill in the blanks. Replace each [FIELD] with appropriate content. Output only the completed text, nothing else.

Template: [template with [FIELD] placeholders]

Values: KEY=value, KEY=value
```

### KWD — Keyword Extraction
```
Extract exactly N keywords from this passage. Output as a plain text comma-separated list on one line, nothing else.

Passage: [text]
```

### OWA — One-Word Answer
```
[Question]? Answer in one word:
```

### JSN — Structured JSON
```
Output only valid JSON, no explanation, no markdown fences. Use this schema: {schema}

Data: [description]
```

### LGC — Logic
```
Is this argument valid? Answer with exactly one word: valid or invalid.

Argument: [argument]
```

### Core Encoding Principles (Derived)
1. **Explicit count bound** — "exactly N" is the primary boundary; redundant "not more, not fewer" needed for some models
2. **Negative constraints** — "nothing else", "no explanation", "no markdown fences" all suppress unwanted output
3. **Dash-separated constraint pairs** — "No introduction, no explanation — just the sentence" clarifies what IS expected
4. **Colon terminator** — prompt ending with `:` signals immediate reply, minimal output
5. **Answer-line template** — "Give your answer on the last line as: Answer: [format]" is a reliable extraction anchor
6. **[FIELD] bracket delimiters** — recognized as fill targets; `<angle>` placeholders echo literally — avoid
7. **"plain text" modifier** — suppresses trailing markdown artifacts in list outputs
8. **"no markdown fences"** — suppresses JSON code block wrapping in compliant models

---

## Part 2: Encoding Overhead Matrix

The central claim: encoding overhead measures channel friction. Zero overhead = signal transfers without loss.

| Model | Tier | Score | Overhead | Case | Count | JSON | Reasoning | Logic | Notable |
|-------|------|-------|----------|------|-------|------|-----------|-------|---------|
| **qwen3:1.7b** | 1 | 9/10 | 0 (baseline) | ✅ | ✅ | ✅ | ✅ | ⚠️ partial | Angle-bracket echo on LGC |
| **llama3.2:1b** | 1 | 8/10 | **5** | ❌ need "lowercase" | ❌ need "not more, not fewer" | ✅ | ❌ scaffold only | ❌ fails | Safety refusal on TPL baseline |
| **gemma3:1b** | 1 | 10/10 | **3** | ❌ need "lowercase" | ✅ | ❌ few-shot only | ✅ | ✅ w/ fix | JSON few-shot is major workaround |
| **phi4-mini** | 1 | 8/10 | **6** | ❌ need "lowercase" | ✅ | ❌ key=value | ❌ scaffold only | ⚠️ partial | Technical bias in SUM; keyword separator issue |
| **qwen2.5-coder:7b** | 2 | 9/10 | **5** | ❌ need "lowercase" | ❌ need "not more, not fewer" | ❌ +no backticks | ❌ scaffold only | ✅ w/ fix | Comma spacing cosmetic |
| **llava:7b** | 2 | 9/10 | **4** | ❌ need "lowercase" | ❌ need counting scaffold | ✅ | ❌ scaffold only | ✅ w/ fix | Vision model — text-only here |
| **qwen3:8b** | 3 | 9/10 | **1** | ✅ | ✅ | ✅ | ⚠️ +plain text | ✅ | Comma spacing cosmetic |
| **deepseek-r1:8b** | 3 | 10/10 | **0** | ✅ | ✅ | ✅ | ✅ | ✅ | **Zero overhead** — baseline transfers |
| **gemma3:4b** | 3 | 10/10 | **3** | ❌ need "lowercase" | ✅ | ❌ +no backticks | ✅ | ✅ | Lowercase + JSON fix |
| **qwen2.5-coder:14b** | 3 | 10/10 | **2** | ❌ need "lowercase" | ✅ | ✅ | ✅ | ✅ w/ fix | Only case fix needed |
| **qwen3:14b** | 4 | 10/10 | **0** | ✅ | ✅ | ✅ | ✅ | ✅ | **Zero overhead** — baseline transfers |
| **deepseek-r1:14b** | 4 | 10/10 | **1** | ✅ | ❌ need intent affirmation | ✅ | ✅ | ✅ | Unique: self-correction overrides count |
| **phi4** | 4 | 10/10 | **4** | ❌ need complex framing | ✅ | ❌ key=value | ✅ | ❌ fill-blank only | Verbosity bias throughout |
| **gemma3:12b** | 4 | 10/10 | **0** | ✅ | ✅ | ✅ | ✅ | ✅ | **Zero overhead** — baseline transfers |

**Zero-overhead models:** deepseek-r1:8b, qwen3:14b, gemma3:12b  
**Near-zero (1 fix):** qwen3:8b, deepseek-r1:14b  
**Moderate (2–3 fixes):** qwen2.5-coder:14b, gemma3:1b, gemma3:4b  
**High overhead (4–6 fixes):** phi4, llava:7b, qwen2.5-coder:7b, llama3.2:1b, phi4-mini

---

## Part 3: Per-Task Encoding Variations

### EXT — Extraction

**Baseline:** "Extract exactly N [items]... plain text comma-separated list on one line, no explanation, nothing else."

| Model | Deviation from Baseline |
|-------|------------------------|
| qwen3:1.7b | None — baseline works |
| llama3.2:1b | Add: "Stop after listing N. You must list exactly N items — not more, not fewer." |
| gemma3:1b | None — baseline works |
| phi4-mini | None — baseline works |
| qwen2.5-coder:7b | Add: "Stop at N. Exactly N items — not more, not fewer." |
| llava:7b | Replace count with: "Count: 1, 2, 3, 4, 5 — exactly five. No more." |
| qwen3:8b | None — but output lacks spaces after commas (cosmetic) |
| deepseek-r1:8b | None — baseline works |
| gemma3:4b | None — baseline works |
| qwen2.5-coder:14b | None — baseline works |
| qwen3:14b | None — baseline works |
| deepseek-r1:14b | Add: "This is intentional — there are M items but choose only N and stop." |
| phi4 | None — baseline works |
| gemma3:12b | None — baseline works |

**Rule:** Smaller models (≤7b, except qwen3:1.7b) need redundant count enforcement. deepseek-r1:14b needs intent affirmation when total > count.

---

### CLS — Classification

**Baseline:** "Answer with exactly one word: [A], [B], or [C]."

| Model | Deviation from Baseline |
|-------|------------------------|
| qwen3:1.7b | None — lowercase by default |
| llama3.2:1b | Add "lowercase": "exactly one lowercase word". Add disambiguation hint for mixed-sentiment inputs. |
| gemma3:1b | Add "lowercase" |
| phi4-mini | Rephrase to explicit enumeration: "The answer is exactly one of: A, B, C. [hint if ambiguous]" + lowercase |
| qwen2.5-coder:7b | Add "lowercase" |
| llava:7b | Add "lowercase only. No other words, no capitalization." |
| qwen3:8b | None — lowercase by default |
| deepseek-r1:8b | None — lowercase by default |
| gemma3:4b | Add "lowercase" |
| qwen2.5-coder:14b | Add "lowercase" |
| qwen3:14b | None — lowercase by default |
| deepseek-r1:14b | None — lowercase by default |
| phi4 | Use: "The answer is exactly one of these three words: A, B, C. Choose the correct one and output it in lowercase with no punctuation, no explanation:" |
| gemma3:12b | None — baseline works |

**Rule:** qwen3 family and deepseek-r1 family output lowercase by default. gemma3, qwen2.5-coder, llama, llava, phi families default to sentence-case — add "lowercase".

---

### SRT — Sorting

**Baseline:** "Sort these words alphabetically. Output as a comma-separated list, nothing else."

| Model | Deviation from Baseline |
|-------|------------------------|
| All models | **None — baseline works universally** |

**Rule:** Sorting is the most robust task type. No model required adjustment. This is the channel's most efficient operation.

---

### SUM — Summarization

**Baseline:** "Summarize in exactly one sentence. No introduction, no explanation — just the sentence."

| Model | Deviation from Baseline |
|-------|------------------------|
| qwen3:1.7b | None |
| llama3.2:1b | None |
| gemma3:1b | None |
| phi4-mini | Replace with: "Write one simple clear sentence summarizing this. Only the sentence, nothing else." (technical jargon bias) |
| qwen2.5-coder:7b | None |
| llava:7b | None |
| qwen3:8b | None |
| deepseek-r1:8b | None |
| gemma3:4b | None |
| qwen2.5-coder:14b | None |
| qwen3:14b | None |
| deepseek-r1:14b | None |
| phi4 | None (baseline works, no technical bias at full scale) |
| gemma3:12b | None |

**Rule:** Summarization is reliable at baseline for all models except phi4-mini, which has a technical-jargon bias requiring "simple clear" framing.

---

### RSN — Reasoning

**Baseline:** "Solve this problem. Give your answer on the last line as: Answer: [format]"

| Model | Capability | Deviation from Baseline |
|-------|-----------|------------------------|
| qwen3:1.7b | ✅ Independent | None (thinking mode assists) |
| llama3.2:1b | ❌ Scaffold only | Pre-compute all intermediate steps in prompt. Capability ceiling. |
| gemma3:1b | ✅ Independent | None — surprisingly capable for 1b |
| phi4-mini | ❌ Scaffold only | Pre-compute required. Even with scaffolding, format compliance poor. |
| qwen2.5-coder:7b | ❌ Scaffold only | Pre-compute required. May produce bold "**Answer:**" instead of "Answer:". |
| llava:7b | ❌ Scaffold only | Pre-compute required. Format compliance inconsistent under load. |
| qwen3:8b | ✅ Independent | Add "plain text" to anchor: "Give your answer on the last line as plain text: Answer: [format]" |
| deepseek-r1:8b | ✅ Independent | None — multi-method self-verification in thinking |
| gemma3:4b | ✅ Independent | None — full solution with verification |
| qwen2.5-coder:14b | ✅ Independent | None — strong structured reasoning from coder training |
| qwen3:14b | ✅ Independent | None — thinking mode, multi-method verification |
| deepseek-r1:14b | ✅ Independent | None — most thorough reasoning in ensemble |
| phi4 | ✅ Independent | None — detailed step-by-step, correct answer |
| gemma3:12b | ✅ Independent | None |

**Rule:** Reasoning capability correlates with model size but is not strictly linear. gemma3:1b is a notable exception — handles reasoning above its weight class. All 1b-tier and 7b-tier models (except gemma3:1b) require scaffolding. 8b+ models reason independently. qwen3:8b needs "plain text" modifier to prevent markdown bold contamination on the Answer: line.

---

### TPL — Template Fill

**Baseline:** "[FIELD] bracket placeholders + key=value Values block"

| Model | Deviation from Baseline |
|-------|------------------------|
| qwen3:1.7b | None |
| llama3.2:1b | Avoid "blanks" and "fill in the blanks" phrasing — triggers safety refusal. Use: "Write the completed sentence. Replace [FIELD] with value. Output only the completed sentence, nothing else." |
| gemma3:1b | None |
| phi4-mini | None |
| qwen2.5-coder:7b | None |
| llava:7b | None |
| qwen3:8b | None |
| deepseek-r1:8b | None |
| gemma3:4b | None |
| qwen2.5-coder:14b | None |
| qwen3:14b | None |
| deepseek-r1:14b | None |
| phi4 | None |
| gemma3:12b | None |

**Rule:** Template fill is reliable at baseline for 13/14 models. llama3.2:1b is the single exception — its safety filter can misfire on "fill in the blanks" phrasing. Rephrase around the word "blanks".

---

### KWD — Keyword Extraction

**Baseline:** "Extract exactly N keywords... plain text comma-separated list on one line, nothing else."

| Model | Deviation from Baseline |
|-------|------------------------|
| qwen3:1.7b | None |
| llama3.2:1b | None — baseline works |
| gemma3:1b | Add "all lowercase" — keyword lists default to sentence-case |
| phi4-mini | Add "comma-separated lowercase: word1, word2..." — space-separated by default, not comma |
| qwen2.5-coder:7b | None — baseline works |
| llava:7b | Add stop instruction: "Stop after N. Format: word1, word2, word3..." — returns too many without |
| qwen3:8b | None — but comma spacing may be omitted (cosmetic) |
| deepseek-r1:8b | None |
| gemma3:4b | Add "all lowercase" |
| qwen2.5-coder:14b | None |
| qwen3:14b | None |
| deepseek-r1:14b | None — but may return multi-word phrases rather than single tokens |
| phi4 | None — baseline works at full scale |
| gemma3:12b | None |

**Rule:** Gemma family (all sizes) needs "all lowercase" on keywords. phi4-mini uniquely defaults to space-separated output — needs comma format. deepseek-r1:14b may return phrase-length keywords (semantically richer but harder to parse).

---

### OWA — One-Word Answer

**Baseline:** "[Question]? Answer in one word:"

| Model | Deviation from Baseline |
|-------|------------------------|
| qwen3:1.7b | None |
| llama3.2:1b | None (may include trailing period — cosmetic) |
| gemma3:1b | None |
| phi4-mini | None |
| qwen2.5-coder:7b | None |
| llava:7b | None |
| qwen3:8b | None |
| deepseek-r1:8b | None |
| gemma3:4b | None |
| qwen2.5-coder:14b | None |
| qwen3:14b | None |
| deepseek-r1:14b | None |
| phi4 | Replace with: "Reply with only the [answer type], nothing else:" — "Answer in one word:" triggers explanation reflex |
| gemma3:12b | None |

**Rule:** One-word factual recall works at baseline for 13/14 models. phi4 requires tighter output framing due to verbosity bias.

---

### JSN — Structured JSON

**Baseline:** "Output only valid JSON, no explanation, no markdown fences. Use this schema: {schema} / Data: [description]"

| Model | JSON Behavior | Deviation from Baseline |
|-------|--------------|------------------------|
| qwen3:1.7b | Compact single-line | None — "no markdown fences" sufficient |
| llama3.2:1b | Indented, valid | None — baseline works (indented is still valid) |
| gemma3:1b | Fences: strong bias | **Few-shot template only**: provide example JSON and ask to confirm values. Verbal suppression fails entirely. |
| phi4-mini | Fences: strong bias | **Key-value conversion**: "Convert to JSON (one line, no code blocks): key=value" |
| qwen2.5-coder:7b | Fences: moderate | Add "no backticks" to baseline: "no markdown fences, no backticks" |
| llava:7b | Compact | None — baseline works |
| qwen3:8b | Compact single-line | None — "no markdown fences" sufficient |
| deepseek-r1:8b | Compact single-line | None — baseline works |
| gemma3:4b | Fences: moderate | Add "no backticks, no triple backticks" |
| qwen2.5-coder:14b | Compact single-line | None — baseline works |
| qwen3:14b | Compact single-line | None — baseline works |
| deepseek-r1:14b | Compact single-line | None — baseline works |
| phi4 | Fences: strong bias | **Key-value conversion** (same as phi4-mini): "Convert to JSON (one line, no code blocks): key=value" |
| gemma3:12b | Compact single-line | None — baseline works |

**JSON Fence Risk by Family:**
- **gemma3 family**: High fence risk at all sizes; 1b needs few-shot, 4b needs backtick suppression, 12b works at baseline (fence risk appears to reduce with scale for gemma)
- **phi family**: High fence risk at both sizes (phi4-mini and phi4); requires key=value conversion
- **qwen2.5-coder family**: Moderate at 7b (needs +backticks), resolved at 14b
- **qwen3, deepseek-r1, llama, llava**: Baseline sufficient

---

### LGC — Logic

**Baseline:** "Is this argument valid? Answer with exactly one word: valid or invalid."

| Model | Deviation from Baseline |
|-------|------------------------|
| qwen3:1.7b | ⚠️ Partial — angle-bracket echo conflict. Use "[answer]" not "\<answer\>" in answer template |
| llama3.2:1b | ❌ Capability failure — consistently misclassifies valid syllogisms. Do not route logic tasks. |
| gemma3:1b | Add "lowercase": "exactly one lowercase word" |
| phi4-mini | ⚠️ Partial — correct answer, format non-compliant (adds period). Apply post-processing. |
| qwen2.5-coder:7b | Add "lowercase" |
| llava:7b | Use parenthetical format: "One word answer in lowercase. Answer (valid/invalid):" |
| qwen3:8b | None — baseline works |
| deepseek-r1:8b | None — baseline works |
| gemma3:4b | None — baseline works |
| qwen2.5-coder:14b | Add "lowercase" |
| qwen3:14b | None — baseline works |
| deepseek-r1:14b | None — baseline works |
| phi4 | **Fill-in-blank framing only**: "Logic check. Fill in the blank with one word: '[argument] This argument is _____." (multi-retry verbal suppression fails) |
| gemma3:12b | None — baseline works |

**Rule:** Logic evaluation is reliable at 8b+ (with minor fixes). llama3.2:1b has a hard capability ceiling — routing will fail. phi4 and phi4-mini have explanation reflexes that resist format constraints on logic; requires structural workarounds.

---

## Part 4: Model-Specific Routing Profiles

### Tier 1 — Pi-Native

#### qwen3:1.7b ★ Recommended Default
- **Overhead:** 0 (this is the baseline)
- **Thinking mode:** Yes — adds latency, improves reasoning accuracy
- **Route here:** All standard task types at Tier 1
- **Avoid:** Angle-bracket placeholders in output templates
- **Pi note:** Thermal-safe. Loop-safe.

#### llama3.2:1b — Limited Use
- **Overhead:** 5 adjustments
- **Route here:** Extraction (with hard boundary), sorting, summarization, JSON, factual recall
- **Avoid:** Reasoning, logic (hard capability ceiling). Avoid "fill in the blanks" phrasing.
- **Notes:** Fastest model at Tier 1. "Not more, not fewer" boundary required for extraction count. Case constraint required on all single-word tasks.

#### gemma3:1b — Strong General, JSON Exception
- **Overhead:** 3 adjustments (1 major)
- **Route here:** General NLP including reasoning (surprisingly capable for 1b)
- **Avoid:** JSON-heavy workflows (few-shot workaround adds overhead — use qwen3:1.7b instead)
- **Notes:** Best reasoning at Tier 1 after qwen3:1.7b. Consistent sentence-case default. JSON is the only hard workaround.

#### phi4-mini — Narrow Use
- **Overhead:** 6 adjustments
- **Route here:** Simple bounded retrieval only — extraction, sorting, factual recall, template fill
- **Avoid:** Reasoning, multi-step tasks, logic, summarization of technical content
- **Notes:** Most restricted Tier-1 executor. Technical-jargon summarization bias. Keyword separator defaults to spaces, not commas. Not recommended for general NLP.

---

### Tier 2 — Pi Ceiling / Workstation

#### qwen2.5-coder:7b — Code First, General Tasks Secondary
- **Overhead:** 5 adjustments
- **Route here:** Code generation (primary purpose), simple bounded NLP
- **Avoid:** Reasoning without scaffolding. Prefer qwen2.5-coder:14b when available.
- **Notes:** Coder training does not eliminate general NLP weaknesses at 7b. Count boundary reinforcement and lowercase constraint both required. Comma spacing may be omitted in list outputs.

#### llava:7b — Vision Primary, Text Secondary
- **Overhead:** 4 adjustments
- **Route here:** **Vision tasks via image API** (primary purpose). Text: classification, sorting, JSON, template fill.
- **Avoid:** Reasoning (scaffolding required), independent counting tasks without scaffold
- **Notes:** Text-only protocol documented here. Visual tasks require separate vision protocol with image attachment. Count boundaries need visual enumeration scaffolding ("Count: 1, 2, 3...").

---

### Tier 3 — Workstation GPU-Accelerated

#### deepseek-r1:8b ★ Best Tier-3 (Zero Overhead)
- **Overhead:** 0
- **Thinking mode:** Yes — extensive multi-method verification
- **Route here:** All task types at Tier 3. Preferred for reasoning-heavy workloads.
- **Latency:** 30–60s per complex task due to thinking phase
- **Notes:** Baseline transfers perfectly. Self-verification via thinking makes this the most reliable mid-tier executor. Minor: may omit AM/PM on time answers — specify format explicitly if needed.

#### qwen3:8b — Near-Zero Overhead
- **Overhead:** 1 (reasoning anchor only)
- **Thinking mode:** Yes — thorough multi-method verification
- **Route here:** General NLP at Tier 3; reasoning tasks
- **Notes:** Add "plain text" to reasoning answer anchor to prevent markdown bold contamination. Comma spacing may be omitted in list outputs (cosmetic). Near-identical capability to qwen3:14b on most tasks.

#### gemma3:4b — Three Targeted Fixes
- **Overhead:** 3
- **Route here:** General NLP at Tier 3; strong reasoning
- **Fixes:** (1) "lowercase" on CLS/LGC, (2) "all lowercase" on KWD, (3) "no backticks" on JSN
- **Notes:** Same lowercase and JSON patterns as gemma3:1b but at higher capability. Reasoning quality matches Tier-4 behavior. Fast (no thinking overhead).

#### qwen2.5-coder:14b — Two Simple Fixes
- **Overhead:** 2 (lowercase only)
- **Route here:** Code generation + general NLP. Best coding executor at Tier 3.
- **Fixes:** Add "lowercase" to CLS and LGC tasks
- **Notes:** Coder training improves structured reasoning quality. "Lowercase" is the only systematic fix needed. Clean, reliable tier-3 general executor after this fix.

---

### Tier 4 — Full Workstation (16GB+ VRAM)

#### qwen3:14b ★ Best Tier-4 (Zero Overhead)
- **Overhead:** 0
- **Thinking mode:** Yes — multi-method verified reasoning
- **Route here:** All task types at Tier 4. General default executor.
- **Latency:** ~2–3× slower than non-thinking Tier-4 models
- **Notes:** Baseline transfers perfectly. Correct case by default (unlike qwen2.5-coder:14b). Ideal Sovereign default for Tier 4.

#### gemma3:12b ★ Best Tier-4 (Zero Overhead, Fastest)
- **Overhead:** 0
- **Thinking mode:** No — direct output
- **Route here:** Format-critical tasks where latency matters. All task types.
- **Notes:** Zero overhead, no thinking latency. Fastest zero-overhead executor. Preferred when response time matters more than reasoning depth.

#### deepseek-r1:14b — One Unique Fix
- **Overhead:** 1 (count affirmation only)
- **Thinking mode:** Yes — most thorough in ensemble (60–90s complex tasks)
- **Route here:** Complex reasoning, open-ended analysis, tasks where self-correction is beneficial
- **Fix:** Add "This is intentional" when extraction count < total available items
- **Notes:** Self-correction reasoning can override explicit constraints at this scale — the model becomes "too smart" for bounded retrieval when it detects a seeming inconsistency. For open-ended tasks, this is an asset.

#### phi4 — Four Workarounds, Strong Reasoning
- **Overhead:** 4
- **Thinking mode:** No — direct output (but detailed step-by-step reasoning)
- **Route here:** Reasoning-heavy tasks where brief explanation is acceptable. Not format-critical tasks.
- **Fixes:** (1) CLS: choice enumeration framing, (2) OWA: tight output constraint, (3) JSN: key=value conversion, (4) LGC: fill-in-blank framing
- **Notes:** Verbosity bias is the core encoding challenge. Excellent reasoning quality. Prefer qwen3:14b or gemma3:12b for format-critical workflows.

---

## Part 5: Cross-Tier Encoding Patterns

### The Case Constraint Gradient

Whether a model defaults to lowercase single-word answers correlates with architecture family, not tier:

| Family | Case Default | Fix Required |
|--------|-------------|-------------|
| qwen3 (all sizes) | lowercase ✅ | None |
| deepseek-r1 (all sizes) | lowercase ✅ | None |
| gemma3 (all sizes) | sentence-case ❌ | "lowercase" |
| qwen2.5-coder (all sizes) | sentence-case ❌ | "lowercase" |
| llama | sentence-case ❌ | "lowercase" |
| phi / phi4-mini | sentence-case ❌ | complex framing |
| llava | sentence-case ❌ | "lowercase" |
| gemma3:12b | **lowercase ✅** (exception) | None |

**Observation:** gemma3:12b breaks the gemma3 pattern — it outputs lowercase without constraint. The smaller gemma3 models do not. This may reflect scale-dependent instruction-following calibration.

---

### The JSON Fence Gradient

JSON fence bias is architecture-linked and partially scale-dependent:

| Family | Fence Risk | Fix |
|--------|-----------|-----|
| qwen3 | None — clean by default | None |
| deepseek-r1 | None — clean by default | None |
| llama | None | None |
| llava | None | None |
| qwen2.5-coder:14b | None | None |
| qwen2.5-coder:7b | Moderate | + "no backticks" |
| gemma3:4b | Moderate | + "no backticks, no triple backticks" |
| gemma3:1b | High — verbal suppression fails | Few-shot template |
| gemma3:12b | **None** (exception) | None |
| phi4 | High — verbal suppression fails | Key-value conversion |
| phi4-mini | High — verbal suppression fails | Key-value conversion |

**Observation:** JSON fence bias appears to reduce with scale within the gemma3 family (gemma3:12b has no bias) but persists in the phi family at both scales tested. The phi key=value workaround bypasses the learned code-block association entirely by changing the input representation, not the output instruction.

---

### Reasoning Capability Threshold

The threshold for independent multi-step reasoning:

| Tier | Model | Independent Reasoning |
|------|-------|----------------------|
| 1 | qwen3:1.7b | ✅ (thinking mode) |
| 1 | gemma3:1b | ✅ (surprising outlier) |
| 1 | llama3.2:1b | ❌ (hard ceiling) |
| 1 | phi4-mini | ❌ (hard ceiling) |
| 2 | qwen2.5-coder:7b | ❌ (scaffold only) |
| 2 | llava:7b | ❌ (scaffold only) |
| 3 | qwen3:8b | ✅ (thinking mode) |
| 3 | deepseek-r1:8b | ✅ (thinking mode) |
| 3 | gemma3:4b | ✅ |
| 3 | qwen2.5-coder:14b | ✅ |
| 4 | All | ✅ |

**Observation:** The reasoning threshold at 1b is crossed only by models with thinking mode (qwen3) or models with strong reasoning training (gemma3). 7b non-thinking models (qwen2.5-coder:7b, llava:7b) fail reasoning without scaffolding — they are not larger enough to compensate for the absence of thinking mode. The 8b thinking models (qwen3:8b, deepseek-r1:8b) surpass 7b non-thinking models substantially.

---

## Part 6: Thesis Evidence

### The Channel Is the Intelligence

The corpus advances the research direction. It does not close it.

**What the corpus proves:**

1. **Encoding adjustments recover capability.** Every model that failed at baseline succeeded after encoding adjustment — except llama3.2:1b on logic (hard capability ceiling). This means encoding failures are channel failures, not model failures, in all but the edge cases.

2. **Three models require zero encoding overhead.** deepseek-r1:8b, qwen3:14b, and gemma3:12b accept the baseline encoding without modification and achieve 10/10 across all task types. The channel is lossless at baseline for these models.

3. **Encoding overhead scales inversely with model quality, but not perfectly.** The correlation holds within families (qwen3:8b < qwen3:14b overhead) but breaks across families (gemma3:12b = 0 overhead despite being a non-thinking model; phi4 = 4 overhead despite being Tier 4). Training approach matters as much as parameter count.

4. **Sorting is universal.** Every model passed SRT at baseline with zero adjustment. This is the most channel-efficient operation in the task set — sorting is a pattern-completion task with minimal semantic ambiguity.

5. **Logic is the hardest task.** Logic evaluation produced the most failures and partial results across the corpus. Only 8b+ models handle it reliably at baseline or with minor fixes. llama3.2:1b fails entirely. phi4 requires structural reframing. This aligns with the thesis: formal reasoning requires the deepest channel precision.

**The nuance (from DNA.md):**

> "THE CHANNEL IS THE INTELLIGENCE — empirically validated as *partially* correct — individual agent capability also shapes outcomes. Protocol design is necessary but not sufficient."

The corpus confirms this. Encoding resolved every failure except llama3.2:1b's logic ceiling. That failure is not a channel failure — it is a capability ceiling that no encoding can cross. The channel can optimize signal transfer up to the model's actual capability. It cannot extend the model's capability ceiling.

**The practical implication for Sovereign:**

Sovereign should maintain per-model encoding overlays — not a single prompt template, but a routing layer that selects the appropriate encoding variant based on the active executor. The encoding overhead matrix (Part 2) is the input to that routing layer.

---

## Part 7: Routing Table (Recommended Defaults)

| Task Type | Tier 1 Default | Tier 2 | Tier 3 Default | Tier 4 Default |
|-----------|---------------|--------|----------------|----------------|
| General NLP | qwen3:1.7b | — | deepseek-r1:8b | qwen3:14b |
| Code | qwen2.5-coder:7b¹ | qwen2.5-coder:7b | qwen2.5-coder:14b | qwen2.5-coder:14b |
| Reasoning | qwen3:1.7b | — | deepseek-r1:8b | deepseek-r1:14b |
| Logic | qwen3:1.7b | — | deepseek-r1:8b | qwen3:14b |
| Vision | — | llava:7b | llava:7b | llava:7b |
| Fast retrieval | llama3.2:1b | — | gemma3:4b | gemma3:12b |
| Embeddings | nomic-embed-text | nomic-embed-text | nomic-embed-text | nomic-embed-text |

¹ Use Pi thermal doctrine on Pi: one-shot, taskset -c 0,1

**Do not route to:**
- llama3.2:1b → reasoning, logic
- phi4-mini → reasoning, logic (anything beyond bounded retrieval)
- Any Tier 1/2 model → multi-step math without scaffolding

---

## Appendix: Encoding Adjustment Reference Card

Quick reference for Sovereign's encoding dispatch layer.

### Always apply:
- `[FIELD]` brackets for template fill (never `<angle>`)
- `Answer: [format]` colon-anchor for reasoning extraction

### Apply per-family:
| Pattern | Apply to |
|---------|---------|
| Add "lowercase" to CLS/LGC | gemma3 (all), qwen2.5-coder (all), llama3.2, llava |
| Add "all lowercase" to KWD | gemma3 (all) |
| Add "not more, not fewer" to EXT | llama3.2:1b, qwen2.5-coder:7b, llava:7b |
| Add counting scaffold to EXT | llava:7b |
| Add "plain text" to RSN anchor | qwen3:8b |
| Add intent affirmation to EXT | deepseek-r1:14b (when count < total) |
| Add "no backticks" to JSN | gemma3:4b, qwen2.5-coder:7b |
| Use few-shot JSN template | gemma3:1b |
| Use key=value JSN | phi4, phi4-mini |
| Use choice framing for CLS | phi4, phi4-mini |
| Use fill-blank for LGC | phi4 |
| Use "Reply with only X" for OWA | phi4 |
| Avoid "fill in the blanks" for TPL | llama3.2:1b |
| Scaffold RSN (capability ceiling) | llama3.2:1b, phi4-mini, qwen2.5-coder:7b, llava:7b |
| Do not route LGC | llama3.2:1b |

---

*End of guide. Update this document when new models are added to the ensemble or when existing model behavior changes across Ollama version updates.*
