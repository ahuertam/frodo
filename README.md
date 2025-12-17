# 🤖 Frodo - AI Agents for Automation

A collection of specialized AI agents designed to automate creative and practical tasks using free or low-cost AI services.

## 🎯 Philosophy

**Zero-Cost Automation**: All agents prioritize free APIs and open-source tools to make AI automation accessible to everyone.

---

## 📦 Available Agents

### 🎨 [Altamira](./Altamira) - Visual Illustrator
Transforms text into illustrations for multimedia content.

**What it does:**
- Reads text fragments and generates digital illustrations
- Creates visual accompaniment for audiobooks or YouTube videos
- Uses free Pollinations.ai API

**Usage:**
```bash
cd Altamira
python3 altamira.py
```

---

### 🎭 [Charactor](./Charactor) - Character Creator
Generates deep character profiles with visual portraits.

**What it does:**
- Transforms simple ideas into complete character sheets
- Creates biographical backgrounds, personality traits, and physical descriptions
- Generates character portraits using AI

**Tech Stack:**
- Text generation: Google Gemini API (free tier) or HuggingFace
- Image generation: Pollinations.ai

**Usage:**
```bash
cd Charactor
python3 charactor.py
```

---

### 🎭 [Charme](./Charme) - RPG Character Transformer
Converts photos into epic RPG character classes.

**What it does:**
- Transforms photos of people or drawings into RPG characters
- Supports 12 character classes (Warrior, Mage, Rogue, Cleric, etc.)
- Generates 1-4 characters simultaneously
- Web interface with drag-and-drop upload

**Modes:**
- 🔑 **Premium**: GPT-4 Vision analysis + DALL-E 3 generation (requires OpenAI API key)
- 🆓 **Free**: BLIP captioning + Pollinations.ai (no API key needed)

**Usage:**
```bash
cd Charme
source venv/bin/activate
pip install -r requirements.txt
python app.py
# Opens web interface at http://127.0.0.1:5001
```

---

### 📐 [Delineante](./Delineante) - Isometric Draftsman
Converts photos into isometric technical drawings.

**What it does:**
- Transforms any image into hand-drawn isometric blueprints
- Offers premium mode (OpenAI GPT-4 Vision + DALL-E 3) and free mode (BLIP + Pollinations)
- Provides web interface for easy image upload

**Modes:**
- 🔑 **Premium**: GPT-4 Vision analysis + DALL-E 3 generation (requires OpenAI API key)
- 🆓 **Free**: BLIP captioning + Pollinations.ai (no API key needed)

**Usage:**
```bash
cd Delineante
# Optional: Add OPENAI_API_KEY to .env.local for premium mode
source venv/bin/activate
pip install -r requirements.txt
python app.py
# Opens web interface at http://127.0.0.1:5000
```

---

### 🎙️ [Narrator](./Narrator) - Audiobook Generator
Converts text into narrated audiobooks with neural voices.

**What it does:**
- Transforms books, articles, or any text into MP3 audiobooks
- Uses Microsoft Edge's neural voices (free, unlimited, studio quality)
- Supports multiple languages and voice styles

**Tech Stack:**
- Voice engine: `edge-tts` (free Microsoft neural voices)
- No GPU required, no model downloads

**Usage:**
```bash
cd Narrator
./venv/bin/python3 narrator.py
```

---

### ✂️ [Salomon](./Salomon) - Text Splitter
Intelligently divides large texts into manageable chunks.

**What it does:**
- Prepares large books for the Narrator agent
- Splits text respecting paragraph boundaries
- Creates numbered fragments for easy processing

**Usage:**
```bash
cd Salomon
python3 salomon.py
```

**Workflow with Narrator:**
1. Place full book in `Salomon/books/`
2. Run Salomon to split into chunks
3. Use Narrator on the generated fragments

---

### 🎯 [Sniper](./Sniper) - Second-Hand Arbitrage Hunter
Automates deal hunting on Vinted and Wallapop.

**What it does:**
- Monitors Vinted and Wallapop for specific items
- Detects arbitrage opportunities automatically
- Generates live HTML dashboard with results

**Features:**
- Interactive mode (no code editing needed)
- Auto-refreshing results page
- Anti-bot protections (random delays, user-agent rotation)

**Usage:**
```bash
cd Sniper
./venv/bin/python3 sniper.py
# Opens results.html in browser
```

**Platforms:**
- ✅ Vinted: Very stable
- ⚠️ Wallapop: Functional but may trigger CAPTCHA

---

### 🔊 [sfxDrama](./sfxDrama) - Reactive Soundboard
Real-time sound effects triggered by audio events.

**What it does:**
- Listens to your microphone for volume spikes
- Automatically plays sound effects for dramatic moments
- Perfect for streams, presentations, or just fun

**Tech Stack:**
- Audio input: `sounddevice` + `numpy`
- Audio output: `pygame`
- Real-time analysis with configurable thresholds

**Requirements:**
```bash
# macOS
brew install portaudio
cd sfxDrama
# Install Python dependencies
```

---

## 🚀 Quick Start

Each agent is self-contained in its own directory with:
- `doc.md` - Detailed documentation
- Main script (`.py`)
- `venv/` - Virtual environment (where applicable)

### General Setup Pattern
```bash
# Navigate to agent directory
cd [AgentName]

# Activate virtual environment (if exists)
source venv/bin/activate

# Install dependencies (if needed)
pip install -r requirements.txt

# Run the agent
python3 [agent_script].py
```

---

## 🛠️ Technology Stack

- **Python 3** - Core language for all agents
- **Free AI APIs**:
  - Pollinations.ai (image generation)
  - Google Gemini (text generation)
  - Microsoft Edge TTS (voice synthesis)
  - OpenAI (optional premium features)
- **Web Automation**: Selenium
- **Audio Processing**: edge-tts, sounddevice, pygame
- **Web Interfaces**: Flask

---

## 📋 Project Ideas

See [ideas.md](./ideas.md) for future agent concepts and enhancements.

---

## 🤝 Contributing

Each agent is designed to be modular and independent. Feel free to:
- Enhance existing agents
- Add new free API integrations
- Improve documentation
- Share your use cases

---

## ⚠️ Important Notes

- **API Keys**: Some agents offer premium features with API keys (always optional)
- **Rate Limits**: Free APIs may have usage limits
- **Anti-Bot**: Web scraping agents (Sniper) may encounter protections
- **Audio Permissions**: Microphone access required for sfxDrama and similar agents

---

## 📄 License

Open source - use responsibly and respect API terms of service.
