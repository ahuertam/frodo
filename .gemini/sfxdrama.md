# sfxDrama — Soundboard reactivo por voz 🔊

## Qué hace
Escucha el micrófono en tiempo real, detecta palabras clave en tu habla, y reproduce instantáneamente el efecto de sonido asociado. Funciona como un "stream deck" activado por voz. Todo offline (Vosk).

## Archivos clave

| Archivo | Función |
|---|---|
| `sfx_drama.py` | Script principal (5KB). Captura mic, STT con Vosk, reproduce SFX. |
| `soundmap.json` | Mapeo `"palabra_clave": "archivo.mp3"` (1.2KB) |
| `doc.md` | Documentación |

## Carpetas

- `sounds/` → Biblioteca de efectos de sonido (`.wav`, `.mp3`) — 7 archivos
- `model/` → Modelo Vosk español descargado automáticamente (14 archivos)
- `venv/` → Entorno virtual

## Flujo

1. `python sfx_drama.py`
2. Primera vez: descarga modelo Vosk (~50MB)
3. Selecciona micrófono
4. Habla → detecta palabras clave → reproduce SFX asociado

## Configuración de soundmap.json

```json
{
    "genial": "applause.mp3",
    "susto": "heartbeat.mp3",
    "fail": "sad_trombone.wav"
}
```
Múltiples palabras pueden mapear al mismo archivo.

## Stack técnico

- **Vosk** → STT offline en español (modelo `vosk-model-small-es-0.42`)
- **sounddevice** → Captura de micrófono en tiempo real
- **afplay** → Reproductor nativo de macOS (output de audio)
- Requiere `portaudio` del sistema: `brew install portaudio`

## Dependencias
`vosk`, `sounddevice`, `numpy` + `portaudio` (brew)

## Notas para desarrollo

- **macOS específico**: usa `afplay` para reproducir audio (no funciona en Linux).
- El modelo Vosk se descarga automáticamente la primera vez.
- Comparte tecnología con **Bardo** (ambos usan Vosk para STT).
- Sin conexión a internet necesaria en ejecución (todo offline salvo descarga inicial del modelo).
