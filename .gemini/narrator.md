# Narrator — Generador de audiolibros 🎙️

## Qué hace
Convierte textos (libros, artículos, fanfics) en archivos MP3 con voces neuronales de alta calidad usando `edge-tts` (Microsoft Edge, gratis e ilimitado). No requiere GPU ni descargar modelos grandes.

## Archivos clave

| Archivo | Función |
|---|---|
| `narrator.py` | Script principal (5.5KB). Selección de voz, velocidad, generación de audio. |
| `doc.md` | Documentación |

## Carpetas

- `texts/` → Entrada (archivos `.txt` para narrar)
- `generatedAuds/` → Salida (archivos `.mp3` generados)
- `venv/` → Entorno virtual

## Flujo

1. Coloca texto en `texts/`
2. `./venv/bin/python3 narrator.py`
3. Selecciona archivo → elige voz (Español Neutro, Castellano, Inglés, etc.) → elige velocidad
4. Audio generado en `generatedAuds/`

## Motor de voz

- **edge-tts**: Voces neuronales de Microsoft Edge
  - Gratuito y sin límites estrictos
  - Calidad de estudio
  - Múltiples idiomas y estilos
  - Solo necesita `pip install edge-tts`

## Dependencias
`edge-tts`, `asyncio` (estándar)

## Notas para desarrollo

- Muy sencillo y autocontenido.
- Funciona con **Salomon**: primero divides un libro largo con Salomon, luego narras cada fragmento con Narrator.
- Funciona con **Altamira**: un mismo texto puede tener audio (Narrator) + ilustraciones (Altamira) para contenido multimedia completo.
