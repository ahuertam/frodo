# Magallanes — Cartógrafo de mundos 🧭

## Qué hace
Convierte una descripción en texto de un territorio en un mapa de fantasía. Gemini diseña la
**estructura lógica** (localizaciones, tipos, conexiones) y emite un prompt visual; Pollinations dibuja
el mapa. Seis estilos. Web en `:5003`.

## Archivos clave

| Archivo | Función |
|---|---|
| `app.py` | Servidor Flask + integración Gemini/Pollinations |
| `requirements.txt` | Dependencias |
| `doc.md` | Documentación del agente |

## Patrón a imitar: LLM como emisor de datos

Este es el agente donde el patrón está más limpio, y el que conviene copiar a cualquier agente que
necesite **salida estructurada** de un modelo:

1. **Contrato estricto** — el prompt describe la forma JSON exacta, no "dame una descripción".
2. **Stripping de vallas markdown** — los modelos envuelven el JSON en ```json ... ```; se recorta antes
   de parsear en lugar de confiar en que这一个 vez venga limpio.
3. **Esquema tipado con enum** — los tipos de ubicación y los estilos son enums, no strings libres: el
   modelo no puede inventar un valor fuera del dominio.
4. **Cadena de fallback** — Pollinations primero, Gemini Imagen como respaldo, para que un 503 de uno no
   deje al usuario sin nada.

La respuesta a *"¿cómo usas un LLM en producción sin que te devuelva prosa cuando quieres datos?"* es:
no parsing por regex de prosa, sino contrato + validación.

## Estructuras

```
Magallanes/
├── app.py, requirements.txt, doc.md
├── templates/index.html, static/style.css
└── results/<timestamp>_<nombre>/
    ├── map.jpg
    └── map_data.json    # estructura editable: name, locations[], connections[], visual_prompt
```

## APIs
- **Google Gemini** (`GOOGLE_API_KEY`) → estructura del mapa + prompt visual
- **Pollinations.ai** (sin key) → imagen, modelo Flux. Fallback: Gemini Imagen.