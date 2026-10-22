# 🤖 Frodo — Contexto del Repositorio

> **Documento de referencia para asistentes de IA.** Lee este archivo primero para obtener contexto general. Solo entra en los subdocumentos de `.gemini/` cuando necesites trabajar en un agente concreto.

## Qué es Frodo

Colección de **agentes y utilidades Python**, cada uno autocontenido en su propia carpeta. La mayoría
envuelve una API gratuita o de bajo coste; algunos resuelven el problema sin red. No hay framework
compartido ni runtime común: cada agente tiene su `requirements.txt` y se ejecuta por separado.

Filosofía: **coste cero** por defecto, APIs de pago siempre opcionales.

## Estructura raíz

```
frodo/
├── GEMINI.md              # ← Este archivo (contexto principal)
├── .gemini/               # Subdocumentos de contexto por agente
├── README.md              # Documentación pública del proyecto
├── .env.local             # API Keys (GOOGLE_API_KEY, OPENAI_API_KEY)
├── .gitignore             # Ignora venv/, .venv/, __pycache__/, .env*, *.mp3, *.txt, *.jpg
├── ideas.md               # Ideas de agentes futuros
├── ideas2.md              # Ideas orientadas a juegos de rol
│
├── Altamira/              # Ilustrador de textos (CLI)
├── Magallanes/            # Cartógrafo de mundos (web :5003)
├── EncounterComposer/     # Generador de encuentros + export VTT/Roll20 (web :5010)
├── Charme/                # Foto → Personaje RPG (web :5001)
├── Delineante/            # Foto → Dibujo isométrico (web :5000)
├── Cronista/              # Generador de aventuras de rol (web :5002)
├── Bardo/                 # Dungeon Master IA (CLI / web :5004 / voz)
├── sfxDrama/              # Soundboard reactivo por voz (CLI, offline)
├── Salomon/               # Divisor de textos largos (auxiliar de Narrator)
├── Narrator/              # Generador de audiolibros (edge-tts)
├── Charactor/             # Generador de nombres de fantasía por raza (CLI, sin IA)
│
└── ideas.md / ideas2.md   # Backlog de agentes propuestos (no implementados)
```

## Stack tecnológico general

| Categoría | Tecnologías |
|---|---|
| **Lenguaje** | Python 3 |
| **Web** | Flask (Delineante :5000, Charme :5001, Cronista :5002, Magallanes :5003, Bardo :5004, EncounterComposer :5010) |
| **IA Texto** | Google Gemini (gratuito), OpenAI GPT-4 (premium, opcional) |
| **IA Imagen** | Pollinations.ai (gratuito), DALL-E 3 (premium), BLIP/HuggingFace (captioning gratuito) |
| **Voz/Audio** | edge-tts (Microsoft neural voices), Vosk (STT offline), sounddevice |
| **Determinista** | `random.Random(seed)` + dataclasses congeladas (EncounterComposer) |
| **Entornos** | `venv/` o `.venv/` por agente (nunca commiteado) |

## Patrón común de cada agente

- **Script principal** `.py` en la raíz del agente
- **`requirements.txt`** con sus propias dependencias
- **`doc.md`** con documentación específica
- **Entorno virtual propio** (no commiteado)
- **Carpeta de entrada** (`texts/`, `books/`, `uploads/`) y **carpeta de salida** (`results/`, `generatedAuds/`, etc.)

En los agentes web, Flask solo parsea la petición y renderiza; el trabajo real vive en un módulo Python
importable, sin contexto de request.

## APIs y claves

Las claves se cargan desde `.env.local` con `python-dotenv`. Cada agente busca primero en su propia
carpeta y después en la raíz del repo:

- `GOOGLE_API_KEY` → Gemini (Cronista, Magallanes)
- `OPENAI_API_KEY` → GPT-4 Vision / DALL-E 3 (Charme y Delineante en modo premium)

Todos los agentes sin key siguen funcionando: o usan el tier gratuito (Pollinations, BLIP) o lo dicen
explícitamente al arrancar.

## Mapa de agentes (resumen rápido)

