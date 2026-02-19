# Charme — Transformador de fotos a personajes RPG 🎭

## Qué hace
Convierte fotos de personas o dibujos en personajes RPG de diferentes clases (Guerrero, Mago, Pícaro, etc.). Interfaz web con drag-and-drop. Modo premium (OpenAI) y gratuito (BLIP + Pollinations).

## Archivos clave

| Archivo | Función |
|---|---|
| `app.py` | Servidor Flask + lógica dual (premium/free) — 14.5KB |
| `characters.json` | Definiciones de 12 clases RPG (keywords, descripciones) |
| `.env.local` | API key de OpenAI (opcional, para modo premium) |
| `requirements.txt` | `flask`, `openai`, `Pillow`, `python-dotenv` |
| `doc.md` | Documentación detallada |

## Carpetas

- `templates/` → `index.html` (interfaz web)
- `static/` → CSS/JS
- `uploads/` → Imágenes subidas temporalmente
- `results/` → Salida organizada por nombre de imagen (`input.jpg`, `character_1.jpg`, etc.)
- `venv/` → Entorno virtual

## Modos de operación

### Premium (con `OPENAI_API_KEY`)
1. GPT-4 Vision analiza la foto → descripción detallada
2. DALL-E 3 genera el personaje RPG

### Gratuito (sin key)
1. BLIP (HuggingFace API) → captioning básico
2. Pollinations.ai (modelo Flux) → generación de imagen

El modo se detecta automáticamente según si existe la API key.

## Web

- **Puerto**: 5001 (`http://127.0.0.1:5001`)
- Se lanza automáticamente en el navegador
- Permite generar 1-4 personajes simultáneamente
- 12 clases disponibles: Guerrero, Mago, Pícaro, Clérigo, Montaraz, Paladín, Bárbaro, Bardo, Druida, Monje, Nigromante, Brujo

## Ejecución
```bash
cd Charme && source venv/bin/activate && python app.py
```

## Notas para desarrollo

- `characters.json` es personalizable para añadir/modificar clases.
- Tiene su propio `.env.local` y `.gitignore`.
- La interfaz web es vanilla HTML/CSS/JS.
