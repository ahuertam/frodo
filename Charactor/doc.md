# Agente Charactor (Creador de Personajes) 🎭

Charactor es un agente diseñado para generar perfiles de personajes profundos y visuales para tus novelas o juegos.

## Objetivo
Transformar una idea o arquetipo simple (ej: "Villano con miedo a las alturas") en una ficha completa de personaje y su retrato visual.

## Estructura
```
Charactor/
├── chars/          # Carpeta de salida (un subdirectorio por personaje)
├── charactor.py    # Script principal
├── doc.md          # Esta documentación
└── venv/           # Entorno virtual
```

## Arquitectura Propuesta (Sugerencia)
Para mantener el coste cero pero alta calidad:

### 1. Cerebro (Texto) 🧠
Necesitamos una IA capaz de inventar historias coherentes.
*   **Recomendación**: **Google Gemini API** (Tier Gratuito).
    *   *Pros*: Gratuito, contexto largo, muy inteligente.
    *   *Contras*: Requiere una API Key (se saca en 1 min).
*   **Alternativa**: HuggingFace Inference (Modelos Open Source).
    *   *Contras*: Más lento, respuestas a veces cortas o incoherentes.

### 2. Pincel (Imagen) 🎨
*   **Motor**: **Pollinations.ai** (Igual que Altamira).
*   *Workflow*: Usaremos la descripción física generada por el "Cerebro" para crear el prompt de la imagen.

## Flujo de Trabajo
1.  Ejecutas `python3 charactor.py`.
2.  Escribes tu idea: *"Una anciana que vende recuerdos en Marte"*.
3.  El agente conecta con la IA de Texto para generar:
    *   Nombre
    *   Biografía / Pasado
    *   Personalidad (Miedos, Deseos, Virtudes)
    *   Descripción Física
4.  El agente guarda la ficha en `chars/Nombre/perfil.md`.
5.  El agente envía la descripción física a Pollinations.
6.  El agente guarda el retrato en `chars/Nombre/retrato.jpg`.
