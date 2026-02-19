# Bardo — Dungeon Master IA 🎭

## Qué hace
Actúa como Dungeon Master para juegos de rol. Genera narrativa, reacciona a las acciones de los jugadores, y pide tiradas de dado cuando hay incertidumbre. Soporta interacción por texto, web y voz en tiempo real.

## Archivos clave

| Archivo | Función |
|---|---|
| `bardo.py` | Clase `Bardo` con toda la lógica (GPT-4, Vosk, Deepgram) |
| `session_profile.json` | Config de aventura: personajes, escenario, tono |
| `web_server.py` | Servidor Flask para interfaz web |
| `narrador_sim.py` | Simulador de narrador |
| `run_realtime.py` | Lanza modo escucha en tiempo real (Vosk) |
| `README.md` | Doc del modo Deepgram en tiempo real |

## Carpetas

- `model/` → Modelo Vosk descargado automáticamente (~50MB, `vosk-model-small-es-0.42`)
- `static/` → Archivos estáticos (imágenes generadas)
- `templates/` → Templates HTML (1 archivo)

## Clase `Bardo` (bardo.py)

Métodos principales:
- `__init__()` → Carga `.env.local`, init OpenAI client, keywords de acción
- `check_model()` → Descarga modelo Vosk si no existe
- `load_session_profile()` → Lee `session_profile.json`
- `get_system_prompt()` → Prompt del DM con personajes, escenario, tono
- `get_response(user_input)` → Llama a `gpt-4-turbo` con system prompt
- `listen(text)` → Procesa texto del jugador y responde
- `listen_realtime()` → Modo escucha con Vosk (mic → texto → respuesta)
- `start_listening()` → Modo texto interactivo (stdin)

## Keywords de acción
`["ataca", "lanza", "entra", "descubre", "muere", "huye"]` → Disparan tirada de dados d20.

## APIs

- **OpenAI GPT-4 Turbo** → Generación de texto narrativo (modelo `gpt-4-turbo`, max 150 tokens)
- **Vosk** → STT offline en español
- **Deepgram** → STT en tiempo real (alternativa online a Vosk)
- **LiveKit** → Comunicación en tiempo real (keys en `.env.local` raíz)

## Dependencias
`openai`, `python-dotenv`, `vosk`, `sounddevice`, `deepgram-sdk`

## Notas para desarrollo

- El modelo Vosk se descarga automáticamente la primera vez.
- Las rutas hardcodeadas asumen ejecución desde la raíz del proyecto (`Bardo/model`, `Bardo/session_profile.json`).
- GPT-4 es de pago (usa `OPENAI_API_KEY` de `.env.local` raíz).
