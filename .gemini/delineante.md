# Delineante — Conversor de fotos a dibujos isométricos 📐

## Qué hace
Toma cualquier imagen y la transforma en un dibujo isométrico técnico, estilo plano dibujado a mano sobre papel cuadriculado. Opcionalmente genera mapas top-down RPG. Interfaz web con modos premium y gratuito.

## Archivos clave

| Archivo | Función |
|---|---|
| `app.py` | Servidor Flask + lógica dual premium/free (17KB, el más largo) |
| `requirements.txt` | `flask`, `openai`, `Pillow`, `python-dotenv`, `requests` |
| `.env.local` | `OPENAI_API_KEY` opcional (para modo premium) |
| `.gitignore` | Protección de archivos sensibles y subidas |
| `doc.md` | Documentación |

## Carpetas

- `templates/` → `index.html` (interfaz web)
- `static/` → CSS/JS
- `uploads/` → Imágenes subidas temporalmente
- `results/` → Organizado por nombre de archivo: `input.jpg`, `isometric.jpg`, `map_1.jpg`, `map_2.jpg`, etc.
- `venv/` → Entorno virtual

## Modos de operación

### Premium (con `OPENAI_API_KEY`)
1. GPT-4 Vision analiza la imagen → descripción detallada
2. DALL-E 3 (o DALL-E 2 para mapas más baratos) genera el isométrico + mapas

### Gratuito (sin key)
1. BLIP (HuggingFace API) → captioning (usa múltiples modelos para mejor calidad)
2. Pollinations.ai (Flux) → generación

## Web

- **Puerto**: 5000 (`http://127.0.0.1:5000`)
- Subida de imagen por drag-and-drop
- Genera: 1 vista isométrica + 0-4 mapas top-down opcionales
- Los mapas no llevan grid overlay

## Ejecución
```bash
cd Delineante && source venv/bin/activate && python app.py
```

## Notas para desarrollo

- Es el `app.py` más complejo del proyecto (17KB).
- Tiene su propio `.env.local` y `.gitignore`.
- Los resultados se organizan en carpetas nombradas como el archivo de entrada.
- DALL-E 3 produce resultados significativamente mejores que el modo gratuito.
