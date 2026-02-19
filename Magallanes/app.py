import os
import json
import time
import random
import re
import requests
from flask import Flask, render_template, request, jsonify, send_from_directory
from dotenv import load_dotenv

# Cargar variables de entorno desde la raíz del proyecto
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env.local'))

# Configurar Gemini (mismo patrón que Cronista)
try:
    import google.genai as genai
    if os.getenv("GOOGLE_API_KEY"):
        client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        print("✅ Gemini configurado correctamente.")
    else:
        print("⚠️  GOOGLE_API_KEY no encontrada. La generación estará desactivada.")
        client = None
except Exception as e:
    print(f"❌ Error al inicializar Gemini: {e}")
    client = None

app = Flask(__name__, template_folder='templates', static_folder='static')

RESULTS_DIR = os.path.join(os.path.dirname(__file__), 'results')
POLLINATIONS_URL = "https://image.pollinations.ai/prompt/"

if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)


def slugify(text):
    """Convierte un texto a un formato 'slug' para nombres de carpeta."""
    text = text.lower()
    text = re.sub(r'[\s\W-]+', '-', text)
    return text.strip('-')[:60]


def generate_map_data(user_prompt, map_style="fantasy"):
    """Usa Gemini para generar la estructura del mapa y un prompt visual detallado."""
    if not client:
        return {
            "name": "Mapa de ejemplo",
            "description": "Sin conexión a Gemini. Configura GOOGLE_API_KEY.",
            "locations": [],
            "visual_prompt": f"Fantasy hand-drawn map of {user_prompt}, parchment style"
        }

    system_prompt = f"""Eres un cartógrafo experto de mundos de fantasía. Tu tarea es diseñar un mapa a partir de la descripción que te dan.

Debes devolver un JSON con esta estructura EXACTA (sin markdown, sin ```json, solo el JSON puro):

{{
    "name": "Nombre del mapa/región",
    "description": "Descripción narrativa corta del mapa (2-3 frases)",
    "locations": [
        {{
            "name": "Nombre del lugar",
            "type": "city|town|village|ruins|dungeon|forest|mountain|lake|river|port|castle|temple|cave|island|bridge|tower|camp",
            "description": "Descripción corta del lugar",
            "connections": ["Nombre de otro lugar conectado"]
        }}
    ],
    "visual_prompt": "Un prompt CONCISO en INGLÉS (máximo 50 palabras) para generar una imagen de mapa de fantasía. Debe describir: estilo visual ({map_style}), los accidentes geográficos principales y la disposición del territorio. NO incluyas texto legible. Sé muy breve y directo."
}}

REGLAS:
1. Genera entre 5 y 12 localizaciones según la complejidad de la descripción.
2. Las conexiones deben ser bidireccionales y lógicas (caminos, ríos, pasos de montaña).
3. El visual_prompt debe ser MUY detallado y en INGLÉS, optimizado para generación de imagen por IA.
4. El estilo del mapa debe ser: {map_style}.
5. NO incluyas markdown, solo JSON puro.
6. Sé CREATIVO con los nombres y descripciones, que suenen épicos y evocadores.

Descripción del usuario:
{user_prompt}"""

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=system_prompt
        )
        raw_text = response.text.strip()

        # Limpiar posibles wrappers de markdown
        if raw_text.startswith("```"):
            raw_text = re.sub(r'^```(?:json)?\s*', '', raw_text)
            raw_text = re.sub(r'\s*```$', '', raw_text)

        map_data = json.loads(raw_text)
        return map_data

    except json.JSONDecodeError as e:
        print(f"❌ Error parseando JSON de Gemini: {e}")
        print(f"   Respuesta raw: {raw_text[:500]}")
        return {
            "name": "Error de generación",
            "description": "No se pudo interpretar la respuesta de la IA.",
            "locations": [],
            "visual_prompt": f"Fantasy hand-drawn map of {user_prompt}, detailed parchment style, mountains, rivers, forests, compass rose, decorative borders, ink illustration"
        }
    except Exception as e:
        print(f"❌ Error generando datos del mapa: {e}")
        return {
            "name": "Error",
            "description": f"Error: {e}",
            "locations": [],
            "visual_prompt": f"Fantasy hand-drawn map of {user_prompt}, parchment style, detailed ink illustration"
        }


def generate_map_image_pollinations(visual_prompt):
    """Intenta generar la imagen del mapa con Pollinations.ai."""
    MAX_PROMPT_LENGTH = 350
    if len(visual_prompt) > MAX_PROMPT_LENGTH:
        visual_prompt = visual_prompt[:MAX_PROMPT_LENGTH].rsplit(' ', 1)[0]

    encoded_prompt = requests.utils.quote(visual_prompt)
    print(f"🗺️  Intentando con Pollinations... ({len(visual_prompt)} chars)")

    try:
        seed = random.randint(0, 999999)
        params = {
            'width': 1024, 'height': 1024, 'seed': seed,
            'nologo': 'true', 'model': 'flux', 'enhance': 'true'
        }
        param_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        image_url = f"{POLLINATIONS_URL}{encoded_prompt}?{param_string}"

        response = requests.get(image_url, timeout=90)
        if response.status_code == 200:
            print("✅ Imagen generada con Pollinations")
            return response.content
        else:
            print(f"⚠️ Pollinations respondió: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Error Pollinations: {e}")

    return None


