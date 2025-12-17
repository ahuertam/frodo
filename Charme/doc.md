# 🎭 Charme - Transformador de Personajes RPG

Convierte fotos de personas o dibujos en personajes de rol épicos de diferentes clases.

## 🎯 ¿Qué hace?

- Transforma cualquier foto en un personaje de RPG de la clase que elijas
- Soporta 12 clases diferentes: Guerrero, Mago, Pícaro, Clérigo, Montaraz, Paladín, Bárbaro, Bardo, Druida, Monje, Nigromante y Brujo
- Permite generar de 1 a 4 personajes simultáneamente
- Interfaz web moderna y fácil de usar
- Se lanza automáticamente en el navegador

## 🔑 Modos de Operación

### Modo Premium (con OpenAI API Key)
- **Análisis**: GPT-4 Vision para descripción detallada de la persona
- **Generación**: DALL-E 3 para personajes de alta calidad
- **Ventajas**: Mayor calidad y coherencia en los resultados

### Modo Gratuito (sin API Key)
- **Análisis**: BLIP (HuggingFace) para descripción básica
- **Generación**: Pollinations.ai con modelo Flux
- **Ventajas**: Completamente gratuito, sin límites

## 🚀 Uso

### Instalación

```bash
cd Charme

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Configuración (Opcional)

Para usar el modo premium, edita `.env.local`:

```bash
OPENAI_API_KEY=tu_clave_de_openai_aqui
```

Si no configuras la API key, funcionará en modo gratuito automáticamente.

### Ejecución

```bash
python app.py
```

El navegador se abrirá automáticamente en `http://127.0.0.1:5001`

## 📖 Cómo Usar la Interfaz

1. **Sube una foto**: Arrastra una imagen o haz clic para seleccionar
2. **Selecciona la clase**: Elige entre 12 clases de personajes RPG
3. **Cantidad**: Selecciona cuántos personajes generar (1-4)
4. **Generar**: Haz clic en "Generar Personajes" y espera

Los resultados se guardarán en la carpeta `results/` organizados por nombre de archivo.

## 🎨 Clases Disponibles

- **⚔️ Guerrero**: Maestro del combate cuerpo a cuerpo
- **🔮 Mago**: Maestro de las artes arcanas
- **🗡️ Pícaro**: Experto en sigilo y combate furtivo
- **✨ Clérigo**: Sanador divino y guerrero de la fe
- **🏹 Montaraz**: Cazador experto y guardián de la naturaleza
- **🛡️ Paladín**: Caballero sagrado que combina fe y acero
- **⚡ Bárbaro**: Guerrero salvaje de fuerza descomunal
- **🎵 Bardo**: Artista mágico que inspira con música
- **🌿 Druida**: Guardián de la naturaleza con poderes primordiales
- **🥋 Monje**: Maestro de artes marciales y disciplina interior
- **💀 Nigromante**: Maestro de la magia oscura
- **🔥 Brujo**: Pactante con entidades de otros planos

## 📁 Estructura de Resultados

```
results/
└── nombre_de_tu_imagen/
    ├── input.jpg          # Imagen original
    ├── character_1.jpg    # Primer personaje generado
    ├── character_2.jpg    # Segundo personaje (si se generó)
    └── ...
```

## 🛠️ Stack Tecnológico

- **Backend**: Flask (Python)
- **Análisis Premium**: OpenAI GPT-4 Vision
- **Generación Premium**: OpenAI DALL-E 3
- **Análisis Gratuito**: HuggingFace BLIP
- **Generación Gratuita**: Pollinations.ai (Flux)
- **Frontend**: HTML5, CSS3, JavaScript vanilla

## 💡 Consejos

- **Mejores resultados**: Usa fotos con buena iluminación y el rostro visible
- **Variedad**: Genera múltiples personajes para tener opciones
- **Clases**: Cada clase tiene su estilo visual único
- **Modo Premium**: Ofrece mayor coherencia y calidad artística

## ⚙️ Personalización

Puedes editar `characters.json` para:
- Añadir nuevas clases de personajes
- Modificar descripciones existentes
- Ajustar keywords para la generación de imágenes

## 🔧 Troubleshooting

**Error: No se genera la imagen**
- Verifica tu conexión a internet
- Si usas modo premium, verifica tu API key en `.env.local`
- Intenta con una imagen más pequeña (< 5MB)

**La calidad no es buena**
- Considera usar modo premium con OpenAI
- Usa fotos de mejor calidad como entrada
- Prueba con diferentes clases de personajes

## 📄 Licencia

Parte del proyecto Frodo - Uso responsable y respeto a los términos de servicio de las APIs.
