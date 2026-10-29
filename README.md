# 🤖 Frodo — a toolbox of small Python agents

A collection of focused, self-contained Python tools. Most of them wrap a free or low-cost API; a few
solve a problem without any network call at all.

There is no framework and no shared runtime. Each agent lives in its own folder, has its own
`requirements.txt`, and runs on its own.

---

## 📦 Agents

### 🎨 [Altamira](./Altamira) — Visual Illustrator
Text → illustrations via Pollinations.ai, for illustrating the same texts [Narrator](./Narrator) reads.

```bash
cd Altamira && python3 altamira.py
```

---

### 🧭 [Magallanes](./Magallanes) — World Cartographer
Turns a text description of a territory into a fantasy map. Gemini designs the *logical* structure
(locations, types, connections) and emits a visual prompt; Pollinations draws the map. Six visual styles,
and every map is saved with its `map_data.json` so the structure stays editable.

This is an LLM used as a **structured data emitter**, not as a prose generator: strict contract, markdown
fences stripped, typed schema with enums, and a fallback chain from Pollinations to Gemini Imagen.

```bash
cd Magallanes
pip install -r requirements.txt
python3 app.py          # http://127.0.0.1:5003
```

---

### ⚔️ [EncounterComposer](./EncounterComposer) — Encounter Generator
Generates a one-page RPG encounter (scene or interlude) and exports it to **Foundry VTT** (Journal Entry
JSON) or **Roll20** (handout text).

The design choice worth reading is that **this one is deliberately not an LLM**. Generation is
deterministic: frozen dataclasses for the input contract, a seeded `random.Random`, and a cascade of
defaults. Same seed, same encounter — every time. Structured content where you want reproducibility and
no hallucinated stat blocks does not need a model. Export runs the interpolated fields through
`html.escape()`. Nothing touches disk; you generate and download in the browser.

```bash
cd EncounterComposer
pip install -r requirements.txt
python3 app.py          # http://127.0.0.1:5010
```

---

### 🎭 [Charme](./Charme) — Photo → RPG Character
Turns a photo or drawing into an RPG character, 1–4 at a time, with drag-and-drop upload.

- 🔑 **Premium**: GPT-4 Vision + DALL-E 3 (`OPENAI_API_KEY`)
- 🆓 **Free**: BLIP captioning + Pollinations.ai (no key)

```bash
cd Charme && python3 app.py        # http://127.0.0.1:5001
```

---

### 📐 [Delineante](./Delineante) — Photo → Isometric Blueprint
Turns any image into a hand-drawn isometric technical blueprint.

- 🔑 **Premium**: GPT-4 Vision + DALL-E 3 (`OPENAI_API_KEY`)
- 🆓 **Free**: BLIP captioning + Pollinations.ai (no key)

```bash
cd Delineante && python3 app.py     # http://127.0.0.1:5000
```

---

### 📖 [Cronista](./Cronista) — Adventure Weaver
Builds an RPG adventure from a world description, then expands it chapter by chapter from your prompts.
Serves without `GOOGLE_API_KEY` — it just skips generation.

```bash
cd Cronista && python3 app.py        # http://127.0.0.1:5002
```

---

### 🎙️ [Bardo](./Bardo) — AI Dungeon Master
Runs a text adventure with a persistent session profile, and can *listen* to it: Vosk transcribes your
microphone offline and triggers scene changes on keywords. Web UI plus a voice mode.

```bash
cd Bardo
python3 run_realtime.py              # voice
python3 web_server.py                # web, http://127.0.0.1:5004
```

---

### 🔊 [sfxDrama](./sfxDrama) — Voice-Triggered Soundboard
A "stream deck" you trigger by talking. Vosk transcribes offline, and a keyword plays its sound effect.

The interesting part is the threading: a `sounddevice` callback pushes raw bytes into a `queue.Queue`
and the main thread drains it, because Vosk's recognizer is not thread-safe. It reads Vosk's **partial**
results while you are still speaking and calls `recognizer.Reset()` after a match — that is what buys
sub-second reaction instead of waiting for the end of a sentence.

