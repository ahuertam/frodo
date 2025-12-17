# Agente Delineante (Draftsman) 📐✏️

Delineante toma cualquier imagen y la redibuja en estilo isométrico, como un plano técnico dibujado a mano sobre papel cuadriculado.

## Objetivo
Transformar fotos o bocetos en ilustraciones técnicas artísticas mediante IA Generativa (Img2Img), proporcionando una interfaz web simple para usarlo localmente.

## Modos de Operación

### 🔑 Modo PREMIUM (con OpenAI API Key)
- **Análisis**: GPT-4 Vision analiza la imagen en detalle
- **Generación**: DALL-E 3 crea dibujos isométricos de alta calidad
- **Resultado**: Mejor comprensión del contenido y mayor fidelidad

### 🆓 Modo GRATUITO (sin API Key)
- **Análisis**: BLIP (HuggingFace) para captioning básico
- **Generación**: Pollinations.ai (Flux model)
- **Resultado**: Funcional pero con menor precisión

## Estructura
```
Delineante/
├── app.py              # Servidor Flask y lógica híbrida
├── requirements.txt    # Dependencias
├── .env.local          # API Keys (NO COMMITEAR)
├── .gitignore          # Protección de archivos sensibles
├── doc.md              # Documentación
├── templates/
│   └── index.html      # Interfaz Web
├── results/            # Resultados organizados por nombre de archivo
│   ├── castle/
│   │   ├── input.jpg
│   │   ├── isometric.jpg
│   │   ├── map_1.jpg
│   │   ├── map_2.jpg
│   │   └── ...
│   └── house/
│       └── ...
└── uploads/            # Imágenes temporales
```

## Tecnología
*   **Backend**: Python (Flask)
*   **AI Premium**: OpenAI (GPT-4 Vision + DALL-E 3)
*   **AI Gratuito**: HuggingFace (BLIP) + Pollinations.ai (Flux)
*   **Frontend**: HTML5 + CSS + JavaScript

## Instalación

### 1. Instalar dependencias
```bash
cd Delineante
pip install -r requirements.txt
```

### 2. Configurar API Key (Opcional - para modo premium)
Edita `.env.local` y añade tu clave:
```bash
OPENAI_API_KEY=sk-tu-clave-aqui
```

### 3. Ejecutar
```bash
python app.py
```
Acceder a `http://127.0.0.1:5000`

## Flujo de Trabajo
1.  **Subir**: Arrastra una foto a la web local
2.  **Analizar**: El sistema detecta automáticamente el contenido
3.  **Generar**: Crea el dibujo isométrico técnico
4.  **Resultado**: Descarga o regenera si es necesario

## Notas
- Sin API key, el sistema funciona en modo gratuito automáticamente
- El archivo `.env.local` está protegido por `.gitignore`
- DALL-E 3 produce resultados significativamente mejores que Pollinations
