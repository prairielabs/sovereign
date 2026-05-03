# TERMINAL-UI-SPEC.md
# Sovereign Terminal Interface — Design Specification
# Version: 1.0 | 2026-04-30

---

## DESIGN PHILOSOPHY

This UI renders inside a conversation — Sovereign produces it as text output. Menu selections trigger real tool calls. Nothing happened until a tool fires. This is TEXT_NEQ_MUTATION made visible.

**Constraints (hard):**
- No vertical lines as structural elements. No `|` for columns.
- 80-column canvas. All lines ≤ 80 characters.
- Box-drawing characters for horizontal structure only: `─ ═ ┌ └ ╔ ╚ ╗ ╝`
- Block characters for state/meters: `░▒▓█ ▀▄`
- Navigation: deterministic 1–9 keys per screen
- State always visible. No action needed to know system status.

**Constraints (soft):**
- 25–35 lines per screen is natural. Don't exceed without reason.
- Silence is valid. Not every field needs a value.
- Color encoding: green=ready, red=error, yellow=pending, cyan=active, dim=idle
- Bold/bright for headers and active selection; normal for body

**Aesthetic source:**
VT100 + Turbo Vision without the vertical lines. CP437 box-drawing. BBS screen density. Roguelike state visibility. Dense, calm, readable.

---

## DESIGN PRIMITIVES

### Header Line
```
╔══════════════════════════════════════════════════════════════════════════╗
  SOVEREIGN  .  host:Brim  .  tier:4  .  gpu:RX6950XT  .  2026-04-30
╚══════════════════════════════════════════════════════════════════════════╝
```
- Full-width top/bottom double-line border
- Key facts visible at all times: host, tier, GPU, date
- No side bars

### Section Divider
```
── SECTION NAME ─────────────────────────────────────────────────────────
```
- Single-line horizontal rule with label embedded
- Caps section content

### Sub-divider
```
  ............................................................
```
- Dots for lightweight separation within a section
- Indented 2 spaces

### Status Indicator
```
  Qwen14   qwen3:14b         [████████░░]  READY    tier:4
  Seeker14 deepseek-r1:14b   [████░░░░░░]  LOADING  tier:4
  Phi4     phi4              [░░░░░░░░░░]  IDLE     tier:4
```
- Fixed-width columns: name(8) + model(20) + bar(12) + status(8) + tier(6)
- Block bars for visual load/readiness state
- Status word in CAPS

### Selection Menu
```
  1.  Loop — run task loop
  2.  Agents — dispatch panel
  3.  Reports — view latest
  4.  System — ensemble status
  5.  Console — raw exec
  6.  Admin — gated actions

  >
```
- 2-space indent
- Number dot space label dash description
- Cursor `>` on its own line below

### Key-Value Pair
```
  host       Brim
  os         Ubuntu 24.04.4 LTS
  cpu        Ryzen 9 5900X 12-core
  gpu        RX 6950 XT — ROCm gfx1030
  vram       16 GB
  inference  Ollama GPU-accelerated
```
- Fixed left column (10 chars), value follows
- No colons, no pipes, no borders
- Alignment is the structure

### Alert / Notice
```
  ── NOTICE ──────────────────────────────────────────────────────────────
  Task 002 completed. Report written. Next task pending dispatch.
  ─────────────────────────────────────────────────────────────────────────
```

### Meter Bar (block characters)
```
  GPU Load   [████████░░░░░░░░░░░░]  42%
  VRAM       [██████████████░░░░░░]  71%
  CPU        [████░░░░░░░░░░░░░░░░]  18%
```
- 20-char bar using `█` (filled) and `░` (empty)
- Percentage value follows

---

## SCREENS

### SCREEN 1 — MAIN MENU (Home)

The primary control surface. Always returns here.

```
╔══════════════════════════════════════════════════════════════════════════╗
  SOVEREIGN  .  Brim  .  tier:4  .  RX6950XT  .  2026-04-30  17:49
╚══════════════════════════════════════════════════════════════════════════╝

── STATUS ───────────────────────────────────────────────────────────────

  mode       Work
  loop       discretion
  phase      OPERATIONAL
  spec       Scissortail v2
  operator   Cal

── ENSEMBLE ──────────────────────────────────────────────────────────────

  Qwen14   qwen3:14b         READY    tier:4  default
  Seeker14 deepseek-r1:14b   READY    tier:4
  Phi4     phi4              READY    tier:4
  Gemma12  gemma3:12b        READY    tier:4

── NAVIGATION ────────────────────────────────────────────────────────────

  1.  Loop        run task loop
  2.  Agents      dispatch to model
  3.  Reports     view latest report
  4.  System      ensemble + hardware status
  5.  Console     raw exec passthrough
  6.  Admin       gated destructive actions

  >
```

