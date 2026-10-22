# Agente Narrador (Audiolibros Automáticos)

Este proyecto implementa la **Idea 6**: un agente capaz de convertir libros de texto en audiolibros narrados con voces neuronales de alta calidad de forma gratuita.

## 🎯 Objetivo
Transformar textos (libros de dominio público, artículos, fanfics) en archivos de audio `.mp3` listos para escuchar o publicar.

## 🛠 Stack Tecnológico
*   **Lenguaje:** Python 3.
*   **Motor de Voz:** `edge-tts`
    *   *Por qué:* Utiliza las voces neuronales de Microsoft Edge (Gratis, Sin límites estrictos, Calidad de estudio).
    *   *Ventaja:* No necesitas descargar modelos de 5GB ni tener una GPU potente como con Coqui TTS / XTTS.
*   **Gestión de Texto:** División inteligente de capítulos/párrafos.

## 📂 Estructura de Carpetas
*   `Narrator/`
    *   `texts/`: 📥 Aquí depositas los archivos `.txt` que quieres narrar.
    *   `generatedAuds/`: 📤 Aquí aparecerán los `.mp3` resultantes.
    *   `narrator.py`: El script principal.
    *   `doc.md`: Esta documentación.

## 🚀 Flujo de Trabajo
1.  **Preparación:** Copias un libro (ej. `dracula.txt`) a la carpeta `texts/`.
2.  **Ejecución:** Lanzas `python3 narrator.py` (o `./venv/bin/python3 narrator.py` si usas venv).
3.  **Selección:** El agente detecta los archivos en `texts/` y te pregunta cuál procesar.
4.  **Configuración:** Eliges la voz (Español Neutro, Castellano, Inglés, etc.) y la velocidad.
5.  **Generación:** El agente lee el texto y genera el audio en `generatedAuds/`.

## 📦 Instalación
Necesitaremos instalar la librería `edge-tts` y `asyncio` (estándar en Python).

```bash
# Crear entorno virtual (si no existe ya en frodo, crearemos uno específico para Narrator)
cd Narrator
python3 -m venv venv
./venv/bin/pip install edge-tts
```
