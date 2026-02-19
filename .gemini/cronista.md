# Cronista — Generador de aventuras de rol 📖

## Qué hace
Crea y expande aventuras de rol de forma iterativa. El usuario describe un mundo y personajes, y la IA genera tramas que se van expandiendo con cada interacción. Interfaz web para gestionar múltiples aventuras.

## Archivos clave

| Archivo | Función |
|---|---|
| `app.py` | Servidor Flask + lógica de generación con Gemini (9KB) |
| `doc.md` | Documentación detallada |

## Carpetas

- `templates/` → 2 archivos HTML (lista de aventuras + vista de aventura)
- `static/` → CSS/JS
- `adventures/` → Carpeta donde se guardan las aventuras creadas
- `Cronista/Cronista/adventures/` → También contiene aventuras (estructura anidada)

## Estructura de una aventura guardada

Cada aventura crea una carpeta (slug del título) con:
- `context.json` → Título, descripción del mundo, personajes
- `adventure.md` → Historia completa en Markdown (crece con cada expansión)

## Web

- **Puerto**: 5002 (`http://127.0.0.1:5002`)
- **Página principal**: Lista de aventuras existentes
- **Crear**: Título + Descripción del mundo + Descripción de personajes
- **Continuar**: Escribes instrugcciones (ej: "Los héroes investigan el asesinato") → la IA genera el siguiente capítulo

## API

- **Google Gemini** (gratuito, `GOOGLE_API_KEY` desde `.env.local` raíz)
- Sin key funciona con textos placeholder

## Ejecución
```bash
python3 Cronista/app.py
```
(Se ejecuta desde la raíz del proyecto)

## Notas para desarrollo

- Compatible con **Charactor**: los personajes generados se pueden pegar como descripción de personajes.
- La historia es acumulativa — cada expansión recibe el contexto completo anterior.
- No tiene `requirements.txt` propio (posiblemente necesita `flask`, `google-generativeai`, `python-dotenv`).
