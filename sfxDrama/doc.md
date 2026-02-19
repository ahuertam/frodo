# Agente SFXDrama (Oído Absoluto) 🎭�

SFXDrama es un agente que **escucha lo que dices** y reacciona con efectos de sonido específicos cuando detecta **palabras clave**. Funciona como un "stream deck" activado por voz en tiempo real.

## Objetivo
Detectar palabras clave específicas en tu habla (ej: "aplauso", "miedo", "error") y reproducir instantáneamente el efecto de sonido asociado. Utiliza reconocimiento de voz local (offline) para máxima privacidad y baja latencia.

## Estructura
```
sfxDrama/
├── sounds/         # Tu biblioteca de efectos (.wav, .mp3)
├── model/          # Modelo de reconocimiento de voz Vosk (se descarga auto)
├── sfx_drama.py    # Script principal de escucha y reacción
├── soundmap.json   # Configuración de palabras clave -> archivos de sonido
├── doc.md          # Esta documentación
└── venv/           # Entorno virtual
```

## Tecnología
*   **Lenguaje**: Python 3
*   **Reconocimiento de Voz**: `vosk` (Modelo offline ligero en español).
*   **Input Audio**: `sounddevice` (Captura de micrófono en tiempo real).
*   **Output Audio**: `afplay` (Reproductor de audio nativo de macOS).
*   **Lógica**:
    1.  Captura audio del micrófono.
    2.  Transcribe el audio a texto en tiempo real usando el modelo Vosk.
    3.  Busca coincidencias exactas entre las palabras detectadas y `soundmap.json`.
    4.  Si encuentra una palabra clave -> Reproduce el sonido correspondiente inmediatamente.

## Configuración

### 1. Instalación de Dependencias
Requiere `portaudio` para el micrófono:
```bash
brew install portaudio
pip install -r requirements.txt
```

### 2. Mapeo de Sonidos (`soundmap.json`)
Edita este archivo para vincular tus palabras con tus archivos de sonido en la carpeta `sounds/`.
Formato: `"palabra_clave": "nombre_archivo.mp3"`

Ejemplo:
```json
{
    "genial": "applause.mp3",
    "susto": "heartbeat.mp3",
    "fail": "sad_trombone.wav"
}
```
*Puedes mapear múltiples palabras al mismo archivo.*

### 3. Ejecución
```bash
python sfx_drama.py
```
*   La primera vez descargará automáticamente el modelo de voz (aprox. 50MB).
*   Te pedirá seleccionar el micrófono si tienes varios.
*   ¡Empieza a hablar y escucha la magia!
