import os
import time
import base64
import json
from flask import Flask, render_template, request, url_for, jsonify, send_from_directory
from PIL import Image
import traceback
from dotenv import load_dotenv

# Cargar variables de entorno desde .env.local
load_dotenv('.env.local')

app = Flask(__name__)

# Configuración
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
RESULTS_FOLDER = os.path.join(BASE_DIR, 'results')
CHARACTERS_FILE = os.path.join(BASE_DIR, 'characters.json')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# Cargar clases de personajes
with open(CHARACTERS_FILE, 'r', encoding='utf-8') as f:
    CHARACTERS_DATA = json.load(f)

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
    """Analiza la imagen con GPT-4 Vision SOLO extrayendo características faciales permanentes"""
    try:
        # Leer y codificar la imagen
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Llamar a GPT-4 Vision con instrucciones muy específicas
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """Analyze ONLY the permanent facial features of the person in this image. IGNORE all clothing and accessories.

Describe ONLY:
- Face shape (oval, round, square, angular, etc.)
- Eye color and shape
- Eyebrow style (thick, thin, arched, straight)
- Nose shape (small, large, pointed, broad)
- Mouth and lip shape
- Facial hair (beard, mustache, clean-shaven)
- Hair color and style (length, texture, color)
- Skin tone
- Age appearance (young, middle-aged, elderly)
- Gender presentation
- Overall facial expression or demeanor

DO NOT describe: clothing, accessories, modern items, background, or anything that is not a permanent facial feature.

Be concise and focus only on features that would help recreate this person's face in a fantasy setting."""
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
            max_tokens=250
        )
        
        description = response.choices[0].message.content
        print(f"📝 Características faciales extraídas: {description[:80]}...")
        return description
    
    except Exception as e:
        print(f"⚠️ Error en GPT-4 Vision: {e}")
        return None

def analyze_image_free(image_path):
    """Analiza imagen con BLIP para obtener descripción básica"""
    try:
        if hf_client:
            caption = hf_client.image_to_text(image_path)
            print(f"📝 BLIP Caption: {caption}")
            return caption
    except Exception as e:
        print(f"⚠️ Error en BLIP: {e}")
    
    return "a person"

def generate_character_with_dalle3(description, character_class):
    """Genera personaje RPG usando DALL-E 3 con prompts estructurados en capas"""
    try:
        class_info = next((c for c in CHARACTERS_DATA['classes'] if c['id'] == character_class), None)
        if not class_info:
            return None
        
        # Construir prompt en capas con negative prompts
        prompt = f"""Professional fantasy RPG character portrait in {class_info.get('art_style', 'D&D style')}.

=== FACIAL FEATURES (from reference) ===
{description}

=== CHARACTER CLASS ===
{class_info['name']} - {class_info['description']}

=== REQUIRED VISUAL ELEMENTS ===
{class_info.get('required_elements', class_info['keywords'])}

=== VISUAL STYLE ===
{class_info['keywords']}

=== STRICT REQUIREMENTS ===
- Medieval fantasy setting ONLY
- {class_info.get('art_style', 'High fantasy character art')}
- Detailed fantasy armor/clothing appropriate for the class
- Heroic pose with dramatic lighting
- NO modern elements whatsoever

=== ABSOLUTELY FORBIDDEN (DO NOT INCLUDE) ===
{class_info.get('forbidden_elements', 'modern clothing, suits, ties, contemporary items')}

Create a detailed character portrait that combines the facial features described with the fantasy class requirements. The character MUST be dressed in appropriate medieval/fantasy attire for their class, with zero modern elements."""

        print(f"🎨 Generando {class_info['name']} con DALL-E 3 (prompts mejorados)...")
        
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

