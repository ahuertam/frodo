# Agente SFXDrama (Soundboard Reactivo) 🎭🔊

SFXDrama es un agente que escucha tu entorno y reacciona con efectos de sonido en tiempo real. Convierte tu vida (o tu stream) en una sitcom o una película de acción automáticamente.

## Objetivo
Detectar picos de volumen (gritos, risas fuertes, golpes) a través del micrófono y disparar efectos de sonido aleatorios para añadir dramatismo o comedia.

## Estructura
```
sfxDrama/
├── sounds/         # Tu biblioteca de efectos (.wav, .mp3)
├── sfx_drama.py    # Script de escucha y reacción
├── doc.md          # Esta documentación
└── venv/           # Entorno virtual
```

## Tecnología
*   **Lenguaje**: Python 3
*   **Input Audio**: `sounddevice` + `numpy` (Para análisis en tiempo real de baja latencia).
*   **Output Audio**: `pygame` (Para reproducción de efectos sin bloquear el hilo principal).
*   **Lógica**:
    1.  Captura bloques de audio del micrófono (Callback).
    2.  Calcula el RMS (Volumen promedio).
    3.  Si RMS > UMBRAL (configurable) y ha pasado el TIEMPO_DE_ENFRIAMIENTO -> Dispara sonido.

## Configuración
*   **Instalación**: Requiere `portaudio` (en Mac: `brew install portaudio`) y las librerías de Python.
*   **Ajuste**: Al inicio, el agente te mostrará el volumen actual para que calibres el umbral de disparo.