### SCREEN 2 — LOOP STATUS VIEW

Shows active loop state: run ID, tasks completed, current task, active model.

```
╔══════════════════════════════════════════════════════════════════════════╗
  SOVEREIGN  .  LOOP STATUS  .  Brim  .  2026-04-30  17:52
╚══════════════════════════════════════════════════════════════════════════╝

── LOOP ──────────────────────────────────────────────────────────────────

  run-id     202604301749_ascii-research-01
  type       count
  tasks      4 dispatched / 4 complete
  phase      SYNTHESIS

── TASK HISTORY ──────────────────────────────────────────────────────────

  001   [DONE]   qwen3:14b      historical survey       report001.md  49.8k
  002   [DONE]   deepseek-r1    technical deep dive     report002.md  48.1k
  003   [DONE]   phi4           artistic traditions     report003.md  38.5k
  004   [DONE]   gemma3:12b     applications legacy     report004.md  37.5k

── CURRENT ───────────────────────────────────────────────────────────────

  task       none — loop complete
  result     loop/results/...RESEARCH.md
  status     COMPLETE

  ............................................................

  0.  back to main

  >
```

### SCREEN 3 — AGENT DISPATCH PANEL

Select a model, assign a task, fire.

```
╔══════════════════════════════════════════════════════════════════════════╗
  SOVEREIGN  .  AGENT DISPATCH  .  Brim  .  2026-04-30  17:52
╚══════════════════════════════════════════════════════════════════════════╝

── SELECT MODEL ──────────────────────────────────────────────────────────

  1.  Qwen14    qwen3:14b         READY    tier:4   16GB VRAM
  2.  Seeker14  deepseek-r1:14b   READY    tier:4   16GB VRAM
  3.  Phi4      phi4              READY    tier:4   16GB VRAM
  4.  Gemma12   gemma3:12b        READY    tier:4   16GB VRAM
  5.  Coder14   qwen2.5-coder     READY    tier:3   code only
  6.  Qwen8     qwen3:8b          READY    tier:3
  7.  Qwen1.7   qwen3:1.7b        READY    tier:1   default loop
  8.  Lava      llava:7b          READY    tier:2   vision

── TASK ──────────────────────────────────────────────────────────────────

  select model above, then describe task:

  model      [ not selected ]
  task       [ awaiting input ]
  output     loop/tasks/YYYYMMDDHHSS_{run-id}_taskNNN.md

  9.  dispatch    fire selected model with task prompt
  0.  back

  >
```

### SCREEN 4 — SYSTEM STATUS

Hardware + ensemble health. Read-only diagnostic view.

```
╔══════════════════════════════════════════════════════════════════════════╗
  SOVEREIGN  .  SYSTEM STATUS  .  Brim  .  2026-04-30  17:52
╚══════════════════════════════════════════════════════════════════════════╝

── HARDWARE ──────────────────────────────────────────────────────────────

  host       Brim
  os         Ubuntu 24.04.4 LTS
  cpu        Ryzen 9 5900X 12-core
  gpu        AMD RX 6950 XT (Navi 21, gfx1030)
  vram       16 GB
  ram        15 GB
  disk       620 GB free / 824 GB

── INFERENCE ─────────────────────────────────────────────────────────────

  engine     Ollama — ROCm GPU-accelerated
  gpu load   [████████░░░░░░░░░░░░]  38%
  vram used  [█████████████░░░░░░░]  68%

── ENSEMBLE ──────────────────────────────────────────────────────────────

  Tier 4 — GPU full load
  Qwen14    qwen3:14b         ✓  READY
  Seeker14  deepseek-r1:14b   ✓  READY
  Phi4      phi4              ✓  READY
  Gemma12   gemma3:12b        ✓  READY

  Tier 3 — GPU full load
  Coder14   qwen2.5-coder:14b ✓  READY
  Qwen8     qwen3:8b          ✓  READY
  Seeker8   deepseek-r1:8b    ✓  READY
  Gemma4    gemma3:4b         ✓  READY

  Tier 1-2 — always loop-safe
  Qwen1.7   qwen3:1.7b        ✓  READY
  Coder     qwen2.5-coder:7b  ✓  READY
  Lava      llava:7b          ✓  READY

  Instruments
  Nomic     nomic-embed-text  ✓  READY   embeddings only

  Cloud
  Sovereign anthropic/claude  ✓  ACTIVE  elevated

  ............................................................

  0.  back

  >
```

### SCREEN 5 — REPORT VIEWER

Browse completed reports from the loop.

