# Agente Altamira (Ilustrador) 🎨

Altamira es un agente diseñado para dar vida visual a tus textos. Lee fragmentos de texto y genera ilustraciones digitales que representan la escena descrita, utilizando el título y el contenido como contexto.

## Objetivo
Crear acompañamiento visual para los audiolibros o textos procesados, ideal para vídeos de YouTube o contenido multimedia. Mantiene la filosofía de "coste cero" utilizando APIs públicas gratuitas para la generación de imágenes.

## Estructura
```
Altamira/
├── texts/          # Carpeta de entrada para tus archivos .txt o carpetas de capítulos
├── results/        # Carpeta de salida (se crean subcarpetas por libro)
├── altamira.py     # Script principal
├── doc.md          # Esta documentación
└── venv/           # Entorno virtual (si es necesario)
```

## Tecnología
*   **Lenguaje**: Python 3
*   **Generación de Imágenes**: Pollinations.ai (API gratuita, no requiere Key).
*   **Lógica**:
    1.  Lee el archivo de texto.
    2.  Extrae un "prompt" del contenido (usando el título + primeras frases o resumen simple).
    3.  Solicita la imagen a la API.
    4.  Guarda la imagen en la carpeta de resultados.

## Uso
1.  Coloca tus textos en `texts/`.
2.  Ejecuta `python3 altamira.py`.
3.  Selecciona el texto.
4.  Revisa `results/` para ver tus obras de art.
