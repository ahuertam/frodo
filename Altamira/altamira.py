import os
import time
import requests
import textwrap
from urllib.parse import quote

# Configuración
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEXTS_DIR = os.path.join(BASE_DIR, "texts")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

def list_input_options():
    """Lista archivos y carpetas en TEXTS_DIR."""
    items = []
    if not os.path.exists(TEXTS_DIR):
        os.makedirs(TEXTS_DIR)
        
    for f in os.listdir(TEXTS_DIR):
        full_path = os.path.join(TEXTS_DIR, f)
        if f.startswith("."): continue # Ignorar ocultos
        
        if os.path.isfile(full_path) and f.endswith(".txt"):
            items.append({"type": "file", "name": f, "path": full_path})
        elif os.path.isdir(full_path):
            subfiles = [sf for sf in os.listdir(full_path) if sf.endswith(".txt")]
            if subfiles:
                items.append({"type": "folder", "name": f, "path": full_path, "count": len(subfiles)})
            
    items.sort(key=lambda x: x["name"])
    return items

def extract_prompt(text, title, limit=300):
    """
    Crea un prompt a partir del texto. 
    Toma las primeras líneas significativas para capturar la escena.
    """
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    content_sample = " ".join(lines)[:limit]
    
    # Prompt engineering básico para estilo
    style = "digital art, storybook illustration, fantasy style, highly detailed, cinematic lighting, 8k"
    
    # Construcción del prompt
    prompt = f"Scene from '{title}': {content_sample}. {style}"
    return prompt

def generate_image(prompt, output_path):
    """Genera imagen usando Pollinations.ai con reintentos."""
    encoded_prompt = quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Timeout aumentado a 90s para imágenes complejas
            response = requests.get(url, timeout=90)
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                return True
            else:
                print(f"      ⚠️ Error API ({response.status_code})...", end="")
        except Exception as e:
            print(f"      ⚠️ Error conexión ({str(e)[:50]})...", end="")
        
        # Exponential backoff: 2s, 4s, 8s
        wait_time = 2 ** (attempt + 1)
        if attempt < max_retries - 1:
            print(f" Reintentando en {wait_time}s")
            time.sleep(wait_time)
        else:
            print(" ❌ Abortando tras reintentos.")
            
    return False

def main():
    print("\n🎨  AGENTE ALTAMIRA - ILUSTRADOR  🎨")
    print("======================================")
    
    options = list_input_options()
    if not options:
        print(f"❌ No hay textos en '{TEXTS_DIR}'.")
        return

    print("\n📚 Lienzos disponibles (Textos):")
    for idx, item in enumerate(options):
        type_icon = "📄" if item["type"] == "file" else "gg"
        extra_info = f"({item['count']} escenas)" if item["type"] == "folder" else ""
        print(f"{idx + 1}. {type_icon} {item['name']} {extra_info}")

    try:
        sel = int(input("\nElige una opción: ")) - 1
        if sel < 0 or sel >= len(options): return
        selected = options[sel]
    except: return

    # Preparar tareas
    tasks = [] # (filepath, output_filename_base)
    book_title = selected["name"].replace("_", " ").title()
    
    if selected["type"] == "folder":
        folder_files = sorted([f for f in os.listdir(selected["path"]) if f.endswith(".txt")])
        out_folder = os.path.join(RESULTS_DIR, selected["name"])
        for f in folder_files:
            tasks.append({
                "path": os.path.join(selected["path"], f),
                "name": os.path.splitext(f)[0]
            })
    else:
        out_folder = os.path.join(RESULTS_DIR, "Single_Works")
        tasks.append({
            "path": selected["path"],
            "name": os.path.splitext(selected["name"])[0]
        })
        book_title = selected["name"]

    os.makedirs(out_folder, exist_ok=True)
    
    print(f"\n🚀 Generando {len(tasks)} ilustraciones para '{book_title}'...")
    print(f"📂 Guardando en: {out_folder}\n")

    pass_count = 1
    
    while True:
        # Detectar qué falta
        missing_tasks = []
        for t in tasks:
            img_path = os.path.join(out_folder, f"{t['name']}.jpg")
            if not os.path.exists(img_path):
                missing_tasks.append(t)
        
        if not missing_tasks:
            print(f"\n✨ ¡Colección completada al 100%! ({len(tasks)} imágenes)")
            break
            
        if pass_count > 1:
            print(f"\n🔄 Ronda {pass_count}: Faltan {len(missing_tasks)} imágenes. Reintentando en 10s...")
            time.sleep(10)
        
        for i, task in enumerate(missing_tasks):
            with open(task["path"], "r", encoding="utf-8") as f:
                text_content = f.read()
                
            if not text_content.strip(): continue

            prompt = extract_prompt(text_content, book_title)
            
            out_file_img = os.path.join(out_folder, f"{task['name']}.jpg")
            out_file_txt = os.path.join(out_folder, f"{task['name']}_prompt.txt")
            
            # Progreso relativo a la ronda actual
            print(f"[{i+1}/{len(missing_tasks)}] 🖌️  Ronda {pass_count} | Pintando: {task['name']}...")
            
            with open(out_file_txt, "w", encoding="utf-8") as f:
                f.write(prompt)
            
            success = generate_image(prompt, out_file_img)
            
            if success:
                print("   ✅ Imagen guardada.")
            else:
                print("   ❌ Pendiente para siguiente ronda.")
                
            time.sleep(3)
            
        pass_count += 1

    os.system(f"open '{out_folder}'")

if __name__ == "__main__":
    main()
