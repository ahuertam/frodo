from flask import Flask, render_template, request, redirect, url_for
import os
import json
import re
import google.genai as genai
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv(dotenv_path='.env.local')

# Configurar Gemini
try:
    if os.getenv("GOOGLE_API_KEY"):
        # La librería google.genai lee la variable de entorno GOOGLE_API_KEY automáticamente.
        model = genai.GenerativeModel('gemini-pro')
    else:
        print("⚠️  GOOGLE_API_KEY no encontrada. La generación de tramas estará desactivada.")
        model = None
except Exception as e:
    print(f"Error al inicializar el modelo de Gemini: {e}")
    model = None

app = Flask(__name__, template_folder='templates', static_folder='static')
ADVENTURES_DIR = 'Cronista/adventures'

if not os.path.exists(ADVENTURES_DIR):
    os.makedirs(ADVENTURES_DIR)

def slugify(text):
    """Convierte un texto a un formato 'slug' para nombres de carpeta."""
    text = text.lower()
    text = re.sub(r'[\s\W-]+', '-', text)
    return text.strip('-')

def generate_initial_plot(title, world, characters):
    """Genera el Capítulo 1 de la aventura usando Google Gemini."""
    if not model:
        return f"# Capítulo 1\n\n*La aventura '{title}' comienza aquí...*\n\n**Mundo:** {world}\n\n**Personajes:** {characters}"
    
    prompt = f"""
Eres un maestro de juegos de rol y un narrador experto. Tu tarea es crear el **Capítulo 1** de una aventura épica para un juego de rol.

**Título de la Aventura:** {title}

**Descripción del Mundo:**
{world}

**Descripción de los Personajes:**
{characters}

**Instrucciones para generar el Capítulo 1:**
1.  **Introducción Atractiva:** Comienza con una escena que capte la atención de los jugadores. Puede ser una situación de tensión, un misterio, o un evento inesperado.
2.  **Presentar el Conflicto Inicial:** Introduce el problema principal o el objetivo inicial que motivará a los personajes a actuar.
3.  **Describir el Entorno:** Detalla el lugar donde comienza la aventura. Usa descripciones sensoriales para sumergir a los jugadores.
4.  **Sugerir Opciones:** Finaliza el capítulo dejando abiertas varias opciones o caminos para que los jugadores decidan qué hacer a continuación.
5.  **Tono Coherente:** Mantén un tono de aventura épica, misterio o intriga, según corresponda al mundo y los personajes descritos.

**Formato de Salida:**
El texto debe estar en formato Markdown. Usa negritas para los títulos de secciones o eventos importantes, y cursivas para los pensamientos o descripciones más poéticas.

**Ejemplo de estructura (no uses este ejemplo literalmente, es solo una guía):**
```markdown
# Capítulo 1: El Despertar de las Sombras

**La bruma matinal** se cierne sobre la ciudadela de Valmoris. Los personajes, reunidos en la taberna del "Dragón Dorado", escuchan un grito desgarrador desde la plaza del mercado...

*Un silencio inquietante se apodera de la taberna.*

**El tabernero**, un hombre corpulento con cicatrices de antiguas batallas, se acerca a la mesa de los héroes...

**¿Qué hacen los personajes?**
```

Ahora, genera el Capítulo 1 único y emocionante para la aventura proporcionada.
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generando trama: {e}")
        return f"# Capítulo 1\n\n*La aventura '{title}' comienza aquí...*\n\n**Mundo:** {world}\n\n**Personajes:** {characters}"

def generate_next_chapter(title, world, characters, story, user_prompt):
    """Genera el siguiente capítulo de la aventura usando Google Gemini."""
    if not model:
        return f"\n\n---\n\n*Continuación basada en la instrucción: '{user_prompt}'...*"

    # Contar cuántos capítulos hay para nombrar el siguiente
    chapter_count = story.count("# Capítulo")
    next_chapter_number = chapter_count + 1

    prompt = f"""
Eres un maestro de juegos de rol y un narrador experto. Tu tarea es continuar una aventura épica.

**Título de la Aventura:** {title}

**Descripción del Mundo:**
{world}

**Descripción de los Personajes:**
{characters}

**Historia Hasta Ahora:**
{story}

**Instrucción del Usuario para el Siguiente Capítulo:**
{user_prompt}