```bash
brew install portaudio
cd sfxDrama
pip install -r requirements.txt
python3 sfx_drama.py
```

Keywords and sounds are configured in `soundmap.json`.

---

### ✂️ [Salomon](./Salomon) — Text Splitter
Splits a long book on paragraph boundaries into numbered chunks, ready for Narrator.

```bash
cd Salomon && python3 salomon.py
```

### 🎙️ [Narrator](./Narrator) — Audiobook Generator
Turns text into narrated MP3s using Microsoft Edge's neural voices (free, no GPU, no model download).
Reads files or whole folders, six voices across Spanish and English.

```bash
cd Narrator && python3 narrator.py
```

---

### 🏷️ [Charactor](./Charactor) — Fantasy Name Generator
Syllable-based fantasy name generator with per-race tables (human, elf, dwarf, halfling, gnome, orc,
drow) drawn from the "Marca del Este" setting.

**No AI, no network, no API** — it is a syllable table and `random.choices`, and that is the whole point.
Earlier docs described a Gemini + Pollinations character-sheet pipeline here; that code never existed and
the description has been corrected.

```bash
cd Charactor && python3 marcaCharMaker.py
```

---

## 🧱 Architecture

There is no shared library. What exists is a **composition pattern**: agents are written to hand off
files and folders to each other, and any of them can be used on its own.

```
books/*.txt
     │
     ├──▶ Salomon ──▶ chunks/*.txt
     │                    │
     │                    └──▶ Narrator ──▶ *.mp3
     │                    └──▶ Altamira ──▶ illustrations
     │
     └──▶ Cronista ──▶ adventures/
              ▲                │
              │                ▼
         Magallanes ──▶ locations & connections
```

Concretely: [Salomon](./Salomon) chunks a book and [Narrator](./Narrator) narrates the chunks;
[Altamira](./Altamira) illustrates the same text Narrator reads; [Cronista](./Cronista) stores the world
and its characters, which [Bardo](./Bardo) then runs as a live session.

The one place where a pattern goes beyond file handoff is **Magallanes**: it treats the LLM as a typed
data source, with a strict JSON contract, markdown fence stripping, enum-validated schema and a fallback
chain. That is the pattern to copy for any agent that needs structured output from a model.

Each web agent keeps the same split: Flask only parses the request and renders the result; the actual work
lives in a plain Python module that can be imported and tested without a request context.

---

## 🛠️ Stack

- **Python 3** across the board, no packaging, no monorepo tooling
- **Flask** for the six web agents, each on its own port (see above)
- **Free-tier APIs**: Pollinations.ai (images), Google Gemini (text), Microsoft Edge TTS (speech)
- **Optional paid APIs**: OpenAI GPT-4 Vision / DALL-E 3 (premium mode in Charme and Delineante)
- **Offline / local**: Vosk (speech-to-text), BLIP via HuggingFace (captioning)
- **Deterministic**: `random.Random(seed)` and frozen dataclasses where output must be reproducible

---

## ⚠️ Honest notes

- **There are no tests and no CI.** This is a personal toolbox, not a maintained library. The parts that
  are worth reusing were written to be readable rather than covered — if you want to build on them,
  expect to add your own tests. `EncounterComposer` is the exception worth reading anyway: it is the most
  rigorously structured code here (frozen dataclasses, seeded RNG, engine separated from Flask) precisely
  because it is the one that had to produce correct output every time.
- **Every Flask app defaults to `debug=False`.** Set `FLASK_DEBUG=1` to enable it.
- **API keys are optional** and live in `.env.local` (git-ignored). Without them, agents fall back to free
  tiers or refuse to start with a clear message.

---

## 📄 License

MIT — see [`LICENSE`](LICENSE).

The agents call third-party APIs (Pollinations.ai, Google Gemini, Microsoft Edge TTS,
OpenAI, HuggingFace). This license covers **the code in this repository only**: use it
responsibly and respect the terms of service of whichever API you call.
