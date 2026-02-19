# Documentación de Bardo

Bardo es un asistente de inteligencia artificial que actúa como un Dungeon Master para un juego de rol. Esta documentación te guiará a través de cómo modificar y personalizar el agente para adaptarlo a tus necesidades.

## Estructura del Proyecto

El proyecto se estructura de la siguiente manera:

- `Bardo/`: Carpeta principal del agente.
  - `bardo.py`: Contiene la lógica principal del agente, incluyendo la inicialización del modelo de lenguaje, el manejo de la conversación y la interacción con el usuario.
  - `session_profile.json`: Archivo de configuración que define los personajes, el escenario y el tono de la aventura.
  - `static/`: Carpeta que contiene los archivos estáticos, como las imágenes generadas.
- `app.py`: Aplicación Flask que sirve la interfaz de usuario.
- `run.py`: Script para iniciar la aventura en modo de texto.

## Personalización de la Aventura

Para personalizar la aventura, puedes modificar el archivo `Bardo/session_profile.json`. Este archivo contiene tres secciones principales:

- `characters`: Una lista de los personajes que participan en la aventura. Cada personaje tiene un nombre, un tipo y una descripción.
- `setting`: El escenario de la aventura, incluyendo la ubicación y la atmósfera.
- `tone`: El tono general de la aventura (por ejemplo, "oscuro y misterioso", "épico y heroico", etc.).

### Ejemplo de `session_profile.json`

```json
{
    "characters": {
        "Arion": {
            "type": "Elfo",
            "description": "Un arquero elfo con un pasado misterioso."
        },
        "Gimli": {
            "type": "Enano",
            "description": "Un guerrero enano con un hacha de dos manos."
        }
    },
    "setting": "Un bosque oscuro y antiguo.",
    "tone": "Oscuro y misterioso."
}
```

## Modificación del Agente

Si deseas modificar el comportamiento del agente, puedes editar el archivo `Bardo/bardo.py`. Este archivo contiene la clase `Bardo`, que es responsable de la lógica principal del agente.

### Métodos Principales

- `__init__()`: Inicializa el agente, cargando la configuración y el modelo de lenguaje.
- `load_session_profile()`: Carga el perfil de la sesión desde el archivo `session_profile.json`.
- `get_characters_string()`: Devuelve una cadena con los nombres y tipos de los personajes.
- `get_system_prompt()`: Devuelve el prompt del sistema que se utiliza para guiar al modelo de lenguaje.
- `get_response(user_input)`: Envía el prompt del sistema y la entrada del usuario al modelo de lenguaje y devuelve la respuesta.
- `listen(text)`: Procesa la entrada del usuario y la respuesta del modelo de lenguaje.
- `start_listening()`: Inicia el bucle de escucha para la interacción con el usuario en modo de texto.
- `listen_realtime()`: Inicia el modo de escucha en tiempo real utilizando `vosk` para el reconocimiento de voz.

### Escucha en Tiempo Real

Bardo ahora tiene un modo de escucha en tiempo real que utiliza la librería `vosk` para el reconocimiento de voz. Para utilizar este modo, primero debes instalar las dependencias necesarias:

```bash
pip install vosk sounddevice
```

Una vez instaladas las dependencias, puedes iniciar el modo de escucha en tiempo real ejecutando el siguiente comando:

```bash
python3 run_realtime.py
```

El programa te pedirá que selecciones un micrófono y luego comenzará a escuchar.

### Personalización del Prompt del Sistema

El prompt del sistema es la parte más importante para guiar el comportamiento del modelo de lenguaje. Puedes modificar el método `get_system_prompt()` en `Bardo/bardo.py` para cambiar la forma en que el agente se comporta.

Por ejemplo, puedes agregar más detalles sobre el mundo, los personajes o la trama de la aventura. También puedes cambiar las reglas del juego, como la forma en que se manejan las tiradas de dados.
