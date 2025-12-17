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
RESULTS_FOLDER = os.path.join(BASE_DIR, 'results')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

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

def identify_rooms_with_gpt4(description, count=4):
    """Identifica habitaciones/áreas distintas para mapas top-down"""
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": f"""Based on this description: {description}

Identify up to {count} distinct rooms or areas that would be interesting for a tabletop RPG session.
For each room, provide a concise description (1-2 sentences) including:
- Room name/type
- Key features and layout
- Tactical elements (furniture, obstacles, etc.)

Format: Return only the room descriptions, one per line, numbered 1-{count}."""
                }
            ],
            max_tokens=400
        )
        
        rooms_text = response.choices[0].message.content
        # Parse numbered list
        rooms = []
        for line in rooms_text.split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-')):
                # Remove numbering
                room_desc = line.split('.', 1)[-1].strip() if '.' in line else line.lstrip('- ')
                if room_desc:
                    rooms.append(room_desc)
        
        # Limit to requested count
        rooms = rooms[:count]
        print(f"🏰 Identificadas {len(rooms)} habitaciones")
        return rooms
    
    except Exception as e:
        print(f"⚠️ Error identificando habitaciones: {e}")
        # Fallback: generic rooms
        generic_rooms = [
            "Main hall with stone pillars and wooden furniture",
            "Throne room with elevated platform and decorative elements",
            "Dungeon chamber with cells and torture equipment",
            "Tower room with spiral stairs and arrow slits"
        ]
        return generic_rooms[:count]

def generate_topdown_map(room_description, model="dall-e-3"):
    """Genera un mapa top-down de una habitación usando DALL-E 2 o 3"""
    try:
        prompt = f"""Top-down floor plan for tabletop RPG of: {room_description}

Style: Clean architectural floor plan, black and white
Features: 
- Room layout with walls clearly defined
- Furniture and obstacles marked
- Doors and windows indicated
- Clean, printable design
- NO GRID (grid can be added later)
- Suitable for D&D/Pathfinder
Perspective: Bird's eye view, top-down, 2D floor plan"""
        
        print(f"🗺️ Generando mapa con {model.upper()}...")
        
        # DALL-E 2 uses different size options
        size = "1024x1024" if model == "dall-e-3" else "1024x1024"
        
        response = openai_client.images.generate(
            model=model,
            prompt=prompt,
            size=size,
            n=1,
        )
        
        image_url = response.data[0].url
        
        # Download image
        img_response = requests.get(image_url)
        if img_response.status_code == 200:
            return img_response.content
        else:
            return None
    
    except Exception as e:
        print(f"⚠️ Error generando mapa: {e}")
        return None

def generate_topdown_maps_free(caption, count=4):
    """Genera mapas top-down con Pollinations (modo gratuito)"""
    maps = []
    
    # Generic room types for fallback
    room_types = [
        "entrance hall",
        "main chamber",
        "side room",
        "storage area"
    ]
    
    for i in range(count):
        try:
            room_type = room_types[i] if i < len(room_types) else f"room {i+1}"
            
            final_prompt = f"""Top-down RPG floor plan, {caption} {room_type}, 
architectural blueprint style, black and white,
furniture layout, doors and walls clearly marked,
bird's eye view, no grid overlay, clean printable map,
tabletop gaming battle map"""
            
            encoded_prompt = requests.utils.quote(final_prompt)
            
            import random
            seed = random.randint(0, 999999)
            image_url = f"{POLLINATIONS_URL}{encoded_prompt}?width=1024&height=1024&seed={seed}&nologo=true&model=flux"
            
            print(f"🗺️ Generando mapa {i+1}/{count} con Pollinations...")
            
            response = requests.get(image_url, timeout=60)
            if response.status_code == 200:
                maps.append(response.content)
            else:
                maps.append(None)
        
        except Exception as e:
            print(f"⚠️ Error generando mapa {i+1}: {e}")
            maps.append(None)
    
    return maps


def analyze_image_free(image_path):
    """Analiza imagen con múltiples modelos gratuitos para mejor descripción"""
    captions = []
    
    # Intentar con BLIP
    try:
        if hf_client:
            caption = hf_client.image_to_text(image_path)
            captions.append(caption)
            print(f"📝 BLIP Caption: {caption}")
    except Exception as e:
        print(f"⚠️ Error en BLIP: {e}")
    
    # Intentar con BLIP-2 (mejor modelo)
    try:
        blip2_client = InferenceClient(model="Salesforce/blip2-opt-2.7b")
        caption2 = blip2_client.image_to_text(image_path)
        captions.append(caption2)
        print(f"📝 BLIP-2 Caption: {caption2}")
    except Exception as e:
        print(f"⚠️ Error en BLIP-2: {e}")
    
    # Combinar captions o usar el mejor
    if captions:
        # Usar el caption más largo (generalmente más descriptivo)
        best_caption = max(captions, key=len)
        return best_caption
    
    return "architectural structure"

