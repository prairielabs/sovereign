# SCREENS.md
# Sovereign Terminal Interface — Rendered Example Screens
# 2026-04-30

These are live-renderable screens. Sovereign outputs these as text during a conversation. Menu selections trigger real tool calls.

---

## SCREEN 1 — MAIN MENU

```
╔══════════════════════════════════════════════════════════════════════════╗
  SOVEREIGN  .  Brim  .  tier:4  .  RX6950XT/16GB  .  2026-04-30  17:52
╚══════════════════════════════════════════════════════════════════════════╝

── STATUS ───────────────────────────────────────────────────────────────

  mode       Work
  loop       discretion
  phase      OPERATIONAL
  spec       Scissortail v2
  operator   Cal

── ENSEMBLE (summary) ────────────────────────────────────────────────────

  Tier 4     Qwen14   Seeker14   Phi4   Gemma12    all READY
  Tier 3     Coder14  Qwen8      all READY
  Tier 1-2   Qwen1.7  Coder  Lava    all READY
  Cloud      Sovereign (claude-sonnet-4-6)   ACTIVE

── NAVIGATE ──────────────────────────────────────────────────────────────

  1.  Loop        run task loop
  2.  Agents      dispatch to model
  3.  Reports     view latest report
  4.  System      ensemble and hardware status
  5.  Console     raw exec passthrough
  6.  Admin       gated destructive actions

  >
```

---

## SCREEN 2 — LOOP STATUS

*Shown mid-run with 2 of 4 tasks complete, task 3 active:*

```
╔══════════════════════════════════════════════════════════════════════════╗
  SOVEREIGN  .  LOOP STATUS  .  Brim  .  2026-04-30  17:52
╚══════════════════════════════════════════════════════════════════════════╝

── LOOP ──────────────────────────────────────────────────────────────────

  run-id     202604301749_ascii-research-01
  type       count (4 tasks)
  progress   3 of 4 complete
  phase      RUNNING — task 004 dispatched

── TASK LEDGER ───────────────────────────────────────────────────────────

  001   [DONE]   qwen3:14b         historical survey         49.8k  1:03
  002   [DONE]   deepseek-r1:14b   technical deep dive       48.1k  0:58
  003   [DONE]   phi4              artistic traditions       38.5k  1:12
  004   [RUN » ] gemma3:12b        applications and legacy   ----   ----

── ACTIVE TASK ───────────────────────────────────────────────────────────

  task       004 — applications and legacy
  model      gemma3:12b
  started    17:52:14
  elapsed    0:04:22
  output     loop/reports/...report004.md

  ............................................................

  No action needed. Task is running.

  0.  back to main

  >
```

---

## SCREEN 3 — AGENT DISPATCH PANEL

*With Qwen14 selected, task entered, ready to fire:*

```
╔══════════════════════════════════════════════════════════════════════════╗
  SOVEREIGN  .  AGENT DISPATCH  .  Brim  .  2026-04-30  17:52
╚══════════════════════════════════════════════════════════════════════════╝

── SELECT MODEL ──────────────────────────────────────────────────────────

  1.  Qwen14    qwen3:14b         READY    tier:4
  2.  Seeker14  deepseek-r1:14b   READY    tier:4
  3.  Phi4      phi4              READY    tier:4
  4.  Gemma12   gemma3:12b        READY    tier:4
  5.  Coder14   qwen2.5-coder:14b READY    tier:3   code tasks only
  6.  Qwen8     qwen3:8b          READY    tier:3
  7.  Qwen1.7   qwen3:1.7b        READY    tier:1   loop-safe default
  8.  Lava      llava:7b          READY    tier:2   vision

── TASK ──────────────────────────────────────────────────────────────────

  model      Qwen14 (qwen3:14b)   [selected]
  task       Write a haiku about the three-body problem.
  output     loop/tasks/20260430..._taskNNN.md

  ............................................................

  9.  dispatch    fire — writes task file and calls ollama
  0.  back — no action taken

  >
```

---

## SCREEN 4 — SYSTEM STATUS

