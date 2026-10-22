import os
import asyncio
import edge_tts
from datetime import datetime

# Configuración de carpetas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEXTS_DIR = os.path.join(BASE_DIR, "texts")
OUTPUT_DIR = os.path.join(BASE_DIR, "generatedAuds")

# Voces Recomendadas (Edge TTS)
VOICES = {
    "1": {"name": "Español (España) - Alvaro (H)", "id": "es-ES-AlvaroNeural"},
    "2": {"name": "Español (España) - Elvira (M)", "id": "es-ES-ElviraNeural"},
    "3": {"name": "Español (México) - Dalia (M)", "id": "es-MX-DaliaNeural"},
    "4": {"name": "Español (México) - Jorge (H)", "id": "es-MX-JorgeNeural"},
    "5": {"name": "Inglés (USA) - Guy (H)", "id": "en-US-GuyNeural"},
    "6": {"name": "Inglés (USA) - Jenny (M)", "id": "en-US-JennyNeural"},
}

def generate_audio(text, voice, output_path):
    """Genera el audio usando edge-tts (su API es asíncrona; aquí no paralelizamos)."""
    asyncio.run(edge_tts.Communicate(text, voice).save(output_path))

def clean_text(text):
    """Limpieza básica del texto."""
    # Eliminar saltos de línea excesivos
    paragraphs = text.split("\n")
    cleaned = [p.strip() for p in paragraphs if p.strip()]
    return "\n".join(cleaned)

def list_input_options():
    """Lista archivos .txt y carpetas en TEXTS_DIR."""
    items = []
    # 1. Archivos sueltos
    for f in os.listdir(TEXTS_DIR):
        full_path = os.path.join(TEXTS_DIR, f)
        if os.path.isfile(full_path) and f.endswith(".txt"):
            items.append({"type": "file", "name": f, "path": full_path})
        elif os.path.isdir(full_path):
            # Verificar si tiene txt dentro
            subfiles = [sf for sf in os.listdir(full_path) if sf.endswith(".txt")]
            if subfiles:
                items.append({"type": "folder", "name": f, "path": full_path, "count": len(subfiles)})
    
    items.sort(key=lambda x: x["name"])
    return items

def main():
    print("\n🎙️  AGENTE NARRADOR - STUDIO  🎙️")
    print("====================================")
    
    # 1. Seleccionar Input (Archivo o Carpeta)
    options = list_input_options()
    if not options:
        print(f"❌ No hay archivos .txt ni carpetas en '{TEXTS_DIR}'.")
        return

    print("\n📚 Biblioteca (Archivos y Carpetas):")
    for idx, item in enumerate(options):
        type_icon = "📄" if item["type"] == "file" else "📁"
        extra_info = f"({item['count']} partes)" if item["type"] == "folder" else ""
        print(f"{idx + 1}. {type_icon} {item['name']} {extra_info}")
    
    try:
        selection = int(input("\nElige una opción (número): ")) - 1
        if selection < 0 or selection >= len(options):
            print("❌ Selección inválida.")
            return
        selected_item = options[selection]
    except ValueError:
        print("❌ Debes escribir un número.")
        return

    # 2. Seleccionar Voz
    print("\n🗣️  Voces Disponibles:")
    for key, val in VOICES.items():
        print(f"{key}. {val['name']}")
    
    voice_opt = input("\nElige una voz (número): ").strip()
    selected_voice_id = VOICES.get(voice_opt, VOICES["1"])["id"]
    
    # 3. Preparar lista de trabajos
    tasks = []
    
    if selected_item["type"] == "file":
        tasks.append(selected_item["path"])
        # Output folder es la raíz de generatedAuds
        job_output_dir = OUTPUT_DIR 
    else:
        # Es una carpeta, cogemos todos los txt ordenados
        folder_path = selected_item["path"]
        files = sorted([f for f in os.listdir(folder_path) if f.endswith(".txt")])
        for f in files:
            tasks.append(os.path.join(folder_path, f))
        
        # Crear subcarpeta en output para organizar
        job_output_dir = os.path.join(OUTPUT_DIR, selected_item["name"])
    
    os.makedirs(job_output_dir, exist_ok=True)
    
    print(f"\n🚀 Iniciando trabajo: {len(tasks)} archivos a procesar.")
    print(f"📂 Salida: {job_output_dir}\n")

    # 4. Procesar cola
    for i, file_path in enumerate(tasks):
        filename = os.path.basename(file_path)
        progress = f"[{i+1}/{len(tasks)}]"
        print(f"{progress} 📖 Leyendo '{filename}'...")
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                raw_text = f.read()
            
            final_text = clean_text(raw_text)
            if not final_text:
                print(f"   ⚠️ Archivo vacío, saltando.")
                continue

            # Output name: mismo nombre pero mp3
            safe_name = os.path.splitext(filename)[0].replace(" ", "_")
            output_path = os.path.join(job_output_dir, f"{safe_name}.mp3")
            
            print(f"   ⏳ Generando audio ({len(final_text)} chars)...")
            generate_audio(final_text, selected_voice_id, output_path)
            print(f"   ✅ Guardado: {os.path.basename(output_path)}")
            
        except Exception as e:
            print(f"   ❌ ERROR CRÍTICO en '{filename}': {e}")
            print("⚠️  Deteniendo agente para evitar errores en cadena.")
            break
            
    print("\n✨ Proceso finalizado.")
    if selected_item["type"] == "folder":
        os.system(f"open '{job_output_dir}'")
    else:
        # Si era un solo archivo, abrimos la carpeta general
        os.system(f"open '{OUTPUT_DIR}'")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Agente detenido.")
