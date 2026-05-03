# Architecture

The shape of Sovereign, and why it has that shape.

---

## 1. Two roles

There are two roles in the system.

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│        SOVEREIGN  ─→  task  ─→  EXECUTOR                 │
│                                       │                  │
│                                    report                │
│                                       ↓                  │
│        SOVEREIGN  ←─────────────  EXECUTOR               │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

**Sovereign** is the conductor. A frontier model. It reads context,
resolves meaning, and dispatches discrete units of work.

**Executor** is the limb. A small local model — usually 1B–7B
parameters. It takes a task, executes it, writes a report. It does
not think about the larger problem. It does not generate its own work.
It is blind to all prior tasks.

Sovereign generates the next task by reading the report of the previous
one. There is no plan ahead of time. Each task emerges from the state
created by the report of the one before it.

This is the **task loop**. It is the only shape of work in the system.

---

## 2. The folder is the system

```
~/sovereign/
├── README.md       ← entry point
├── LICENSE
├── DNA.md          ← constitution, read first
├── AGENTS.md       ← boot protocol
├── WORKING.md      ← durable state, written before shutdown
├── RAM.md          ← volatile scratchpad, flushed each session
├── PULSE.md        ← watchdog config (cron-driven, every 30 min)
├── INSTALLER.md    ← install runbook
├── DOCTOR.md       ← diagnostic runbook
├── SOUL.md, TOOLS.md, IDENTITY.md, USER.md, HEARTBEAT.md   ← OpenClaw bootstrap stubs
├── scissortail/    ← the spec language used by DNA.md
├── agents/         ← one card per executor (Coder, Gemma, Lava, Llama, Phi, Qwen)
├── ensemble/       ← runtime status (apis, ollama, openclaw)
├── loop/           ← the protocol
│   ├── problems/   ← user requests, framed
│   ├── solutions/  ← Sovereign's direction (not a plan)
│   ├── tasks/      ← discrete units of work
│   ├── reports/    ← executor outputs
│   ├── results/    ← final synthesized outputs
│   ├── questions/  ← frontier-executor questions to Sovereign
│   └── answers/    ← Sovereign's responses
├── apps/           ← productized capabilities (Mozart, Savannah, Spur)
├── memory/         ← durable memory archive
├── data/           ← curated artifacts from real runs
└── projects/       ← user-specific work bins
```

The folder structure is not metadata about the system. It **is** the
system. There is no database, no message queue, no state machine. Every
piece of state is a `.md` file in a named folder. State transitions
are file moves and writes.

This has consequences:

- **Reboot the machine, re-open the folder, the system resumes.**
- **Two agents can share a superstructure** by reading the same folder.
- **A task that leaves no file in `loop/tasks/` did not happen.**
- The system can be inspected with `ls`, `cat`, `grep`. Debugging is
  reading files.

---

## 3. The constitution

`DNA.md` is loaded into the agent's context at the start of every
session. It is the agent's constitution. It defines:

- **Identity** — name, role, what the agent is.
- **Axioms** — non-negotiable principles (TEXT ≠ MUTATION, DEFAULT DENY,
  FOLDER STATE IS SYSTEM STATE, etc).
- **Loop types** — count, duration, indefinite, discretion, oneshot.
- **Modes** — Work, ML, Hybrid.
- **Spawn protocol** — how children inherit constitution.
- **Memory** — what's durable, what's volatile, what's promoted.

`DNA.md` is written in **Scissortail** — a declarative spec language
where the model itself is the runtime. There is no compiler. The
structure of the spec creates gravity wells in the model's behavior
through precision of definition.

See `scissortail/SCISSORTAIL.md` for the language specification.

---

## 4. The channel is the intelligence

The central hypothesis:

> Multi-agent intelligence may live less in any one model's weights
> than in the protocol — the channel — between agents.

This is **Shannon-Weaver semantic communication theory** applied
as architecture. It is a direction, not a settled claim. Weaver's 1949 framing identified three problems:

- **Engineering** — can the signal arrive?
- **Semantic** — does it carry the intended meaning?
- **Effectiveness** — does the receiver act as desired?

Sovereign treats the Sovereign→Executor link as a Weaver semantic
channel. Each task is a transmission. Each report is an
acknowledgement. Sovereign learns to encode tasks such that the
executor receives what Sovereign meant.

This is **channel ML** — optimization not of model weights but of the
prompting protocol that connects two models.

A multi-hour, multi-cycle drill of exactly this is preserved in the
project archives. It shows that the prompting structure between
Sovereign and a small executor measurably shifts over time —
yielding more reliable output from a fixed local model with no
fine-tuning. Whether this constitutes semantic channel optimization
in the Shannon-Weaver sense is the question the research avenue pursues.


---

## 5. The thermal doctrine

Hardware constrains software. Sovereign was developed on a **Raspberry
Pi 5 / 16 GB / 4-core ARM / no GPU / no active cooling**.

Empirical findings:

- **Thermal pinning works as a passive heatsink.** Restricting an
  inference runner to one or two cores lets the inactive cores absorb
  heat. A 7B model on 1 core holds at 80–83 °C indefinitely. On 4
  cores, the same model spikes and throttles.
- **More cores = distributed heat = lower peak temperature** during a
  short burst.
- **One Tier 1 model in RAM at a time.** OOM kills are common when
  multiple small models are concurrent on a 16 GB Pi.
- **`taskset` on the Ollama CLI client does not pin the runner.** The
  runner is spawned by the Ollama server (different PID). To pin
  inference, taskset the server at startup.
- **Watchdog at 86 °C.** A 30-minute cron (`PULSE.md`) monitors temp,
  cleans zombie runners, snapshots state.

The thesis: **frontier-class local inference is reachable on a Pi via
thermal management alone.** No GPU required. No active cooling required.

---

## 6. Mathematical instantiation

A separate doctrine, but worth recording:

When modeling physical or mathematical phenomena, **derive every
visible element from the equations**. Not visualization. Not artistic
interpretation. Direct rendering of mathematical objects from
first-principle equations.

Examples from the Sovereign field record:

- **Black hole render** — Schwarzschild metric → null geodesics →
  gravitational lensing. Doppler shift from orbital velocity. Color
  from blackbody temperature. The image *is* the math.
- **Three-body figure-8** — Chenciner-Montgomery 2000. Velocity Verlet
  integration of Newton's law. The shape emerges from physics.
- **Burning Ship fractal** — actual `|Re(z)| + i|Im(z)|` iteration.

Provenance matters. Every render notes the theorem or paper behind it.

The equation IS the artwork. The render is the truth.

---

## 7. What's missing from this document

This is the architecture. It is not the operational manual; that lives in `DNA.md`.

For implementation details, read the source. The whole repo is < 200 KB
of human-readable Markdown. There is nothing hidden.
