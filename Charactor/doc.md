# Charactor — Generador de nombres de fantasía 🏷️

Generador de nombres de fantasía por raza, con el setting **"La Marca del Este"** como referencia de
sonoridad. Siete razas: human, elf, dwarf, halfling, gnome, orc, drow.

**No usa IA, ni red, ni ninguna API.** Es una tabla de sílabas y `random.choices`: cada raza tiene sus
prefijos, sufijos y sílabas intermedias, y el nombre se construye como `prefijo [+ sílaba] + sufijo`. La función devuelve además un
apellido o título coherente con la raza.

## Uso

```bash
cd Charactor
python3 marcaCharMaker.py
```

Imprime un nombre de ejemplo por cada raza. Para usar la clase desde otro script:

```python
from marcaCharMaker import MarcaNameGenerator

g = MarcaNameGenerator()
g.generate_full_name("elf")   # → "Thalriel Hojaverde"
```

## Qué hay en la carpeta

| Archivo | Función |
|---|---|
| `marcaCharMaker.py` | El generador. Sin dependencias. |
| `character_data.json` | Datos de clases y razas del sistema. **Ningún script lo lee hoy** — está como referencia. |

## Nota sobre la documentación anterior

Este agente se documentaba antes como un pipeline que usaba **Google Gemini** para generar la ficha de
personaje y **Pollinations.ai** para el retrato, con un entrypoint `charactor.py` y una carpeta `chars/`
de salida. **Nada de eso existe en el repo**: la carpeta se vació a medias y la descripción nunca se
actualizó. El README raíz y `GEMINI.md` ya están corregidos.