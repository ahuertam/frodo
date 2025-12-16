import os
import sys
import queue
import json
import sounddevice as sd
import vosk
import subprocess
import zipfile
import urllib.request

# Configuración
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOUNDS_DIR = os.path.join(BASE_DIR, "sounds")
MODEL_DIR = os.path.join(BASE_DIR, "model")
SOUNDMAP_FILE = os.path.join(BASE_DIR, "soundmap.json")
MODEL_URL = "https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip"

def load_soundmap():
    """Carga el mapeo de sonidos desde JSON."""
    if os.path.exists(SOUNDMAP_FILE):
        try:
            with open(SOUNDMAP_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error leyendo soundmap.json: {e}")
            return {}
    else:
        print("⚠️ soundmap.json no encontrado, creando uno por defecto.")
        default_map = {"aplauso": "applause.mp3", "bip": "beep.wav"}
        with open(SOUNDMAP_FILE, "w") as f:
            json.dump(default_map, f, indent=4)
        return default_map

KEYWORD_MAP = load_soundmap()

# Cola de audios para pasar del thread de audio al principal
q = queue.Queue()

def check_model():
    """Descarga el modelo de Vosk si no existe."""
    if not os.path.exists(MODEL_DIR):
        print(f"⬇️  Descargando modelo de voz (esto puede tardar un poco)...")
        print(f"    URL: {MODEL_URL}")
        
        zip_path = os.path.join(BASE_DIR, "model.zip")
        urllib.request.urlretrieve(MODEL_URL, zip_path)
        
        print("📦 Extrayendo modelo...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(BASE_DIR)
        
        # Renombrar la carpeta extraída a 'model'
        extracted_folder = "vosk-model-small-es-0.42"
        os.rename(os.path.join(BASE_DIR, extracted_folder), MODEL_DIR)
        os.remove(zip_path)
        print("✅ Modelo instalado.")
    else:
        print("✅ Modelo de voz detectado.")

def audio_callback(indata, frames, time_info, status):
    """Callback de audio: mete los bytes en la cola."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def play_sound(filename):
    """Reproduce sonido con afplay (no bloqueante, max 6s)."""
    filepath = os.path.join(SOUNDS_DIR, filename)
    if os.path.exists(filepath):
        # -t 6: Corta a los 6 segundos
        subprocess.Popen(["afplay", "-t", "6", filepath])
        print(f"   🔊 PLAY: {filename}")
    else:
        print(f"   ⚠️ Archivo no encontrado: {filename}")

def main():
    print("\n🎭  AGENTE SFX-DRAMA (OÍDO ABSOLUTO)  🎭")
    print("==========================================")
    
    check_model()
    
    # Cargar Modelo
    print("🧠 Cargando cerebro auditivo...")
    try:
        model = vosk.Model(MODEL_DIR)
    except Exception as e:
        print(f"❌ Error cargando modelo: {e}")
        return

    # Selección de Micro
    print("\n🎤 Dispositivos disponibles:")
    print(sd.query_devices())
    
    try:
        device_id = int(input("\nID del micrófono (o Enter para default): ") or sd.default.device[0])
    except:
        device_id = None
        
    samplerate = 16000 # Vosk prefiere 16kHz
    
    print(f"\n🚀 Escuchando... Di palabras clave: {', '.join(list(KEYWORD_MAP.keys())[:5])}...")
    print("Ctrl+C para salir.\n")

    recognizer = vosk.KaldiRecognizer(model, samplerate)
    
    try:
        with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device_id,
                               dtype='int16', channels=1, callback=audio_callback):
            while True:
                data = q.get()
                if recognizer.AcceptWaveform(data):
                    # Resultado final de una frase
                    result = json.loads(recognizer.Result())
                    text = result.get("text", "")
                else:
                    # Resultado parcial (mientras hablas) - Más rápido para reacción
                    result = json.loads(recognizer.PartialResult())
                    text = result.get("partial", "")

                if text:
                    # Buscar palabras clave
                    words = text.split()
                    for w in words:
                        if w in KEYWORD_MAP:
                            print(f"\r🗣️  Oído: '{w}'", end="") 
                            play_sound(KEYWORD_MAP[w])
                            # Limpiar para no repetir infinitamente en partials
                            recognizer.Reset() 
                            break
                            
    except KeyboardInterrupt:
        print("\n👋 Agente detenido.")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
