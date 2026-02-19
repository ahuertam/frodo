# Salomon — Divisor de textos ✂️

## Qué hace
Agente auxiliar que divide libros completos en fragmentos manejables y numerados. Prepara textos para el Agente Narrator evitando errores por límites de caracteres en motores TTS.

## Archivos clave

| Archivo | Función |
|---|---|
| `salomon.py` | Script principal (6KB). División inteligente respetando párrafos. |
| `doc.md` | Documentación |

## Carpetas

- `books/` → Entrada (libros completos `.txt`)
- `texts/` → Salida (fragmentos numerados: `Libro_01.txt`, `Libro_02.txt`, etc.)

## Flujo

1. Coloca libro en `books/`
2. `python3 salomon.py`
3. Selecciona archivo → se divide en fragmentos (~5000 caracteres) respetando límites de párrafo
4. Fragmentos numerados en `texts/`

## Notas para desarrollo

- **Sin dependencias externas** — solo librerías estándar de Python.
- No tiene `venv/`.
- Agente auxiliar de **Narrator**: pipeline completo = Salomon divide → Narrator narra.
- El límite de caracteres por fragmento es configurable (~5000 por defecto).
