# Charactor — Generador de nombres de fantasía 🏷️

## Qué hace
Genera nombres de fantasía por raza a partir de tablas de sílabas, con el setting "La Marca del Este"
como referencia de sonoridad. Siete razas: human, elf, dwarf, halfling, gnome, orc, drow.

**Cero IA, cero red, cero API.** Es `random.choices` sobre tablas de prefijos, sufijos y sílabas
intermedias. `generate_full_name()` añade un apellido o título según la raza.

> La documentación anterior de este agente lo describía como un pipeline Gemini + Pollinations que
> generaba fichas de personaje con retrato. **Ese código nunca existió.** No reintroducir esa descripción.

## Archivos clave

| Archivo | Función |
|---|---|
| `marcaCharMaker.py` | Generador. Entry point: `python3 marcaCharMaker.py` |
| `character_data.json` | Datos de clases/razas del sistema. **Ningún script lo lee** — referencia suelta |
| `doc.md` | Documentación del agente |

## Notas
- `character_data.json` está pendiente de borrar o de cablear; hoy es peso muerto.
- La documentación anterior mencionaba `charactor.py`, `context.txt`, `bestiario.md`, `clases.md` y una
  carpeta `chars/` de salida. **Nada de eso existe** — la carpeta se vació a medias y la documentación no
  se actualizó hasta ahora.
- Sin relación con IA: no confundir con `Cronista`, que sí usa Gemini.