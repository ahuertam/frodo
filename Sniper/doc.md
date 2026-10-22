# Agente Sniper de Segunda Mano (Vinted/Wallapop)

Este documento describe el funcionamiento y desarrollo del agente "Sniper" diseñado para detectar oportunidades de arbitraje en plataformas de segunda mano.

## 🎯 Objetivo
Automatizar la búsqueda de artículos en **Vinted** y **Wallapop** para detectar oportunidades rápidas (chollos).

## 🚀 Cómo Lanzar
El proyecto usa un entorno virtual para evitar conflictos con macOS.

1.  **Ejecutar el Agente:**
    Desde la terminal en la carpeta `Sniper`:
    ```bash
    python3 sniper.py
    ```
2.  **Seguir las instrucciones en pantalla:**
    - Escribe qué quieres buscar (ej. "Zelda 3DS").
    - Elige la plataforma (1 para Vinted, 2 para Wallapop).

3.  **Ver Resultados:**
    El agente genera automáticamente un archivo **[results.html](./results.html)**. Ábrelo en tu navegador. Se actualiza solo cada 5 segundos.

---

## ⚙️ Características Actuales
1.  **Modo Interactivo:** No necesitas tocar código para cambiar de búsqueda.
2.  **Multi-Plataforma:**
    - ✅ **Vinted:** Muy estable.
    - ⚠️ **Wallapop:** Funcional pero con protecciones anti-bot fuertes (puede pedir CAPTCHA).
3.  **Dashboard en Vivo:**
    - Archivo `results.html` con fotos, precios y enlaces directos.
    - Timestamp de "Último escaneo" para verificar que sigue vivo.
4.  **Seguridad:**
    - User-Agent rotatorio (básico).
    - Esperas aleatorias (30-90s) para parecer humano.

## 🛠 Estructura
- `sniper.py`: El cerebro. Usa Selenium para navegar Chrome.
- `results.html`: La cara. Interfaz gráfica generada dinámicamente.
- `venv/`: Carpeta con las librerías necesarias (Selenium, etc).

## ⚠️ Solución de Problemas
- **"Connection Refused" al cerrar:** Es normal, significa que has cerrado el navegador a la fuerza con Ctrl+C.
- **Wallapop no encuentra nada:** Posible bloqueo de Cloudflare. Abre el navegador que lanza el bot y comprueba si te pide verificar que "eres humano".