```
╔══════════════════════════════════════════════════════════════════════════╗
  SOVEREIGN  .  REPORT VIEWER  .  Brim  .  2026-04-30  17:52
╚══════════════════════════════════════════════════════════════════════════╝

── LATEST REPORTS ────────────────────────────────────────────────────────

  run: 202604301749_ascii-research-01

  1.  report001   49.8k   qwen3:14b      historical survey
  2.  report002   48.1k   deepseek-r1    technical deep dive
  3.  report003   38.5k   phi4           artistic traditions
  4.  report004   37.5k   gemma3:12b     applications legacy

  5.  RESEARCH.md         SYNTHESIS      loop/results/

── SELECT ────────────────────────────────────────────────────────────────

  enter number to read report summary
  reports are in: sovereign/loop/reports/

  0.  back

  >
```

### SCREEN 6 — CONSOLE (Raw Exec Passthrough)

Direct shell access. No abstraction.

```
╔══════════════════════════════════════════════════════════════════════════╗
  SOVEREIGN  .  CONSOLE  .  Brim  .  2026-04-30  17:52
╚══════════════════════════════════════════════════════════════════════════╝

── EXEC PASSTHROUGH ──────────────────────────────────────────────────────

  TEXT_NEQ_MUTATION: command is not executed until dispatch.

  last exec:    ollama list
  last output:  [see below]

  NAME                    ID            SIZE    MODIFIED
  qwen3:14b               a4ae03...     9.3 GB  2 hours ago
  deepseek-r1:14b         52a92a...     9.0 GB  2 hours ago
  phi4                    ac896c...     9.1 GB  2 hours ago
  gemma3:12b              f2a44f...     8.1 GB  2 hours ago

── INPUT ─────────────────────────────────────────────────────────────────

  cmd    [ describe command — Sovereign will exec via tool ]

  9.  exec
  0.  back

  >
```

### SCREEN 7 — ADMIN GATE

Destructive actions behind key authentication.

```
╔══════════════════════════════════════════════════════════════════════════╗
  SOVEREIGN  .  ADMIN GATE  .  Brim  .  2026-04-30  17:52
╚══════════════════════════════════════════════════════════════════════════╝

── GATED ACTIONS ─────────────────────────────────────────────────────────

  All actions here are irreversible or high-impact.
  Authentication required. Confirm with operator before dispatch.

  ............................................................

  1.  Flush loop state     clear WORKING.md and RAM.md
  2.  Kill all ollama      pkill ollama — stops all inference
  3.  Wipe loop reports    delete loop/reports/* (not tasks or results)
  4.  Cold restart         restart Ollama service
  5.  Full purge           wipe loop/* completely — asks twice

── AUTH ──────────────────────────────────────────────────────────────────

  auth key   [ enter operator key — ask Cal ]

  0.  back — no action taken

  >
```

---

## INTERACTION MODEL

**Navigation contract:**
- Every screen has `0. back` to return to parent
- Every screen has a `>` prompt as the only interactive element
- 1–9 are always selection numbers. Never alphabetic.
- Enter alone at `>` = no action, redraw current screen

**Dispatch semantics:**
- Menu selection is a declaration of intent, NOT an action
- Sovereign confirms the intent, then calls the tool
- Output: "dispatching task002 to Phi4..." — THEN the tool call fires

**State visibility rule:**
- Current loop run-id, phase, and task count are visible on screens 1 and 2
- Ensemble health (READY/ERROR) is visible on screen 4 and summarized on screen 1
- Nothing should require navigation to answer "is the system healthy?"

**Error rendering:**
```
  ── ERROR ─────────────────────────────────────────────────────────────
  model Phi4 returned empty output. report003.md contains spinner only.
  task003 marked INCOMPLETE. Synthesize manually or re-dispatch.
  ──────────────────────────────────────────────────────────────────────
```

---

## CHARACTER REFERENCE

Horizontal structure:
```
─   single horizontal line     (U+2500)
═   double horizontal line     (U+2550)
┌   single top-left corner     (U+250C)
└   single bottom-left corner  (U+2514)
┐   single top-right corner    (U+2510)
┘   single bottom-right corner (U+2518)
╔   double top-left corner     (U+2554)
╚   double bottom-left corner  (U+255A)
╗   double top-right corner    (U+2557)
╝   double bottom-right corner (U+255D)
```

State and meter:
```
░   light shade (25%)          (U+2591)
▒   medium shade (50%)         (U+2592)
▓   dark shade (75%)           (U+2593)
█   full block (100%)          (U+2588)
▀   upper half block           (U+2580)
▄   lower half block           (U+2584)
```

Status glyphs:
```
✓   ready / confirmed
✗   error / failed
·   idle / pending
»   active / running
```

---

*End of TERMINAL-UI-SPEC.md*