def generate_with_pollinations(caption):
    """Genera imagen con Pollinations.ai (modo gratuito) - Prompt mejorado"""
    try:
        # Prompt MUCHO más detallado y específico
        final_prompt = f"""Professional isometric architectural technical drawing of {caption}.

STYLE: Hand-drawn blueprint, black ink on white paper, technical illustration
PERSPECTIVE: 30-degree isometric axonometric projection, showing all three dimensions
DETAILS: Clean precise lines, architectural accuracy, structural elements visible
QUALITY: Professional drafting quality, detailed but not cluttered
BACKGROUND: Pure white background, no grid
TECHNIQUE: Technical pen drawing, architectural sketch style

IMPORTANT: Maintain the architectural style and character of {caption}. 
Show the complete structure in isometric view with accurate proportions."""
        
        # Encode prompt for URL
        encoded_prompt = requests.utils.quote(final_prompt)
        
        # Generar con Pollinations usando Flux (mejor modelo)
        import random
        seed = random.randint(0, 999999)
        
        # Parámetros optimizados para mejor calidad
        params = {
            'width': 1024,
            'height': 1024,
            'seed': seed,
            'nologo': 'true',
            'model': 'flux',
            'enhance': 'true'  # Mejora de calidad
        }
        
        param_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        image_url = f"{POLLINATIONS_URL}{encoded_prompt}?{param_string}"
        
        print(f"🎨 Generando con Pollinations (Flux enhanced)...")
        print(f"📋 Prompt: {final_prompt[:100]}...")
        
        response = requests.get(image_url, timeout=90)  # Más tiempo para mejor calidad
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

    # Get user preferences from form
    generate_maps = request.form.get('generate_maps', 'false') == 'true'
    map_count = int(request.form.get('map_count', 0))
    use_dalle2 = request.form.get('use_dalle2', 'false') == 'true'
    
    print(f"📋 Opciones: Maps={generate_maps}, Count={map_count}, DALL-E2={use_dalle2}")

    # Crear carpeta de resultados basada en el nombre del archivo
    original_filename = os.path.splitext(file.filename)[0]  # Sin extensión
    # Limpiar nombre para usar como carpeta
    safe_folder_name = "".join(c for c in original_filename if c.isalnum() or c in (' ', '-', '_')).strip()
    if not safe_folder_name:
        safe_folder_name = f"upload_{int(time.time())}"
    
    result_folder = os.path.join(RESULTS_FOLDER, safe_folder_name)
    os.makedirs(result_folder, exist_ok=True)
    
    print(f"📁 Guardando en: results/{safe_folder_name}/")

    # Guardar imagen de entrada en la carpeta de resultados
    input_filename = "input.jpg"
    input_path = os.path.join(result_folder, input_filename)
    file.save(input_path)

    try:
        description = None
        isometric_data = None
        topdown_maps = []
        room_descriptions = []
        
        # MODO PREMIUM: OpenAI
        if USE_OPENAI:
            print("🔑 Usando pipeline PREMIUM (OpenAI)...")
            
            # 1. Analizar con GPT-4 Vision
            description = analyze_image_with_gpt4_vision(input_path)
            
            if description:
                # 2. Generar isométrico con DALL-E 3
                isometric_data = generate_with_dalle3(description)
                
                # 3. Generar mapas top-down si está activado
                if generate_maps and map_count > 0:
                    rooms = identify_rooms_with_gpt4(description, count=map_count)
                    room_descriptions = rooms
                    model = "dall-e-2" if use_dalle2 else "dall-e-3"
                    
                    for room in rooms:
                        map_data = generate_topdown_map(room, model=model)
                        topdown_maps.append(map_data)
            
            # Fallback a modo gratuito si falla OpenAI
            if not isometric_data:
                print("⚠️ OpenAI falló, usando modo gratuito...")
        
        # MODO GRATUITO: HuggingFace + Pollinations
        if not USE_OPENAI or not isometric_data:
            print("🆓 Usando pipeline GRATUITO...")
            
            # 1. Analizar con BLIP
            description = analyze_image_free(input_path)
            
            # 2. Generar isométrico con Pollinations
            isometric_data = generate_with_pollinations(description)
            
            # 3. Generar mapas top-down si está activado
            if generate_maps and map_count > 0:
                topdown_maps = generate_topdown_maps_free(description, count=map_count)
                room_descriptions = [f"Room {i+1}" for i in range(map_count)]
        
        # Guardar resultados en la carpeta organizada
        if isometric_data:
            # Guardar isométrico
            iso_filename = "isometric.jpg"
            iso_path = os.path.join(result_folder, iso_filename)
            with open(iso_path, 'wb') as f:
                f.write(isometric_data)
            
            # Guardar mapas top-down
            map_urls = []
            for i, map_data in enumerate(topdown_maps):
                if map_data:
                    map_filename = f"map_{i+1}.jpg"
                    map_path = os.path.join(result_folder, map_filename)
                    with open(map_path, 'wb') as f:
                        f.write(map_data)
                    map_urls.append(f"/results/{safe_folder_name}/{map_filename}")
                else:
                    map_urls.append(None)
            
            return jsonify({
                'input_url': f"/results/{safe_folder_name}/{input_filename}",
                'isometric_url': f"/results/{safe_folder_name}/{iso_filename}",
                'topdown_maps': map_urls,
                'room_descriptions': room_descriptions,
                'description': description,
                'mode': 'premium' if USE_OPENAI else 'free',
                'folder': safe_folder_name
            })
        else:
            return jsonify({'error': 'Failed to generate image'}), 500

    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# Ruta para servir archivos de resultados
from flask import send_from_directory
@app.route('/results/<path:folder>/<path:filename>')
def serve_results(folder, filename):
    folder_path = os.path.join(RESULTS_FOLDER, folder)
    return send_from_directory(folder_path, filename)

if __name__ == '__main__':
    url = "http://127.0.0.1:5000"
    print(f"🚀 Delineante corriendo en {url}")
    print(f"📊 Modo: {'PREMIUM (OpenAI)' if USE_OPENAI else 'GRATUITO (Pollinations)'}")
    
    import webbrowser
    webbrowser.open(url)
    app.run(debug=True, port=5000)