def generate_map_image_gemini(visual_prompt):
    """Genera la imagen del mapa usando Gemini Imagen como fallback."""
    if not client:
        return None

    print("🎨 Usando Gemini Imagen como fallback...")
    try:
        from google.genai import types

        response = client.models.generate_images(
            model='imagen-4.0-fast-generate-001',
            prompt=visual_prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio='1:1',
            )
        )

        if response.generated_images and len(response.generated_images) > 0:
            image_data = response.generated_images[0].image.image_bytes
            print("✅ Imagen generada con Gemini Imagen")
            return image_data
        else:
            print("⚠️ Gemini Imagen no devolvió imágenes")
    except Exception as e:
        print(f"⚠️ Error Gemini Imagen: {e}")

    return None


def generate_map_image(visual_prompt):
    """Genera la imagen del mapa. Intenta Pollinations primero, luego Gemini Imagen."""
    # Intento 1: Pollinations (gratuito)
    result = generate_map_image_pollinations(visual_prompt)
    if result:
        return result

    # Intento 2: Gemini Imagen (fallback, usa API key)
    result = generate_map_image_gemini(visual_prompt)
    if result:
        return result

    print("❌ No se pudo generar la imagen con ningún servicio")
    return None


@app.route('/')
def index():
    """Página principal."""
    # Cargar mapas anteriores
    maps = []
    if os.path.exists(RESULTS_DIR):
        for folder_name in sorted(os.listdir(RESULTS_DIR), reverse=True):
            folder_path = os.path.join(RESULTS_DIR, folder_name)
            if os.path.isdir(folder_path):
                data_path = os.path.join(folder_path, 'map_data.json')
                image_path = os.path.join(folder_path, 'map.jpg')
                if os.path.exists(data_path) and os.path.exists(image_path):
                    with open(data_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    maps.append({
                        'id': folder_name,
                        'name': data.get('name', folder_name),
                        'description': data.get('description', ''),
                        'locations': data.get('locations', []),
                        'prompt': data.get('original_prompt', ''),
                    })
    return render_template('index.html', maps=maps)


@app.route('/generate', methods=['POST'])
def generate():
    """Endpoint para generar un mapa."""
    data = request.get_json()
    user_prompt = data.get('prompt', '').strip()
    map_style = data.get('style', 'fantasy hand-drawn parchment')

    if not user_prompt:
        return jsonify({'error': 'El prompt no puede estar vacío.'}), 400

    print(f"\n{'='*60}")
    print(f"🧭 Nueva generación de mapa")
    print(f"📝 Prompt: {user_prompt}")
    print(f"🎨 Estilo: {map_style}")
    print(f"{'='*60}\n")

    # 1. Generar datos del mapa con Gemini
    print("🧠 Generando estructura del mapa con Gemini...")
    map_data = generate_map_data(user_prompt, map_style)
    print(f"✅ Mapa: {map_data['name']} — {len(map_data.get('locations', []))} localizaciones")

    # 2. Generar imagen del mapa con Pollinations
    image_bytes = generate_map_image(map_data['visual_prompt'])

    if not image_bytes:
        return jsonify({'error': 'No se pudo generar la imagen del mapa.'}), 500

    # 3. Guardar resultados
    folder_name = f"{int(time.time())}_{slugify(map_data['name'])}"
    folder_path = os.path.join(RESULTS_DIR, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    # Guardar imagen
    image_path = os.path.join(folder_path, 'map.jpg')
    with open(image_path, 'wb') as f:
        f.write(image_bytes)

    # Guardar datos del mapa
    map_data['original_prompt'] = user_prompt
    map_data['style'] = map_style
    data_path = os.path.join(folder_path, 'map_data.json')
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(map_data, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Mapa guardado en: {folder_path}\n")

    return jsonify({
        'success': True,
        'map': {
            'id': folder_name,
            'name': map_data['name'],
            'description': map_data['description'],
            'locations': map_data.get('locations', []),
            'image_url': f'/results/{folder_name}/map.jpg'
        }
    })


@app.route('/results/<path:filepath>')
def serve_results(filepath):
    """Sirve archivos de la carpeta results/."""
    return send_from_directory(RESULTS_DIR, filepath)


@app.route('/map/<map_id>')
def view_map(map_id):
    """Devuelve los datos de un mapa guardado."""
    folder_path = os.path.join(RESULTS_DIR, map_id)
    data_path = os.path.join(folder_path, 'map_data.json')

    if not os.path.exists(data_path):
        return jsonify({'error': 'Mapa no encontrado.'}), 404

    with open(data_path, 'r', encoding='utf-8') as f:
        map_data = json.load(f)

    return jsonify({
        'map': {
            'id': map_id,
            'name': map_data['name'],
            'description': map_data['description'],
            'locations': map_data.get('locations', []),
            'image_url': f'/results/{map_id}/map.jpg'
        }
    })


if __name__ == '__main__':
    url = "http://127.0.0.1:5003"
    print(f"\n🧭 Magallanes — Cartógrafo de Mundos Fantásticos")
    print(f"🚀 Corriendo en {url}")
    print(f"📊 Gemini: {'✅ Conectado' if client else '❌ No disponible'}")
    print(f"🗺️  Resultados en: {RESULTS_DIR}\n")

    import webbrowser
    webbrowser.open(url)
    app.run(debug=True, port=5003)
