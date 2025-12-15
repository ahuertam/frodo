# Agente Salomon (Divisor de Textos)

Salomon es un agente auxiliar diseñado para preparar libros completos para el Agente Narrador. Su función es dividir archivos de texto grandes en fragmentos manejables y numerados.

## 🎯 Objetivo
Evitar errores por límites de caracteres en los motores TTS y facilitar la gestión de audiolibros largos (capítulos individuales).

## 📂 Estructura
*   `Salomon/`
    *   `books/`: 📥 Carpeta de entrada. Aquí pones el libro completo (ej. `Don_Quijote.txt`).
    *   `texts/`: 📤 Carpeta de salida. Aquí aparecerán los fragmentos (ej. `Don_Quijote_01.txt`, `Don_Quijote_02.txt`...).
    *   `salomon.py`: Script de división inteligente.

## ⚙️ Funcionamiento
1.  Busca archivos `.txt` en la carpeta `books/`.
2.  Pregunta cuál procesar.
3.  Divide el texto basándose en un límite de caracteres (por defecto 5000 aprox) respetando los párrafos para no cortar frases a la mitad.
4.  Guarda los archivos numerados en `texts/`.

## 🚀 Uso
```bash
# Desde la carpeta Salomon
python3 salomon.py
```
(No requiere dependencias externas, usa librerías estándar de Python).