**Instrucciones para generar el Capítulo {next_chapter_number}:**
1.  **Continuidad Lógica:** Asegúrate de que el nuevo capítulo siga la narrativa y los eventos de la "Historia Hasta Ahora".
2.  **Incorporar la Instrucción:** El nuevo capítulo debe basarse en la "Instrucción del Usuario". Úsala como el motor principal del nuevo capítulo.
3.  **Desarrollar la Trama:** Avanza la historia, introduce nuevos desafíos, personajes secundarios o misterios.
4.  **Sugerir Nuevas Opciones:** Finaliza el capítulo dejando abiertas varias opciones o caminos para que los jugadores decidan qué hacer a continuación.
5.  **Tono Coherente:** Mantén el tono establecido en la aventura.

**Formato de Salida:**
El texto debe estar en formato Markdown, comenzando con el título del nuevo capítulo.

**Ejemplo de estructura (no uses este ejemplo literalmente, es solo una guía):**
```markdown
# Capítulo {next_chapter_number}: El Secreto del Gremio

Siguiendo las pistas del mercado, los héroes se adentran en los callejones oscuros de Valmoris, buscando la sede oculta del gremio de ladrones...

*La tensión aumenta con cada sombra que se mueve.*

**De repente, una figura encapuchada les corta el paso.**

**¿Qué hacen los personajes?**
```

Ahora, genera el **Capítulo {next_chapter_number}** de forma única y emocionante.
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generando continuación de la trama: {e}")
        return f"\n\n---\n\n*No se pudo generar la continuación. Error: {e}*"

@app.route('/')
def index():
    adventures = []
    for adventure_id in os.listdir(ADVENTURES_DIR):
        path = os.path.join(ADVENTURES_DIR, adventure_id)
        if os.path.isdir(path):
            # Para obtener el título original, podríamos leerlo del context.json
            # pero por ahora usaremos el id de la carpeta.
            adventures.append({'id': adventure_id, 'title': adventure_id.replace('-', ' ').title()})
    return render_template('index.html', adventures=adventures)

@app.route('/create', methods=['POST'])
def create_adventure():
    title = request.form['title']
    world = request.form['world']
    characters = request.form['characters']
    
    adventure_id = slugify(title)
    adventure_path = os.path.join(ADVENTURES_DIR, adventure_id)
    
    if not os.path.exists(adventure_path):
        os.makedirs(adventure_path)
    
    context = {
        'title': title,
        'world': world,
        'characters': characters
    }
    
    with open(os.path.join(adventure_path, 'context.json'), 'w') as f:
        json.dump(context, f, indent=4)
    
    # Generar el Capítulo 1
    initial_plot = generate_initial_plot(title, world, characters)
    
    with open(os.path.join(adventure_path, 'adventure.md'), 'w', encoding='utf-8') as f:
        f.write(initial_plot)
        
    return redirect(url_for('adventure', adventure_id=adventure_id))

@app.route('/adventure/<adventure_id>')
def adventure(adventure_id):
    adventure_path = os.path.join(ADVENTURES_DIR, adventure_id)
    
    with open(os.path.join(adventure_path, 'context.json'), 'r') as f:
        context = json.load(f)
        
    with open(os.path.join(adventure_path, 'adventure.md'), 'r', encoding='utf-8') as f:
        story = f.read()
        
    return render_template('adventure.html', title=context['title'], story=story, adventure_id=adventure_id)

@app.route('/continue/<adventure_id>', methods=['POST'])
def continue_adventure(adventure_id):
    adventure_path = os.path.join(ADVENTURES_DIR, adventure_id)
    
    # Cargar contexto
    with open(os.path.join(adventure_path, 'context.json'), 'r') as f:
        context = json.load(f)
        
    # Leer historia actual
    with open(os.path.join(adventure_path, 'adventure.md'), 'r', encoding='utf-8') as f:
        story = f.read()
        
    # Obtener nueva instrucción
    user_prompt = request.form['prompt']
    
    # Generar el siguiente capítulo
    print(f"--- Generando capítulo para '{adventure_id}' ---")
    print(f"Prompt del usuario: {user_prompt}")
    next_chapter = generate_next_chapter(
        context['title'],
        context['world'],
        context['characters'],
        story,
        user_prompt
    )
    print(f"Capítulo generado: {next_chapter[:100]}...") # Imprimir los primeros 100 caracteres

    # Añadir el nuevo capítulo a la historia
    if next_chapter:
        with open(os.path.join(adventure_path, 'adventure.md'), 'a', encoding='utf-8') as f:
            f.write("\n\n" + next_chapter)
        print("--- Capítulo añadido correctamente. ---")
    else:
        print("--- El capítulo generado estaba vacío. No se añadió nada. ---")
        
    return redirect(url_for('adventure', adventure_id=adventure_id))

if __name__ == '__main__':
    app.run(debug=True, port=5002)