def generate_character_with_pollinations(description, character_class):
    """Genera personaje RPG con Pollinations.ai usando prompts estructurados"""
    try:
        class_info = next((c for c in CHARACTERS_DATA['classes'] if c['id'] == character_class), None)
        if not class_info:
            return None
        
        # Prompt estructurado para Pollinations con negative prompts
        final_prompt = f"""Professional {class_info.get('art_style', 'fantasy RPG')} character portrait.

Facial features: {description}

Character: {class_info['name']} - {class_info['description']}

Required elements: {class_info.get('required_elements', class_info['keywords'])}

Visual style: {class_info['keywords']}

Art style: Epic fantasy character art, detailed digital painting, dramatic lighting, heroic pose, professional RPG illustration, {class_info.get('art_style', 'D&D aesthetic')}

Medieval fantasy setting, detailed fantasy armor and equipment, NO modern clothing, NO suits, NO ties, NO contemporary items, NO modern accessories, pure fantasy aesthetic"""
        
        # Encode prompt for URL
        encoded_prompt = requests.utils.quote(final_prompt)
        
        # Generar con Pollinations usando Flux
        import random
        seed = random.randint(0, 999999)
        
        params = {
            'width': 1024,
            'height': 1024,
            'seed': seed,
            'nologo': 'true',
            'model': 'flux',
            'enhance': 'true'
        }
        
        param_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        image_url = f"{POLLINATIONS_URL}{encoded_prompt}?{param_string}"
        
        print(f"🎨 Generando {class_info['name']} con Pollinations (prompts mejorados)...")
        
        response = requests.get(image_url, timeout=90)
        if response.status_code == 200:
            return response.content
        else:
            return None
    
    except Exception as e:
        print(f"⚠️ Error en Pollinations: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html', 
                         mode='premium' if USE_OPENAI else 'free',
                         characters=CHARACTERS_DATA['classes'])

@app.route('/generate', methods=['POST'])
def generate():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    # Get user preferences from form
    character_class = request.form.get('character_class', 'warrior')
    character_count = int(request.form.get('character_count', 1))
    
    print(f"📋 Generando {character_count} personaje(s) de clase: {character_class}")

    # Crear carpeta de resultados basada en el nombre del archivo
    original_filename = os.path.splitext(file.filename)[0]
    safe_folder_name = "".join(c for c in original_filename if c.isalnum() or c in (' ', '-', '_')).strip()
    if not safe_folder_name:
        safe_folder_name = f"upload_{int(time.time())}"
    
    result_folder = os.path.join(RESULTS_FOLDER, safe_folder_name)
    os.makedirs(result_folder, exist_ok=True)
    
    print(f"📁 Guardando en: results/{safe_folder_name}/")

    # Guardar imagen de entrada
    input_filename = "input.jpg"
    input_path = os.path.join(result_folder, input_filename)
    file.save(input_path)

    try:
        description = None
        characters = []
        
        # Analizar imagen
        if USE_OPENAI:
            print("🔑 Usando análisis PREMIUM (GPT-4 Vision)...")
            description = analyze_image_with_gpt4_vision(input_path)
        
        if not description:
            print("🆓 Usando análisis GRATUITO (BLIP)...")
            description = analyze_image_free(input_path)
        
        # Generar personajes
        for i in range(character_count):
            print(f"🎭 Generando personaje {i+1}/{character_count}...")
            
            if USE_OPENAI:
                char_data = generate_character_with_dalle3(description, character_class)
            else:
                char_data = generate_character_with_pollinations(description, character_class)
            
            if char_data:
                char_filename = f"character_{i+1}.jpg"
                char_path = os.path.join(result_folder, char_filename)
                with open(char_path, 'wb') as f:
                    f.write(char_data)
                characters.append(f"/results/{safe_folder_name}/{char_filename}")
            else:
                characters.append(None)
        
        if any(characters):
            class_info = next((c for c in CHARACTERS_DATA['classes'] if c['id'] == character_class), None)
            return jsonify({
                'input_url': f"/results/{safe_folder_name}/{input_filename}",
                'characters': characters,
                'class_name': class_info['name'] if class_info else character_class,
                'description': description,
                'mode': 'premium' if USE_OPENAI else 'free',
                'folder': safe_folder_name
            })
        else:
            return jsonify({'error': 'Failed to generate characters'}), 500

    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/results/<path:folder>/<path:filename>')
def serve_results(folder, filename):
    folder_path = os.path.join(RESULTS_FOLDER, folder)
    return send_from_directory(folder_path, filename)

if __name__ == '__main__':
    url = "http://127.0.0.1:5001"
    print(f"🚀 Charme corriendo en {url}")
    print(f"📊 Modo: {'PREMIUM (OpenAI)' if USE_OPENAI else 'GRATUITO (Pollinations)'}")
    print(f"🎭 Clases disponibles: {len(CHARACTERS_DATA['classes'])}")
    
    import webbrowser
    webbrowser.open(url)
    app.run(debug=True, port=5001)
