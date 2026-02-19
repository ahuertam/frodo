# Charactor — Creador de personajes RPG 🎭

## Qué hace
Transforma una idea simple (ej: "Villano con miedo a las alturas") en una ficha completa de personaje con nombre, biografía, personalidad, descripción física y retrato visual generado por IA.

## Archivos clave

| Archivo | Función |
|---|---|
| `marcaCharMaker.py` | Script principal (5KB). Genera personajes de La Marca del Este. |
| `character_data.json` | Datos de clases/razas del sistema de juego (11KB) |
| `context.txt` | Contexto del mundo de juego (700KB, muy largo) |
| `doc.md` | Documentación del agente |
| `*.md` (varios) | Archivos de referencia del mundo: `bestiario.md`, `clases.md`, `combate.md`, `creacion_personajes.md`, `equipo.md`, `hechizos.md`, `objetos_magicos.md` |

## Carpetas

- `chars/` → Salida (subcarpeta por personaje con `perfil.md` + `retrato.jpg`)

## Flujo

1. `python3 marcaCharMaker.py`
2. Introduces idea/arquetipo
3. IA genera: Nombre, Biografía, Personalidad (miedos, deseos, virtudes), Descripción física
4. Se guarda ficha en `chars/Nombre/perfil.md`
5. La descripción física se envía a Pollinations → retrato en `chars/Nombre/retrato.jpg`

## APIs

- **Google Gemini** (gratuito, `GOOGLE_API_KEY`) → Generación de texto
- **Pollinations.ai** (gratuito, sin key) → Generación de retratos
- **Alternativa**: HuggingFace Inference (más lento)

## Notas para desarrollo

- Los `*.md` en la raíz de Charactor están en `.gitignore` (excepciones específicas).
- `character_data.json` contiene datos mecánicos del sistema "La Marca del Este" (clases, razas, habilidades, conjuros por nivel).
- `context.txt` es un volcado enorme del libro de reglas — se usa como contexto para el LLM.
- Compatible con **Cronista**: los personajes generados se pueden usar como input para crear aventuras.
