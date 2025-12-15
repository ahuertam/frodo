import os

# Configuración
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOKS_DIR = os.path.join(BASE_DIR, "books")
TEXTS_OUTPUT_DIR = os.path.join(BASE_DIR, "texts")

CHUNK_SIZE = 4500 # Caracteres aprox por archivo (Edge-TTS va bien con < 5000)

def list_books():
    return [f for f in os.listdir(BOOKS_DIR) if f.endswith(".txt")]

def filter_content(text):
    """
    Intenta limpiar el contenido para quedarse con el Título y los Capítulos,
    ignorando licencias, editoriales, dedicatorias, etc.
    """
    lines = text.split("\n")
    if not lines:
        return text

    # 1. Intentar rescatar el Título (asumimos que está en las primeras líneas)
    # Buscamos la primera línea no vacía que no sea "LIBRO DESCARGADO..."
    title = "Audiolibro"
    for i in range(min(10, len(lines))):
        line = lines[i].strip()
        if line and not "DESCARGADO" in line and not "WWW" in line:
            title = line
            break
            
    filtered_lines = [title, ""] # Empezamos con el título
    
    # 2. Buscar dónde empieza la acción (Capítulo 1, I, Uno...)
    start_keywords = ["CAPÍTULO I", "CAPITULO I", "CAPÍTULO 1", "CAPITULO 1", "START OF THE PROJECT", "COMIENZO"]
    start_index = -1
    
    for i, line in enumerate(lines):
        # Aplanar para búsqueda
        norm_line = line.upper().strip()
        # Buscamos coincidencia exacta o inicio fuerte
        for kw in start_keywords:
            if norm_line == kw or norm_line.startswith(kw + " "):
                start_index = i
                break
        if start_index != -1:
            break
            
    if start_index != -1:
        print(f"🎯 Detectado inicio de contenido en línea {start_index}: '{lines[start_index]}'")
        content_body = lines[start_index:]
    else:
        print("⚠️ No se detectó marcador de 'CAPÍTULO I'. Procesando todo el archivo...")
        content_body = lines # Si no encuentra, usa todo por seguridad
        
    # 3. Eliminar footers comunes (Fin, Gracias, Webs...)
    final_body = []
    for line in content_body:
        norm = line.upper()
        if "FIN DEL LIBRO" in norm or "WWW.ELEJANDRIA.COM" in norm or "END OF PROJECT GUTENBERG" in norm:
            break
        final_body.append(line)
        
    filtered_lines.extend(final_body)
    return "\n".join(filtered_lines)

def split_text(text, limit):
    """Divide el texto en fragmentos respetando saltos de línea."""
    
    # Pre-filtrado inteligente
    clean_text_content = filter_content(text)
    
    paragraphs = clean_text_content.split("\n")
    chunks = []
    current_chunk = []
    current_length = 0
    
    for para in paragraphs:
        if not para.strip():
            continue
            
        # Si el párrafo actual ya supera el límite él solo (caso raro), lo forzamos
        if len(para) > limit:
            # Si el chunk actual tiene algo, guardamos
            if current_chunk:
                chunks.append("\n".join(current_chunk))
                current_chunk = []
                current_length = 0
            
            # El párrafo gigante se añade como un chunk propio
            chunks.append(para)
            continue

        if current_length + len(para) > limit:
            # Cerrar chunk actual
            chunks.append("\n".join(current_chunk))
            current_chunk = [para]
            current_length = len(para)
        else:
            current_chunk.append(para)
            current_length += len(para)
    
    # Añadir lo que falte
    if current_chunk:
        chunks.append("\n".join(current_chunk))
        
    return chunks

def main():
    print("✂️  AGENTE SALOMON - DIVISOR DE LIBROS  ✂️")
    print("==========================================")
    
    # Asegurar directorios
    os.makedirs(BOOKS_DIR, exist_ok=True)
    os.makedirs(TEXTS_OUTPUT_DIR, exist_ok=True)

    files = list_books()
    if not files:
        print(f"❌ No hay libros en '{BOOKS_DIR}'.")
        print("📥 Copia allí tu archivo .txt grande.")
        return

    print("\n📚 Libros disponibles:")
    for idx, f in enumerate(files):
        print(f"{idx + 1}. {f}")
    
    try:
        selection = int(input("\nElige un libro (número): ")) - 1
        if selection < 0 or selection >= len(files):
            print("❌ Selección inválida.")
            return
        book_name = files[selection]
    except ValueError:
        print("❌ Debes escribir un número.")
        return

    file_path = os.path.join(BOOKS_DIR, book_name)
    print(f"\n📖 Leyendo '{book_name}'...")
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            full_text = f.read()
    except Exception as e:
        print(f"❌ Error leyendo archivo: {e}")
        return

    print(f"✅ Texto cargado ({len(full_text)} caracteres).")
    
    # Opción de Exportación Directa
    NARRATOR_DIR = os.path.join(BASE_DIR, "../Narrator/texts")
    base_name = os.path.splitext(book_name)[0].replace(" ", "_").lower()
    
    target_dir = TEXTS_OUTPUT_DIR
    
    if os.path.exists(NARRATOR_DIR):
        print(f"\n🚀 Detectado agente Narrator en: {NARRATOR_DIR}")
        save_direct = input(f"¿Guardar directamente en Narrator/texts/{base_name}? (S/n): ").strip().lower()
        
        if save_direct == "" or save_direct == "s":
            target_dir = os.path.join(NARRATOR_DIR, base_name)
    
    print("procesando división inteligente...")
    
    fragments = split_text(full_text, CHUNK_SIZE)
    
    # Crear directorio si no existe (Salomon/texts o Narrator/texts/libro)
    os.makedirs(target_dir, exist_ok=True)
    
    print(f"\n✨ Generando {len(fragments)} fragmentos en '{target_dir}':")
    
    for i, fragment in enumerate(fragments):
        idx_str = str(i + 1).zfill(3) # 001, 002, 003...
        out_name = f"{base_name}_part{idx_str}.txt"
        out_path = os.path.join(target_dir, out_name)
        
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(fragment)
        print(f"  -> 📄 {out_name} ({len(fragment)} chars)")
        
    print(f"\n✅ ¡Hecho! Los archivos están listos en:")
    print(f"📂 {target_dir}")

if __name__ == "__main__":
    main()
