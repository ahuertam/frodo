### Modo de Escucha en Tiempo Real (Vosk)

Bardo puede escuchar el audio de tu micrófono en tiempo real y transcribirlo localmente con Vosk.

**Requisitos:**

- Tener un micrófono conectado y configurado en tu sistema.
- Tener instaladas las dependencias `vosk` y `sounddevice` (en macOS suele requerir `portaudio`).

**Cómo usarlo:**

```bash
cd Bardo
python3 run_realtime.py
```

La primera vez descargará el modelo de Vosk automáticamente y luego te pedirá el ID del micrófono.
