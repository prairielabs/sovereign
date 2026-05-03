# Install Guide

The apps assume a **Debian-like environment with shell access and
network connectivity** — exactly what `claude.ai` provides via its
analysis tool sandbox.

Each app's install routine uses `apt-get` (system packages),
`pip install --break-system-packages` (Python packages), and for Spur
also `npm install -g` (Node packages). The `--break-system-packages`
flag is required because the sandbox uses a system-managed Python.

## Where it works

| Environment | Status |
|---|---|
| **claude.ai with analysis tool** | ✅ Primary target. Built for this. |
| **Claude Code** | ✅ Works. Use the appropriate output path. |
| **Anthropic API + tool use** | ✅ Works if you give the model shell + filesystem tools. |
| **Local Claude on a server** | ✅ As long as the model can run shell commands. |
| **Pure chat (no tools)** | ❌ The model can't actually install or render. |

## Output paths

The default output path is `/mnt/user-data/outputs/` — this is where
claude.ai surfaces files back to the user. If you're running outside
claude.ai, the model will adapt to whatever output path your environment
exposes.

## Install steps

For each app:

1. Open a fresh Claude conversation.
2. Paste the `.txt` file as a message.
3. Type `install Mozart` (or `Savannah`, or `Spur`).

The model will:
- Run `apt-get install …` for system tools
- Run `pip install …` for Python packages
- Run any verification probes
- Report ready

You don't need to do anything. Just wait. Mozart in particular has a
heavy dependency list (~50 system tools, ~25 Python packages); it can
take a few minutes.

## Order matters (a little)

You can install them in any order, but **Savannah's `compose` command
calls Spur and Mozart**, so if you want video-with-audio out of one prompt,
install Mozart and Spur first, then Savannah.

## Troubleshooting

- **Install partially fails**: the apps swallow `apt-get` and `pip` errors
  via `2>/dev/null` so a missing package doesn't stop the install. The
  model verifies the core toolchain at the end and notes anything broken.
- **Output not appearing**: check the output path the model used. In
  claude.ai it should be `/mnt/user-data/outputs/`.
- **Model breaks character**: re-paste the `.txt` file. The system prompt
  needs to be the most recent thing in the model's context.

## Updating

Each app is self-contained. To upgrade, paste a newer `.txt` file in a
new conversation. There is no install-state to migrate.