```
╔══════════════════════════════════════════════════════════════════════════╗
  SOVEREIGN  .  SYSTEM STATUS  .  Brim  .  2026-04-30  17:52
╚══════════════════════════════════════════════════════════════════════════╝

── HARDWARE ──────────────────────────────────────────────────────────────

  host       Brim
  os         Ubuntu 24.04.4 LTS
  cpu        AMD Ryzen 9 5900X  12-core  3.7GHz
  gpu        AMD RX 6950 XT  Navi21  gfx1030  ROCm
  vram       16 GB
  ram        15 GB
  disk       620 GB free / 824 GB total

── INFERENCE ─────────────────────────────────────────────────────────────

  engine     Ollama 0.3.x  GPU-accelerated
  gpu load   [████████░░░░░░░░░░░░]  42%
  vram       [█████████████░░░░░░░]  68%   10.9 GB / 16 GB
  cpu        [████░░░░░░░░░░░░░░░░]  18%

── ENSEMBLE ──────────────────────────────────────────────────────────────

  Tier 4 — full GPU, 16GB VRAM
  Qwen14    qwen3:14b         ✓  READY    9.3 GB
  Seeker14  deepseek-r1:14b   ✓  READY    9.0 GB
  Phi4      phi4              ✓  READY    9.1 GB
  Gemma12   gemma3:12b        ✓  READY    8.1 GB

  Tier 3 — GPU, fits with swap
  Coder14   qwen2.5-coder:14b ✓  READY    9.0 GB
  Qwen8     qwen3:8b          ✓  READY    5.2 GB
  Seeker8   deepseek-r1:8b    ✓  READY    4.9 GB
  Gemma4    gemma3:4b         ✓  READY    3.3 GB

  Tier 1-2 — always loop-safe
  Qwen1.7   qwen3:1.7b        ✓  READY    1.9 GB   default
  Coder7    qwen2.5-coder:7b  ✓  READY    4.7 GB
  Lava7     llava:7b          ✓  READY    4.7 GB   vision

  Instruments
  Nomic     nomic-embed-text  ✓  READY    embeddings only

  Cloud
  Sovereign claude-sonnet-4-6 ✓  ACTIVE   elevated — this session

  ............................................................

  0.  back

  >
```

---

## SCREEN 5 — LOOP LAUNCH

*Sovereign prompts to start a new loop run:*

```
╔══════════════════════════════════════════════════════════════════════════╗
  SOVEREIGN  .  NEW LOOP  .  Brim  .  2026-04-30  17:52
╚══════════════════════════════════════════════════════════════════════════╝

── CONFIGURE LOOP ────────────────────────────────────────────────────────

  Loop type:
  1.  count       run exactly N tasks then stop
  2.  duration    run for time T then stop
  3.  discretion  run until problem is solved (Sovereign decides)
  4.  open        run indefinitely until interrupted

  Problem statement:
  [ describe the problem — Sovereign writes the solution, then dispatches ]

  ............................................................

  TEXT_NEQ_MUTATION: no loop starts until dispatch is confirmed.

  9.  confirm and launch
  0.  back — no action

  >
```

---

## SCREEN 6 — ERROR STATE

*When a model produces no output or errors:*

```
╔══════════════════════════════════════════════════════════════════════════╗
  SOVEREIGN  .  LOOP STATUS  .  Brim  .  2026-04-30  17:53
╚══════════════════════════════════════════════════════════════════════════╝

── LOOP ──────────────────────────────────────────────────────────────────

  run-id     202604301749_ascii-research-01
  phase      ERROR — manual intervention required

── ERROR ─────────────────────────────────────────────────────────────────

  task       003
  model      phi4
  problem    report003.md contains only terminal spinner output
             file has 38.5k bytes but 0 readable lines
             model likely consumed output before write

  report003 status    INCOMPLETE
  loop status         PAUSED

── OPTIONS ───────────────────────────────────────────────────────────────

  1.  re-dispatch task003    fire phi4 again with same prompt
  2.  swap model             assign task003 to different model
  3.  skip and continue      mark 003 as failed, continue loop
  4.  synthesize manually    Sovereign writes report003 directly
  5.  abort loop             terminate run, write partial results

  0.  back

  >
```

---

## SCREEN 7 — ADMIN GATE

```
╔══════════════════════════════════════════════════════════════════════════╗
  SOVEREIGN  .  ADMIN GATE  .  Brim  .  2026-04-30  17:52
╚══════════════════════════════════════════════════════════════════════════╝

── WARNING ───────────────────────────────────────────────────────────────

  Actions on this screen are irreversible or high-impact.
  Confirm with Cal before proceeding. Key required.

── ACTIONS ───────────────────────────────────────────────────────────────

  1.  flush state    clear WORKING.md and RAM.md
  2.  kill ollama    pkill ollama — stops all running inference
  3.  wipe reports   delete loop/reports/* (not tasks or results)
  4.  restart        ollama service restart
  5.  full purge     wipe loop/* entirely — asks twice

── AUTH ──────────────────────────────────────────────────────────────────

  key        [ operator key — ask Cal ]

  confirm:   "CONFIRM action-name" to proceed

  0.  back — no action taken

  >
```

