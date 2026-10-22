import openai
from dotenv import load_dotenv
import os
import json
import time
import sys
import queue
import sounddevice as sd
import vosk
import zipfile
import urllib.request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Bardo:
    def __init__(self):
        load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env.local"))
        load_dotenv(dotenv_path=os.path.join(BASE_DIR, "..", ".env.local"))
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.session_profile = self.load_session_profile()
        self.action_keywords = ["ataca", "lanza", "entra", "descubre", "muere", "huye"]
        self.model_dir = os.path.join(BASE_DIR, "model")
        self.model_url = "https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip"

    def check_model(self):
        """Descarga el modelo de Vosk si no existe."""
        if not os.path.exists(self.model_dir):
            print(f"⬇️  Descargando modelo de voz (esto puede tardar un poco)...")
            print(f"    URL: {self.model_url}")
            
            zip_path = os.path.join(BASE_DIR, "model.zip")
            urllib.request.urlretrieve(self.model_url, zip_path)
            
            print("📦 Extrayendo modelo...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(BASE_DIR)
            
            extracted_folder = "vosk-model-small-es-0.42"
            os.rename(os.path.join(BASE_DIR, extracted_folder), self.model_dir)
            os.remove(zip_path)
            print("✅ Modelo instalado.")
        else:
            print("✅ Modelo de voz detectado.")

    def load_session_profile(self):
        with open(os.path.join(BASE_DIR, 'session_profile.json'), 'r') as f:
            return json.load(f)

    def get_characters_string(self):
        return ", ".join([f"{name} ({details['type']})" for name, details in self.session_profile['characters'].items()])

    def get_system_prompt(self):
        return f"""
Eres un asistente de inteligencia artificial que actúa como un Dungeon Master para un juego de rol.
Tu objetivo es guiar a los jugadores a través de una aventura de fantasía, describiendo el mundo, los personajes no jugadores y los eventos que ocurren.
El escenario es: {self.session_profile['setting']}.
Los personajes son: {self.get_characters_string()}.
El tono de la aventura es {self.session_profile['tone']}.
Debes ser descriptivo, inmersivo y adaptarte a las decisiones de los jugadores.
Cuando un jugador realice una acción que pueda tener consecuencias inciertas, puedes pedirle que lance un dado de 20 caras para determinar el resultado.
Si un jugador realiza una acción que involucra a una de las siguientes palabras clave: {', '.join(self.action_keywords)}, debes pedirle que lance un dado de 20 caras.
"""

    def get_response(self, user_input):
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": self.get_system_prompt()},
                {"role": "user", "content": user_input}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content

    def listen(self, text):
        print(f"Bardo ha escuchado: {text}")
        response = self.get_response(text)
        print(f"Bardo responde: {response}")

    def listen_realtime(self):
        self.check_model()
        
        q = queue.Queue()

        def audio_callback(indata, frames, time_info, status):
            if status:
                print(status, file=sys.stderr)
            q.put(bytes(indata))

        try:
            model = vosk.Model(self.model_dir)
        except Exception as e:
            print(f"❌ Error cargando modelo: {e}")
            return

        print("\n🎤 Dispositivos disponibles:")
        print(sd.query_devices())
        
        try:
            device_id = int(input("\nID del micrófono (o Enter para default): ") or sd.default.device[0])
        except:
            device_id = None
            
        samplerate = 16000
        
        print(f"\n🚀 Escuchando...")
        print("Ctrl+C para salir.\n")

        recognizer = vosk.KaldiRecognizer(model, samplerate)
        
        try:
            with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device_id,
                                   dtype='int16', channels=1, callback=audio_callback):
                while True:
                    data = q.get()
                    if recognizer.AcceptWaveform(data):
                        result = json.loads(recognizer.Result())
                        text = result.get("text", "")
                        if text:
                            self.listen(text)
                                
        except KeyboardInterrupt:
            print("\n👋 Agente detenido.")
        except Exception as e:
            print(f"\n❌ Error: {e}")

    def start_listening(self):
        print("Bardo está escuchando. Escribe tu acción y pulsa Enter.")
        while True:
            try:
                user_input = input()
                if user_input.lower() in ['exit', 'salir']:
                    print("Saliendo de la aventura.")
                    break
                self.listen(user_input)
            except KeyboardInterrupt:
                print("\nSaliendo de la aventura.")
                break
            time.sleep(1)
