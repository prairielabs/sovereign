# Sovereign

**A multi-agent system written in Markdown.**

```
The folder is the system.
The constitution is a file.
The protocol is a file naming convention.
The state is what's on disk.
Reboot the machine, re-open the folder, the system resumes.
```

Sovereign is the conducting layer of an ensemble of language models.
A frontier model (the Sovereign) receives meaning from the user,
resolves it into discrete tasks, and dispatches each task to a local
executor — a small model that doesn't think, just executes. The
executor reports back. The Sovereign reads the report and generates
the next task. The loop runs until the problem is exhausted.

This was built on a **Raspberry Pi 5** with **$0.00 of cloud
inference** and produced — among other things — a 414-note orchestral
piece, a Schwarzschild-metric black hole rendered from first principles,
the Chenciner-Montgomery figure-8 three-body orbit, and a working
multi-agent ensemble that survives model swaps without code changes.

---

## What this repo contains

```
LICENSE         → CC BY 4.0.
DNA.md          → the constitution. Read first. Always.
AGENTS.md       → boot protocol — what to load on session start.
WORKING.md      → durable state. Written before shutdown, read at boot.
RAM.md          → volatile scratchpad. Flushed each session.
PULSE.md        → 30-minute watchdog config (thermal + zombie cleanup).
INSTALLER.md    → install runbook. Tell Claude to read this to set up.
DOCTOR.md       → diagnostic runbook. Tell Claude to read this when something is wrong.

SOUL.md         → OpenClaw bootstrap stub — redirects to DNA.md.
TOOLS.md        → operator-specific tool notes (optional).
IDENTITY.md     → instance name, vibe (operator-managed).
USER.md         → operator profile (operator-managed).
HEARTBEAT.md    → empty by design — heartbeat is in PULSE.md.

scissortail/    → SCISSORTAIL.md — the spec language used by DNA.md.
agents/         → the ensemble: 6 local executor cards.
                  Coder.md  Gemma.md  Lava.md  Llama.md  Phi.md  Qwen.md
ensemble/       → status descriptors for the runtime (Ollama, OpenClaw, APIs).
loop/           → the task/report protocol — the verb of the system:
                  problems/ solutions/ tasks/ reports/ results/
                  questions/ answers/   (frontier-executor Q&A slots)
apps/           → three productized prompt-systems for Claude:
                  Mozart.txt    — music production
                  Savannah.txt  — animation
                  Spur.txt      — image generation
docs/           → architecture overview, thermal doctrine, theory.
memory/         → durable memory archive.
data/           → curated artifacts from real runs.
projects/       → user-specific work bins.
```

---

## The thesis

Software is mostly **structure**. Multi-agent systems are mostly
**protocol**. Both can be written declaratively in Markdown and
loaded into a model's context as a runtime.

> **The folder IS the system.**

The constitution lives in `DNA.md`. It's read at the start of every
session. The active state lives in `WORKING.md` (durable, written before
shutdown) and `RAM.md` (volatile, flushed each session). The work happens
in the `loop/` — `.md` files routed through directories deterministically.
There is no state machine. There is no runtime. There is the model,
reading the folder, doing the work.

This applies Shannon-Weaver communication theory as software
architecture: if **the channel is the intelligence**, then optimizing
the protocol between Sovereign and its executors should matter more
than optimizing the model weights. That is the hypothesis.
This system is the investigation.

Read `docs/architecture.md` for the long version.

---

## How to run it

There is no build step. There is no installer binary.

1. Pick a workspace location. e.g., `~/sovereign/`.
2. Copy the contents of this repo into it.
3. Open a Claude session in the workspace and tell it to read `INSTALLER.md`.

That is the entire installation procedure. The installer asks the
questions it needs to ask, pulls the local ensemble, seeds the
workspace, installs PULSE, and runs a smoke test. When it leaves,
Sovereign is alive.

### What "open a Claude session in the workspace" means

Any Claude environment with file-system access works. Verified or expected:

| Runtime | Notes |
|---|---|
| **OpenClaw** | Native fit. Point its workspace at this folder; bootstrap files (`AGENTS.md`, `SOUL.md`, `TOOLS.md`, `IDENTITY.md`, `USER.md`, `HEARTBEAT.md`) are present and minimal. Sovereign was developed in this environment. |
| **Claude Code** | Open the folder, message Claude, say "read `INSTALLER.md`." |
| **Anthropic API + tool use** | Wire up filesystem read/write tools and shell. Same flow. |

The system requires Linux + Ollama + Python 3 on the host where executors run. The Sovereign session itself can run anywhere Claude runs.

## When something breaks

Tell Claude to read `DOCTOR.md`. The doctor does a physician's
examination — chief complaint, history, vitals, exam, differential,
diagnosis, treatment — and writes the visit to `WORKING.md`.

---

## Hardware

Sovereign was developed on a **Raspberry Pi 5 / 16 GB / 4-core ARM /
no GPU / no active cooling**. The thermal doctrine in `docs/` describes
how 7B-parameter models run sustainably on this hardware via core
restriction (passive heat-sinking from inactive cores). The thesis:
**frontier-class local inference is reachable on a Pi via thermal
management alone.**

It runs anywhere Linux + Ollama runs. The Pi was the proof.

---

## License

**CC BY 4.0** — Creative Commons Attribution 4.0 International.

Free to use, modify, redistribute, build on, including commercially.
Attribution required.

See `LICENSE`.

---

## Reading order

If you only read three files, read these:

1. **`DNA.md`** — the constitution.
2. **`docs/architecture.md`** — the why.
3. **`scissortail/SCISSORTAIL.md`** — the spec language the DNA is written in.

Everything else expands on those.

---

*"This is the research avenue."*
