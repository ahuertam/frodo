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
                            "text": """Analyze the FACIAL FEATURES of this person with EXTREME DETAIL. Ignore all clothing and accessories.

Provide a VERY DETAILED description of:

**FACE STRUCTURE:**
- Exact face shape (oval, round, square, heart-shaped, diamond, rectangular)
- Jawline (sharp, soft, prominent, receding)
- Cheekbone prominence (high, low, defined, soft)
- Forehead (broad, narrow, high, low)

**EYES:**
- Exact eye color (be specific: hazel, blue-green, dark brown, etc.)
- Eye shape (almond, round, hooded, deep-set, wide-set)
- Eye size relative to face
- Eyelid characteristics

**EYEBROWS:**
- Thickness (thin, medium, thick, bushy)
- Shape (arched, straight, angled)
- Color

**NOSE:**
- Size (small, medium, large, prominent)
- Bridge (straight, curved, wide, narrow)
- Tip shape (pointed, rounded, bulbous)
- Nostril size

**MOUTH & LIPS:**
- Lip fullness (thin, medium, full)
- Mouth width (narrow, medium, wide)
- Lip shape
- Smile characteristics if visible

**FACIAL HAIR:**
- Type (clean-shaven, stubble, beard, mustache)
- If present: style, length, coverage

**HAIR:**
- Color (be very specific)
- Length
- Texture (straight, wavy, curly, coily)
- Style/cut
- Hairline

**SKIN:**
- Skin tone (be specific)
- Texture characteristics

**AGE & EXPRESSION:**
- Approximate age
- Facial expression
- Overall demeanor

Be EXTREMELY DETAILED so the face can be accurately recreated. Focus on UNIQUE identifying features."""
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
            max_tokens=400
        )
        
        description = response.choices[0].message.content
        print(f"📝 Características faciales detalladas extraídas ({len(description)} chars)")
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

def generate_character_with_dalle3(description, character_class, max_retries=3):
    """Genera personaje RPG usando DALL-E 3 con máximo parecido facial y reintentos automáticos"""
    class_info = next((c for c in CHARACTERS_DATA['classes'] if c['id'] == character_class), None)
    if not class_info:
        return None
    
    # Prompt optimizado para MÁXIMO parecido facial
    prompt = f"""A fantasy RPG character portrait of a {class_info['name']}.

CRITICAL - PRESERVE THESE EXACT FACIAL FEATURES (HIGHEST PRIORITY):
{description}

The face MUST look exactly like this description. This is the MOST IMPORTANT requirement. The facial likeness must be PERFECT and RECOGNIZABLE.

Character clothing: {class_info.get('required_elements', class_info['keywords'])}

Art style: {class_info.get('art_style', 'D&D character art')}, professional fantasy portrait, {class_info['keywords']}

STRICT RULES:
1. PHOTOREALISTIC FACE - The face must be highly detailed and match the description EXACTLY
2. Simple portrait, plain background
3. NO decorative objects, NO floating items, NO UI elements
4. NO text, NO letters, NO words, NO symbols
5. Medieval fantasy clothing only, {class_info.get('forbidden_elements', 'no modern items')}

Focus PRIMARILY on making the face look EXACTLY like the description. The facial features are MORE IMPORTANT than the clothing. Keep composition simple and clean."""
    
    # Intentar generar con reintentos
    for attempt in range(max_retries):
        try:
            if attempt > 0:
                print(f"🔄 Reintento {attempt + 1}/{max_retries} para {class_info['name']}...")
            else:
                print(f"🎨 Generando {class_info['name']} con DALL-E 3 (máximo parecido facial)...")
            
            response = openai_client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            
            image_url = response.data[0].url
            
            # Descargar la imagen
            img_response = requests.get(image_url, timeout=60)
            if img_response.status_code == 200:
                print(f"✅ {class_info['name']} generado exitosamente")
                return img_response.content
            else:
                print(f"⚠️ Error descargando imagen (intento {attempt + 1}/{max_retries})")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Espera exponencial: 1s, 2s, 4s
                    continue
        
        except Exception as e:
            print(f"⚠️ Error en DALL-E 3 (intento {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Espera exponencial
                continue
    
    print(f"❌ No se pudo generar {class_info['name']} después de {max_retries} intentos")
    return None

def generate_character_with_pollinations(description, character_class, max_retries=3):
    """Genera personaje RPG con Pollinations.ai con máximo parecido facial y reintentos automáticos"""
    class_info = next((c for c in CHARACTERS_DATA['classes'] if c['id'] == character_class), None)
    if not class_info:
        return None
    
    # Prompt optimizado para máximo parecido
    final_prompt = f"""Fantasy RPG character portrait of a {class_info['name']}.

CRITICAL - EXACT FACIAL FEATURES (HIGHEST PRIORITY): {description}

The face must look EXACTLY like this description. Photorealistic facial features. Perfect facial likeness.

Clothing: {class_info.get('required_elements', class_info['keywords'])}

Style: {class_info.get('art_style', 'D&D character art')}, professional fantasy portrait

IMPORTANT: Photorealistic face matching description EXACTLY, simple portrait, plain background, NO decorative objects, NO text, NO UI elements. Medieval fantasy only, no modern items.

Focus on perfect facial likeness first, then {class_info['name']} attire."""
    
    # Encode prompt for URL
    encoded_prompt = requests.utils.quote(final_prompt)
    
    # Intentar generar con reintentos
    for attempt in range(max_retries):
        try:
            if attempt > 0:
                print(f"🔄 Reintento {attempt + 1}/{max_retries} para {class_info['name']}...")
            else:
                print(f"🎨 Generando {class_info['name']} con Pollinations (máximo parecido facial)...")
            
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
            
            response = requests.get(image_url, timeout=90)
            if response.status_code == 200:
                print(f"✅ {class_info['name']} generado exitosamente")
                return response.content
            else:
                print(f"⚠️ Error en Pollinations (intento {attempt + 1}/{max_retries}): Status {response.status_code}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Espera exponencial
                    continue
        
        except Exception as e:
            print(f"⚠️ Error en Pollinations (intento {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Espera exponencial
                continue
    
    print(f"❌ No se pudo generar {class_info['name']} después de {max_retries} intentos")
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
