import os
import time
import base64
from flask import Flask, render_template, request, url_for, jsonify
from PIL import Image
import traceback
from dotenv import load_dotenv

# Cargar variables de entorno desde .env.local
load_dotenv('.env.local')

app = Flask(__name__)

# Configuración
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
STATIC_GEN_FOLDER = os.path.join(BASE_DIR, 'static', 'generated')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_GEN_FOLDER, exist_ok=True)

# Detectar si tenemos OpenAI API Key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
USE_OPENAI = OPENAI_API_KEY and OPENAI_API_KEY != 'your_openai_api_key_here'

if USE_OPENAI:
    print("🔑 OpenAI API Key detectada - Usando modo PREMIUM")
    from openai import OpenAI
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
else:
    print("🆓 Sin OpenAI API Key - Usando modo GRATUITO")
    openai_client = None

# Configuración para modo gratuito
CAPTION_MODEL = "Salesforce/blip-image-captioning-large"
POLLINATIONS_URL = "https://image.pollinations.ai/prompt/"

# Cliente de HuggingFace para captioning (modo gratuito)
from huggingface_hub import InferenceClient
try:
    hf_client = InferenceClient(model=CAPTION_MODEL)
except:
    hf_client = None

import requests

def analyze_image_with_gpt4_vision(image_path):
    """Analiza la imagen con GPT-4 Vision para obtener descripción detallada"""
    try:
        # Leer y codificar la imagen
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Llamar a GPT-4 Vision
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Describe this image in detail. Focus on: architecture style, main structures, materials, colors, and spatial composition. Be specific and technical."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )
        
        description = response.choices[0].message.content
        print(f"📝 GPT-4 Vision: {description[:100]}...")
        return description
    
    except Exception as e:
        print(f"⚠️ Error en GPT-4 Vision: {e}")
        return None

def generate_with_dalle3(description):
    """Genera imagen isométrica usando DALL-E 3"""
    try:
        # Construir prompt optimizado para DALL-E 3
        prompt = f"""Isometric technical drawing of: {description}

Style: Hand-drawn architectural blueprint on graph paper
Details: Black ink lines, white background, precise technical illustration, schematic view
Perspective: Isometric 30-degree angle, showing depth and dimension
Quality: Clean, professional architectural sketch"""

        print(f"🎨 Generando con DALL-E 3...")
        
        response = openai_client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        image_url = response.data[0].url
        
        # Descargar la imagen
        img_response = requests.get(image_url)
        if img_response.status_code == 200:
            return img_response.content
        else:
            return None
    
    except Exception as e:
        print(f"⚠️ Error en DALL-E 3: {e}")
        return None

def analyze_image_free(image_path):
    """Analiza imagen con BLIP (modo gratuito)"""
    try:
        if hf_client:
            caption = hf_client.image_to_text(image_path)
            print(f"📝 BLIP Caption: {caption}")
            return caption
    except Exception as e:
        print(f"⚠️ Error en BLIP: {e}")
    
    return "architectural structure"

def generate_with_pollinations(caption):
    """Genera imagen con Pollinations.ai (modo gratuito)"""
    try:
        # Prompt mejorado para mejor calidad
        final_prompt = f"""isometric technical drawing blueprint of {caption}, 
hand drawn architectural sketch on graph paper, detailed line art, 
white background, black ink lines, professional schematic, 
30-degree isometric perspective, clean technical illustration"""
        
        # Encode prompt for URL
        encoded_prompt = requests.utils.quote(final_prompt)
        
        # Generar con Pollinations
        import random
        seed = random.randint(0, 999999)
        image_url = f"{POLLINATIONS_URL}{encoded_prompt}?width=1024&height=1024&seed={seed}&nologo=true&model=flux"
        
        print(f"🎨 Generando con Pollinations...")
        
        response = requests.get(image_url, timeout=60)
        if response.status_code == 200:
            return response.content
        else:
            return None
    
    except Exception as e:
        print(f"⚠️ Error en Pollinations: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html', mode='premium' if USE_OPENAI else 'free')

@app.route('/generate', methods=['POST'])
def generate():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    # Guardar imagen de entrada
    filename = f"input_{int(time.time())}.jpg"
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(input_path)

    try:
        description = None
        image_data = None
        
        # MODO PREMIUM: OpenAI
        if USE_OPENAI:
            print("🔑 Usando pipeline PREMIUM (OpenAI)...")
            
            # 1. Analizar con GPT-4 Vision
            description = analyze_image_with_gpt4_vision(input_path)
            
            if description:
                # 2. Generar con DALL-E 3
                image_data = generate_with_dalle3(description)
            
            # Fallback a modo gratuito si falla OpenAI
            if not image_data:
                print("⚠️ OpenAI falló, usando modo gratuito...")
                USE_OPENAI_TEMP = False
        
        # MODO GRATUITO: HuggingFace + Pollinations
        if not USE_OPENAI or not image_data:
            print("🆓 Usando pipeline GRATUITO...")
            
            # 1. Analizar con BLIP
            description = analyze_image_free(input_path)
            
            # 2. Generar con Pollinations
            image_data = generate_with_pollinations(description)
        
        # Guardar resultado
        if image_data:
            output_filename = f"gen_{int(time.time())}.jpg"
            final_path = os.path.join(STATIC_GEN_FOLDER, output_filename)
            with open(final_path, 'wb') as f:
                f.write(image_data)
            
            return jsonify({
                'input_url': f"/uploads/{filename}",
                'result_url': url_for('static', filename=f"generated/{output_filename}"),
                'description': description,
                'mode': 'premium' if USE_OPENAI else 'free'
            })
        else:
            return jsonify({'error': 'Failed to generate image'}), 500

    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# Ruta para servir uploads
from flask import send_from_directory
@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    url = "http://127.0.0.1:5000"
    print(f"🚀 Delineante corriendo en {url}")
    print(f"📊 Modo: {'PREMIUM (OpenAI)' if USE_OPENAI else 'GRATUITO (Pollinations)'}")
    
    import webbrowser
    webbrowser.open(url)
    app.run(debug=True, port=5000)
