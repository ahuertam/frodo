import time
import random
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuración de Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- CONFIGURACIÓN ---
# Ejemplo: Buscar "Castlevania SNES" en Vinted, ordenado por más recientes
# NOTA: Cambia esta URL por la búsqueda exacta que quieras monitorizar tras aplicar filtros manualmente en la web.
TARGET_URL = "https://www.vinted.es/catalog?search_text=castlevania+snes&order=newest_first" 
REFRESH_INTERVAL_MIN = 30  # Segundos mínimos
REFRESH_INTERVAL_MAX = 90  # Segundos máximos

def setup_driver():
    """Configura el navegador Chrome."""
    options = Options()
    # options.add_argument("--headless") # Descomentar para ejecutar sin ventana
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Evitar detección de bot básica
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # User Agent para parecer un navegador normal
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=options)
    # Truco extra para engañar a detecciones de JS
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver


# Guardar historial para no repetir (simple set en memoria)
seen_urls = set()
found_items_history = []

def generate_html(items, status_message="Esperando..."):
    """Genera una página HTML simple con los resultados."""
    current_time = time.strftime('%H:%M:%S')
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="refresh" content="5"> <!-- Auto-reload cada 5s -->
        <title>Sniper: {len(items)} items</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: #f0f2f5; padding: 20px; }}
            h1 {{ text-align: center; color: #333; }}
            .status {{ text-align: center; color: #666; font-size: 0.9em; margin-bottom: 20px; }}
            .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 20px; }}
            .card {{ background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 5px rgba(0,0,0,0.1); transition: transform 0.2s; }}
            .card:hover {{ transform: translateY(-5px); }}
            .card img {{ width: 100%; height: 200px; object-fit: cover; }}
            .content {{ padding: 15px; }}
            .price {{ color: #09b1ba; font-weight: bold; font-size: 1.2em; }}
            .title {{ margin: 10px 0; font-size: 0.9em; height: 40px; overflow: hidden; }}
            .btn {{ display: block; background: #09b1ba; color: white; text-align: center; padding: 10px; text-decoration: none; border-radius: 4px; margin-top: 10px; }}
            .btn:hover {{ background: #078a91; }}
            .timestamp {{ font-size: 0.7em; color: #888; margin-top: 5px; text-align: right; }}
        </style>
    </head>
    <body>
        <h1>🎯 Sniper Results ({len(items)})</h1>
        <div class="status">
            Último escaneo: <strong>{current_time}</strong> <br>
            Estado: {status_message}
        </div>
        <div class="grid">
    """
    
    for item in items:
        html_content += f"""
            <div class="card">
                <img src="{item.get('image', 'https://via.placeholder.com/200')}" alt="Item">
                <div class="content">
                    <div class="price">{item.get('price', '???')}</div>
                    <div class="title">{item.get('title', 'Sin Título')}</div>
                    <a href="{item.get('url', '#')}" target="_blank" class="btn">Ver en Vinted</a>
                    <div class="timestamp">Detectado: {item.get('found_at', '')}</div>
                </div>
            </div>
        """
    
    html_content += """
        </div>
    </body>
    </html>
    """
    
    try:
        with open("results.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        # print("✨ HTML actualizado: results.html") # No es necesario spammear la consola
    except Exception as e:
        print(f"Error escribiendo HTML: {e}")


def filter_by_keywords(title, query):
    """Devuelve True si el título contiene TODAS las palabras clave significativas."""
    title_lower = title.lower()
    # Palabras comunes que ignoramos para evitar falsos negativos (ej. "Zelda para 3DS")
    stop_words = {"de", "del", "la", "el", "en", "y", "con", "para", "for", "with", "the"}
    
    query_words = [w.lower() for w in query.split()]
    meaningful_words = [w for w in query_words if w not in stop_words]
    
    # Si tras filtrar no queda nada (ej. busco "el de la"), usamos la query original
    if not meaningful_words:
        meaningful_words = query_words

    # Lógica AND: Todas las palabras significativas deben estar en el título
    for word in meaningful_words:
        if word not in title_lower:
            return False
            
    return True

def scan_wallapop(driver, url, query_original):
    """Escanea la página de resultados de Wallapop."""
    print(f"🔍 Escaneando Wallapop...")
    driver.get(url)
    
    status_msg = "Escaneo completado sin novedades."
    
    # Check simple de seguridad/bloqueo
    if "Cloudflare" in driver.title or "Access denied" in driver.title:
        print("⚠️ BLOQUEO DETECTADO: Wallapop sospecha que eres un robot.")
        print("👉 Por favor, resuelve el CAPTCHA en la ventana del navegador si aparece.")
        time.sleep(15) 

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
        )
        driver.execute_script("window.scrollTo(0, 300);")
        time.sleep(2)
    except Exception as e:
        print("⚠️ Timeout cargando Wallapop.")
        pass

    items_elements = driver.find_elements(By.CSS_SELECTOR, "a[href*='/item/']")
    
    if not items_elements:
         items_elements = driver.find_elements(By.CSS_SELECTOR, "div.ItemCardList__item")
    
    # DEBUG: Ver qué está pasando
    print(f"🔎 Items crudos encontrados (antes de filtrar): {len(items_elements)}")
    if len(items_elements) == 0:
        print("📸 Guardando captura de depuración: debug_wallapop.png")
        try:
            driver.save_screenshot("debug_wallapop.png")
        except:
            pass

    new_items_count = 0
    unique_elements = {}
    for el in items_elements:
        try:
            h = el.get_attribute("href")
            if h and h not in unique_elements:
                unique_elements[h] = el
        except:
            pass
            
    # Iteramos limitando a 30 para revisar más items (Wallapop mete mucha basura al principio)
    for url, element in list(unique_elements.items())[:30]:
        try:
            url = url.split("?")[0]
            
            title = element.get_attribute("title")
            if not title:
                title = element.text.split("\n")[0]
            
            if not title or len(title) < 3:
                title = "Item Wallapop"

            # --- FILTRO DE RELEVANCIA ---
            if not filter_by_keywords(title, query_original):
                # print(f"👻 Ignorado (No es {query_original}): {title}")
                continue
            # ---------------------------

            if url in seen_urls:
                continue
                
            price = "Consultar"
            text_content = element.text
            import re
            price_match = re.search(r'(\d+[\.,]?\d*\s?€)', text_content)
            if price_match:
                price = price_match.group(1)
            
            image_src = ""
            try:
                img_elem = element.find_element(By.TAG_NAME, "img")
                image_src = img_elem.get_attribute("src")
            except:
                pass

            item_data = {
                "title": title,
                "price": price,
                "url": url,
                "image": image_src,
                "found_at": time.strftime('%H:%M:%S')
            }
            
            seen_urls.add(url)
            found_items_history.insert(0, item_data)
            new_items_count += 1
            print(f"✅ Nuevo item Wallapop: {title} - {price}")
            
        except Exception as e:
            continue
    
    if new_items_count > 0:
        status_msg = f"✨ ¡{new_items_count} nuevos items encontrados!"
        print(status_msg)
    else:
        print("💤 Nada nuevo en Wallapop...")
    
    generate_html(found_items_history, status_message=status_msg)

def scan_vinted(driver, url, query_original):
    """Escanea la página de resultados de Vinted."""
    print(f"🔍 Escaneando Vinted...")
    driver.get(url)
    
    status_msg = "Escaneo completado sin novedades."
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.feed-grid__item, div.web_ui__ItemBox__container"))
        )
    except Exception as e:
        print("⚠️ No se detectaron items o tardó mucho en cargar.")
        generate_html(found_items_history, status_message="Error: No se detectaron items (Timeout)")
        return

    items_elements = driver.find_elements(By.CSS_SELECTOR, "div.feed-grid__item, div.web_ui__ItemBox__container")
    
    new_items_count = 0
    
    for element in items_elements[:30]: # Aumentado el límite de items a revisar
        try:
            try:
                link_elem = element.find_element(By.TAG_NAME, "a")
                url_raw = link_elem.get_attribute("href")
                url = url_raw.split("?")[0]
                title = link_elem.get_attribute("title") 
                if not title: 
                    title = element.text.split("\n")[0]
            except:
                url = "#"
                title = "Desconocido"

            # --- FILTRO DE RELEVANCIA ---
            if not filter_by_keywords(title, query_original):
                # print(f"👻 Ignorado (No es {query_original}): {title}")
                continue
            # ---------------------------

            if url in seen_urls:
                continue
                
            lines = element.text.split("\n")
            price = "N/A"
            for line in lines:
                if "€" in line:
                    price = line
                    break
            
            try:
                img_elem = element.find_element(By.TAG_NAME, "img")
                image_src = img_elem.get_attribute("src")
            except:
                image_src = ""

            item_data = {
                "title": title,
                "price": price,
                "url": url,
                "image": image_src,
                "found_at": time.strftime('%H:%M:%S')
            }
            
            seen_urls.add(url)
            found_items_history.insert(0, item_data) 
            new_items_count += 1
            print(f"✅ Nuevo item: {title} - {price}")
            
        except Exception as e:
            continue
    
    if new_items_count > 0:
        status_msg = f"✨ ¡{new_items_count} nuevos items encontrados!"
        print(status_msg)
    else:
        print("💤 Nada nuevo...")
    
    generate_html(found_items_history, status_message=status_msg)

def main():
    import webbrowser
    import os

    print("🔫 Iniciando Agente Sniper...")
    
    # Inputs interactivos
    print("\n--- CONFIGURACIÓN DE MISIÓN ---")
    query = input("¿Qué quieres buscar? (ej. Jordan, Zelda, iPhone): ").strip()
    print("Elige plataforma:")
    print("1. Vinted")
    print("2. Wallapop")
    platform = input("Opción (1/2): ").strip()
    
    target_url = ""
    is_vinted = True
    
    if platform == "2":
        formatted_query = query.replace(" ", "%20")
        target_url = f"https://es.wallapop.com/app/search?keywords={formatted_query}&order_by=newest"
        is_vinted = False
        print(f"🎯 Objetivo fijado: Wallapop -> {query}")
        print("💡 CONSEJO: Si no ves resultados, scroll manual en el navegador abierto puede ayudar.")
    else:
        formatted_query = query.replace(" ", "+")
        target_url = f"https://www.vinted.es/catalog?search_text={formatted_query}&order=newest_first"
        is_vinted = True
        print(f"🎯 Objetivo fijado: Vinted -> {query}")

    # Auto-abrir HTML al inicio
    results_path = os.path.abspath("results.html")
    if not os.path.exists(results_path):
        # Crear un dummy inicial si no existe
        generate_html([], status_message="Iniciando agente...")
    
    print(f"🚀 Abriendo dashboard: {results_path}")
    webbrowser.open(f"file://{results_path}")

    print("Pulsa Ctrl+C para detener.")
    
    driver = setup_driver()
    
    try:
        while True:
            if is_vinted:
                scan_vinted(driver, target_url, query)
            else:
                scan_wallapop(driver, target_url, query)
            
            sleep_time = random.randint(REFRESH_INTERVAL_MIN, REFRESH_INTERVAL_MAX)
            print(f"⏳ Esperando {sleep_time} segundos para el siguiente escaneo...")
            time.sleep(sleep_time)
            
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo agente...")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
