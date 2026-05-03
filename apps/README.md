# Apps

**Three creative systems for Claude.**
**Each one is a prompt. A `.txt` file. That is all.**

```
  Mozart      music
  Savannah    animation
  Spur        images
```

These were built for Claude — for [claude.ai](https://claude.ai) specifically — but
they work in any environment where Claude has code execution.
They turn Claude into the system: the voice, the interface, the instrument.

There is no API to learn. No service to call. You paste the file in,
say `install Mozart` (or `Savannah`, or `Spur`), and the model becomes
a music producer, a cinematographer, an image generator.

The model does the work. The prompt does the orchestration.

---

## What each one does

### 🎼 Mozart — `Mozart.txt`
A music production system. Two phases with a hard wall between them:

1. **Composition** — pure music theory. The model produces a complete
   symbolic score: notes, chords, dynamics, structure.
2. **Execution** — assigns sounds (FluidSynth, Bristol, csound, numpy
   synthesis, or user samples), renders to WAV.

One word in (`"sad"`, `"banger"`, `"rainfall"`) → a full piece out. Built-in DAW
visualization. Vocal emulation via formant synthesis. Sample import.
Versioned: **v2.0**.

### 🎬 Savannah — `Savannah.txt`
An animation system. Same two-phase architecture:

1. **Design** — a complete blueprint: motion paths, easing, color palette,
   timing.
2. **Execution** — selects the right rendering engine (Pillow, Cairo, Skia,
   ModernGL, Manim) and pipes raw frames to ffmpeg.

The 12 principles of animation are baked in. Easing is mandatory.
Loops are seamless. Versioned: **v1.0**.

### 🖼 Spur — `Spur.txt`
An image generation system. Different philosophy: it doesn't take over
the conversation. After install, Claude just makes images. ~300+ tools
across raster, vector, 3D, fractal, typography, technical diagrams.
The decision step picks the right tool every time. Versioned: **v1.0**.

### 🎨 They compose
All three know about each other. Inside Savannah, the `compose` command
asks Spur for frames and Mozart for soundtrack and assembles them into
a complete motion picture with synchronized audio.

---

## How to use

1. **Open a Claude conversation.** Best results with Claude.ai, Claude Code,
   or any Claude environment that has shell execution and file output.

2. **Drop the prompt in.** Open `Mozart.txt` (or `Savannah.txt`, or
   `Spur.txt`). Copy the entire file. Paste it into Claude.

3. **Install.** Type:
   ```
   install Mozart
   ```
   (Or `install Savannah`, or `install Spur`.) The model executes the
   install steps silently, verifies the toolchain, and reports ready.

4. **Use.**
   - **Mozart** waits with: *"Use one word to describe your first Mozart."*
   - **Savannah** waits with: *"Describe what moves."*
   - **Spur** says *"Spur installed."* and then operates invisibly — just
     ask for any image.

5. **Export.** Outputs go to `/mnt/user-data/outputs/` by default (this is
   the standard analysis-tool path in claude.ai). The model presents files
   to you when ready.

---

## Architectural note

Every app is built on the same primitive:

> **$ →(R)→ M**

A signal `$` flows through a resolver `R` and produces meaning `M`.
For Mozart: symbols → Mozart → audio. For Savannah: descriptions → Savannah
→ video. For Spur: prompts → Claude → image.

This is the Shannon-Weaver semantic communication model, applied as
software architecture. The router is the intelligence. The channel is
the system.

---

## License

**CC BY 4.0** — Creative Commons Attribution 4.0 International.

You can use, share, modify, and build on these freely, including
commercially. See `LICENSE` for the full text.

---

## Why these exist

These apps are demonstrations of a thesis: **most "AI tools" are
overengineered.** A system prompt and a careful library are enough to
turn a frontier model into a credible musician, animator, or visual
artist. No fine-tuning. No model serving. No proprietary stack.
Just a `.txt` file and a model that can read.

The model is the runtime. The prompt is the language.
