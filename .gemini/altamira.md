# Altamira — Ilustrador de textos 🎨

## Qué hace
Lee fragmentos de texto y genera ilustraciones digitales por IA para cada uno. Pensado para acompañar audiolibros o contenido multimedia (YouTube).

## Archivos clave

| Archivo | Función |
|---|---|
| `altamira.py` | Script principal (6KB). Lee textos, genera prompts, llama a Pollinations.ai, guarda imágenes. |
| `doc.md` | Documentación del agente |

## Carpetas

- `texts/` → Entrada (`.txt` o subcarpetas por capítulo)
- `results/` → Salida (subcarpetas por libro, imágenes `.jpg`)
- `venv/` → Entorno virtual

## Flujo

1. Coloca textos en `texts/`
2. `python3 altamira.py`
3. Selecciona texto → genera prompts del contenido → llama a Pollinations.ai → guarda en `results/`

## API

- **Pollinations.ai** (gratuita, sin key). Endpoint HTTP directo para generación de imágenes.

## Notas para desarrollo

- Sin dependencias externas complejas (solo `requests` y librerías estándar).
- El prompt se construye a partir del título + contenido del fragmento.
- Relacionado con **Narrator**: ambos procesan los mismos textos (uno genera audio, otro imagen).
