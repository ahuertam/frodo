# 🤖 Frodo - Contexto del Repositorio

> **Documento de referencia para asistentes de IA.** Lee este archivo primero para obtener contexto general. Solo entra en los subdocumentos de `.gemini/` cuando necesites trabajar en un agente concreto.

## Qué es Frodo

Colección de **agentes de IA especializados** en Python, diseñados para automatizar tareas creativas y prácticas. Filosofía: **coste cero** (APIs gratuitas y open-source). Cada agente es independiente y autocontenido en su propia carpeta.

## Estructura raíz

```
frodo/
├── GEMINI.md              # ← Este archivo (contexto principal)
├── .gemini/               # Subdocumentos de contexto por agente
├── README.md              # Documentación pública del proyecto
├── .env.local             # API Keys (GOOGLE_API_KEY, OPENAI_API_KEY, DEEPGRAM_API_KEY, LIVEKIT_*)
├── .gitignore             # Ignora venv/, __pycache__/, .env*, *.mp3, *.txt, *.jpg (con excepciones)
├── ideas.md               # 32 ideas de agentes futuros
├── frodo.code-workspace   # Workspace de VS Code
│
├── Altamira/              # Ilustrador de textos
├── Bardo/                 # Dungeon Master IA
├── Charactor/             # Creador de personajes RPG (texto + imagen)
├── Charme/                # Transformador de fotos a personajes RPG (web)
├── Cronista/              # Generador de aventuras de rol (web)
├── Delineante/            # Conversor de fotos a dibujos isométricos (web)
├── Narrator/              # Generador de audiolibros (edge-tts)
├── Salomon/               # Divisor de textos largos (auxiliar de Narrator)
├── Sniper/                # Buscador de chollos en Vinted/Wallapop
└── sfxDrama/              # Soundboard reactivo por voz
```

## Stack tecnológico general

| Categoría | Tecnologías |
|---|---|
| **Lenguaje** | Python 3 |
| **Web** | Flask (Charme :5001, Cronista :5002, Delineante :5000, Bardo) |
| **IA Texto** | Google Gemini (gratuito), OpenAI GPT-4 (premium) |
| **IA Imagen** | Pollinations.ai (gratuito), DALL-E 3 (premium), BLIP/HuggingFace (captioning gratuito) |
| **Voz/Audio** | edge-tts (Microsoft neural voices), Vosk (STT offline), sounddevice, Deepgram |
| **Web scraping** | Selenium |
| **Entornos** | `venv/` por agente (activar con `source venv/bin/activate`) |

## Patrón común de cada agente

Todos los agentes siguen una estructura similar:
- **Script principal** `.py` en la raíz del agente
- **`doc.md`** con documentación específica
- **`venv/`** entorno virtual propio (no commiteado)
- **Carpeta de entrada** (`texts/`, `books/`, `uploads/`) y **carpeta de salida** (`results/`, `generatedAuds/`, etc.)

## APIs y claves

Las claves se cargan desde `.env.local` en la raíz del proyecto con `python-dotenv`:
- `GOOGLE_API_KEY` → Gemini (Cronista, Charactor)
- `OPENAI_API_KEY` → GPT-4/DALL-E 3 (Bardo, Charme, Delineante modo premium)
- `DEEPGRAM_API_KEY` → STT en tiempo real (Bardo)
- `LIVEKIT_*` → Comunicación en tiempo real (Bardo)

Algunos agentes tienen su propio `.env.local` (Charme, Delineante) para keys opcionales.

## Mapa de agentes (resumen rápido)

| Agente | Función | Interfaz | API principal |
|---|---|---|---|
| **Altamira** | Texto → Ilustraciones | CLI | Pollinations.ai |
| **Bardo** | Dungeon Master IA | CLI/Web/Voz | OpenAI GPT-4 + Vosk/Deepgram |
| **Charactor** | Idea → Ficha de personaje + retrato | CLI | Gemini + Pollinations |
| **Charme** | Foto → Personaje RPG | Web (Flask :5001) | BLIP/GPT-4V + Pollinations/DALL-E3 |
| **Cronista** | Generador de aventuras iterativo | Web (Flask :5002) | Google Gemini |
| **Delineante** | Foto → Dibujo isométrico | Web (Flask :5000) | BLIP/GPT-4V + Pollinations/DALL-E3 |
| **Narrator** | Texto → Audiolibro MP3 | CLI | edge-tts (gratis) |
| **Salomon** | Divide textos largos (auxiliar) | CLI | Ninguna (Python puro) |
| **Sniper** | Chollos en Vinted/Wallapop | CLI + HTML live | Selenium |
| **sfxDrama** | SFX reactivos por voz | CLI | Vosk (offline) |

## Relaciones entre agentes

- **Salomon → Narrator**: Salomon divide libros → Narrator los nararra.
- **Charactor → Cronista**: Los personajes de Charactor se pueden usar como input de Cronista.
- **Altamira + Narrator**: Altamira genera ilustraciones para los mismos textos que Narrator narra (contenido multimedia).

## Subdocumentos detallados

Cuando necesites trabajar en un agente concreto, consulta su subdocumento:

- [`.gemini/altamira.md`](.gemini/altamira.md) — Ilustrador de textos
- [`.gemini/bardo.md`](.gemini/bardo.md) — Dungeon Master IA
- [`.gemini/charactor.md`](.gemini/charactor.md) — Creador de personajes
- [`.gemini/charme.md`](.gemini/charme.md) — Transformador foto→RPG (web)
- [`.gemini/cronista.md`](.gemini/cronista.md) — Generador de aventuras (web)
- [`.gemini/delineante.md`](.gemini/delineante.md) — Dibujos isométricos (web)
- [`.gemini/narrator.md`](.gemini/narrator.md) — Audiolibros
- [`.gemini/salomon.md`](.gemini/salomon.md) — Divisor de textos
- [`.gemini/sniper.md`](.gemini/sniper.md) — Cazador de chollos
- [`.gemini/sfxdrama.md`](.gemini/sfxdrama.md) — Soundboard reactivo

## Convenciones

- **Idioma**: Documentación y prompts en **español**. Código en inglés.
- **Sin coste**: Siempre priorizar APIs gratuitas. Las de pago son opcionales (modo "premium").
- **Entornos virtuales**: Cada agente tiene su propio `venv/`. No compartir dependencias.
- **macOS**: El proyecto se desarrolla en macOS (afecta a `brew install portaudio`, `afplay`, etc.).
- **Puertos Flask**: 5000 (Delineante), 5001 (Charme), 5002 (Cronista).
