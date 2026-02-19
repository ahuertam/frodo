# Magallanes — Cartógrafo de Mundos Fantásticos 🧭

Magallanes genera mapas de fantasía a partir de descripciones textuales. Le describes un territorio y él diseña la disposición lógica de las localizaciones y dibuja el mapa completo.

## 🎯 ¿Qué hace?

- Transforma descripciones de mundos en **mapas visuales** con estilo de fantasía
- Genera la **estructura lógica** del territorio (localizaciones, conexiones, tipos)
- Ofrece **6 estilos visuales**: pergamino, acuarela, gótico, colorido, náutico, minimalista
- Guarda un historial de todos los mapas generados
- Interfaz web moderna con vista a pantalla completa

## 🛠️ Stack

- **Backend**: Flask (Python)
- **IA Texto**: Google Gemini (estructura del mapa + prompt visual)
- **IA Imagen**: Pollinations.ai (generación del mapa, modelo Flux)
- **Frontend**: HTML5, CSS3, JavaScript vanilla

## 🚀 Uso

### Instalación

```bash
cd Magallanes
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Ejecución

```bash
python app.py
```

Se abre automáticamente en `http://127.0.0.1:5003`

## 📁 Estructura

```
Magallanes/
├── app.py              # Servidor Flask + lógica Gemini/Pollinations
├── requirements.txt    # Dependencias
├── doc.md              # Esta documentación
├── templates/
│   └── index.html      # Interfaz web
├── static/
│   └── style.css       # Estilos
├── results/            # Mapas generados (carpeta por mapa)
│   └── timestamp_nombre/
│       ├── map.jpg         # Imagen del mapa
│       └── map_data.json   # Datos estructurados (localizaciones, conexiones)
└── venv/               # Entorno virtual
```

## 📖 Flujo de trabajo

1. Escribe una descripción del territorio en la caja de texto
2. Selecciona el estilo visual que prefieres
3. Pulsa "Generar Mapa" (o Ctrl+Enter)
4. Gemini diseña la estructura del territorio y genera un prompt visual detallado
5. Pollinations.ai dibuja el mapa
6. Se muestra el mapa con las localizaciones detalladas debajo

## 🔗 Integración con otros agentes

- **Cronista**: Los mapas proporcionan contexto geográfico para las aventuras
- **Bardo**: Las localizaciones sirven como escenarios para sesiones en vivo
- **Delineante**: Los mapas generados se pueden re-estilizar en vista isométrica
- **Charactor**: Las localizaciones dan contexto de origen para personajes

## 📄 Formato de datos

Cada mapa genera un `map_data.json` con esta estructura:

```json
{
    "name": "Las Islas del Velo",
    "description": "Un archipiélago misterioso...",
    "locations": [
        {
            "name": "Puerto Bruma",
            "type": "port",
            "description": "Ciudad portuaria envuelta en niebla perpetua",
            "connections": ["Bosque de Cristal", "Isla del Coloso"]
        }
    ],
    "visual_prompt": "...",
    "original_prompt": "...",
    "style": "fantasy hand-drawn parchment"
}
```