| Agente | Función | Interfaz | Dependencia principal |
|---|---|---|---|
| **Altamira** | Texto → Ilustraciones | CLI | Pollinations.ai |
| **Magallanes** | Descripción → mapa + estructura del territorio | Web (Flask :5003) | Gemini + Pollinations.ai |
| **EncounterComposer** | Encuentro RPG determinista + export VTT/Roll20 | Web (Flask :5010) | Ninguna (Python puro) |
| **Charme** | Foto → Personaje RPG | Web (Flask :5001) | BLIP/GPT-4V + Pollinations/DALL-E 3 |
| **Delineante** | Foto → Dibujo isométrico | Web (Flask :5000) | BLIP/GPT-4V + Pollinations/DALL-E 3 |
| **Cronista** | Generador de aventuras iterativo | Web (Flask :5002) | Google Gemini (opcional) |
| **Bardo** | Dungeon Master IA | CLI / Web (:5004) / Voz | OpenAI GPT-4 + Vosk |
| **sfxDrama** | SFX reactivos por palabra clave | CLI | Vosk (offline) |
| **Salomon** | Divide textos largos (auxiliar) | CLI | Ninguna (Python puro) |
| **Narrator** | Texto → Audiolibro MP3 | CLI | edge-tts (gratis) |
| **Charactor** | Nombres de fantasía por raza | CLI | Ninguna (Python puro) |

### Notas sobre agentes con documentación anterior incorrecta

- **Charactor** es un **generador de nombres** basado en tablas de sílabas por raza (`marcaCharMaker.py`).
  Documentación anterior lo describía como un pipeline Gemini + Pollinations: ese código nunca existió.
  `character_data.json` contiene datos de clases/razas del sistema "La Marca del Este" pero **ningún script
  lo lee** — está como referencia, no cableado.
- **sfxDrama** hace **reconocimiento de voz offline** con Vosk y dispara efectos por palabra clave. No
  detecta picos de volumen.

## Relaciones entre agentes

- **Salomon → Narrator**: Salomon divide libros → Narrator los narra.
- **Altamira + Narrator**: Altamira ilustra los mismos textos que Narrator narra.
- **Cronista ← Magallanes**: los mapas dan el contexto geográfico de la aventura.
- **Bardo ← Cronista / Magallanes**: localizaciones y personajes como escenarios de sesión en vivo.
- **Ideas compose-agents**: ver `ideas2.md` — varios agentes propuestos se construyen encadenando los que ya existen.

## Subdocumentos detallados

Cuando necesites trabajar en un agente concreto, consulta su subdocumento:

- [`.gemini/altamira.md`](.gemini/altamira.md) — Ilustrador de textos
- [`.gemini/magallanes.md`](.gemini/magallanes.md) — Cartógrafo de mundos
- [`.gemini/encountercomposer.md`](.gemini/encountercomposer.md) — Generador de encuentros
- [`.gemini/charme.md`](.gemini/charme.md) — Transformador foto→RPG (web)
- [`.gemini/delineante.md`](.gemini/delineante.md) — Dibujos isométricos (web)
- [`.gemini/cronista.md`](.gemini/cronista.md) — Generador de aventuras (web)
- [`.gemini/bardo.md`](.gemini/bardo.md) — Dungeon Master IA
- [`.gemini/narrator.md`](.gemini/narrator.md) — Audiolibros
- [`.gemini/salomon.md`](.gemini/salomon.md) — Divisor de textos
- [`.gemini/sfxdrama.md`](.gemini/sfxdrama.md) — Soundboard reactivo
- [`.gemini/charactor.md`](.gemini/charactor.md) — Generador de nombres

## Convenciones

- **Idioma**: Documentación y prompts en **español**. Código en inglés.
- **Sin coste**: Priorizar APIs gratuitas. Las de pago son siempre opcionales (modo "premium").
- **Entornos virtuales**: Cada agente tiene el suyo. No compartir dependencias.
- **macOS**: El proyecto se desarrolla en macOS (afecta a `brew install portaudio`, `afplay`, `open`).
- **Puertos Flask**: 5000 (Delineante), 5001 (Charme), 5002 (Cronista), 5003 (Magallanes), 5004 (Bardo), 5010 (EncounterComposer). Cada agente tiene uno propio — **no reutilizar**.
- **Debug**: todas las apps arrancan con `debug=False`. `FLASK_DEBUG=1` para activarlo.
- **Tests/CI**: el repo **no tiene tests ni CI**. Es una caja de herramientas personal, no una librería mantenida.