---

## SCREEN 8 — MAIN MENU (revised 2026-04-30 pm)

```
╔══════════════════════════════════════════════════════════════════════════╗
  SOVEREIGN  .  Brim  .  tier:4  .  RX6950XT/16GB  .  2026-04-30  23:01
╚══════════════════════════════════════════════════════════════════════════╝

── STATUS ───────────────────────────────────────────────────────────────

  mode       Work
  loop       discretion
  phase      OPERATIONAL
  spec       Scissortail v2
  operator   Cal

── ENSEMBLE ─────────────────────────────────────────────────────────────

  Tier 4     Qwen14  Seeker14  Phi4  Gemma12    all READY
  Cloud      Sovereign (claude-sonnet-4-6)       ACTIVE

── NAVIGATE ──────────────────────────────────────────────────────────────

  1.  Loop          run task loop
  2.  Agents        dispatch to model
  3.  Reports       view latest report
  4.  System        ensemble and hardware status
  5.  Install       model install and ensemble management
  6.  Console       raw exec passthrough
  7.  Admin         gated destructive actions

  >
```

---

## SCREEN 9 — INSTALL PANEL

```
╔══════════════════════════════════════════════════════════════════════════╗
  SOVEREIGN  .  INSTALL  .  Brim  .  2026-04-30  23:01
╚══════════════════════════════════════════════════════════════════════════╝

── INSTALLED ─────────────────────────────────────────────────────────────

  Tier 1
  ✓  llama3.2:1b           1.3 GB    Llama
  ✓  gemma3:1b             815 MB    Gemma
  ✓  qwen3:1.7b            1.9 GB    Qwen       default
  ✓  phi4-mini             2.5 GB    Phi

  Tier 2
  ✓  qwen2.5-coder:7b      4.7 GB    Coder
  ✓  llava:7b              4.7 GB    Lava       vision

  Tier 3
  ✓  qwen3:8b              5.2 GB    Qwen8
  ✓  deepseek-r1:8b        4.9 GB    Seeker8
  ✓  gemma3:4b             3.3 GB    Gemma4
  ✓  qwen2.5-coder:14b     9.0 GB    Coder14

  Tier 4
  ✓  qwen3:14b             9.3 GB    Qwen14     default
  ✓  deepseek-r1:14b       9.0 GB    Seeker14
  ✓  phi4                  9.1 GB    Phi4
  ✓  gemma3:12b            8.1 GB    Gemma12

  Instruments
  ✓  nomic-embed-text      274 MB    Nomic

  ............................................................
  total installed    15 models    80.3 GB

── ACTIONS ───────────────────────────────────────────────────────────────

  1.  pull model       ollama pull <name>
  2.  remove model     ollama rm <name>
  3.  verify ensemble  test all installed models with ping task
  4.  set default      change default model for a tier
  5.  set active tier  switch loop to tier 1 / 2 / 3 / 4

── AVAILABLE (not installed) ─────────────────────────────────────────────

  --  qwen3:30b          19.7 GB    requires 24GB+ VRAM
  --  deepseek-r1:32b    20.0 GB    requires 24GB+ VRAM
  --  llava:13b           8.0 GB    vision, higher detail

  0.  back

  >
```

---

## DESIGN NOTES FOR IMPLEMENTATION

**Line width management:**
Every line in the screens above is ≤ 80 characters. To verify: the header line `╔══...══╗` is exactly 76 characters of `═` between corners = 78 chars total. Check rendered output with `| wc -c` per line.

**Color encoding (when implementing in an actual terminal):**
- ANSI `\x1b[1;37m` = bright white — headers, active labels
- ANSI `\x1b[0;37m` = normal gray — body text
- ANSI `\x1b[1;32m` = bright green — READY, DONE, ✓
- ANSI `\x1b[1;31m` = bright red — ERROR, ✗
- ANSI `\x1b[1;33m` = bright yellow — PENDING, running indicators
- ANSI `\x1b[1;36m` = bright cyan — active selection, » markers
- ANSI `\x1b[0;90m` = dark gray — dim labels, dotted separators
- ANSI `\x1b[0m` = reset

**When Sovereign renders these in-conversation:**
No ANSI codes — plain text only. The structure is conveyed by the box characters and alignment alone. The design works without color; color is an enhancement for a proper terminal renderer.

**The `>` prompt:**
When Sovereign renders a screen in conversation, the `>` is the literal prompt that the user types into next. Their reply is the menu selection. Sovereign parses it and executes.

---

*End of SCREENS.md*
