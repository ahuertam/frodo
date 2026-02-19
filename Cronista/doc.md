# Documentación de Cronista

Cronista es un agente inteligente diseñado para la creación y expansión de aventuras de rol. Utiliza un modelo de lenguaje avanzado (Google Gemini) para generar tramas dinámicas y coherentes a partir de la información que le proporciones.

## Características

-   **Generación de Aventuras:** Crea una nueva aventura a partir de un título, una descripción del mundo y una descripción de los personajes.
-   **Expansión Iterativa:** Continúa y expande una aventura existente proporcionando nuevas instrucciones o eventos.
-   **Interfaz Web:** Gestiona tus aventuras a través de una sencilla interfaz web.
-   **Almacenamiento Persistente:** Cada aventura se guarda en su propia carpeta, incluyendo la historia en formato Markdown y un archivo de contexto en JSON.

## ¿Cómo Empezar?

### 1. Configuración

Para que Cronista pueda generar las tramas utilizando la IA de Google, necesitas una clave de API.

1.  **Obtén tu API Key:** Visita [Google AI Studio](https://aistudio.google.com/app/apikey) y crea una nueva clave de API.
2.  **Crea el archivo de entorno:** En la raíz del proyecto, crea un archivo llamado `.env.local`.
3.  **Añade la clave al archivo:** Abre `.env.local` y añade la siguiente línea, reemplazando `TU_API_KEY` con la clave que has obtenido:

    ```
    GOOGLE_API_KEY=TU_API_KEY
    ```

Si no configuras la clave, la aplicación seguirá funcionando, pero en lugar de generar tramas con IA, creará textos de marcador de posición.

### 2. Ejecutar la Aplicación

Para iniciar Cronista, ejecuta el siguiente comando desde la raíz del proyecto:

```bash
python3 Cronista/app.py
```

Esto iniciará un servidor web local. Por defecto, podrás acceder a la aplicación en `http://127.0.0.1:5002`.

### 3. Uso de la Interfaz

-   **Página Principal:** Muestra una lista de todas las aventuras que has creado. Puedes hacer clic en cualquiera de ellas para verla o continuarla.
-   **Crear una Aventura:**
    -   **Título de la Aventura:** Un nombre para tu nueva historia.
    -   **Descripción del Mundo:** Describe el universo, sus ciudades, facciones, reglas mágicas, etc. Cuanto más detallado, mejor será la trama.
    -   **Descripción de los Personajes:** Describe a los protagonistas, sus motivaciones, habilidades y relaciones. Puedes pegar aquí la salida de otro agente como `Charactor`.
-   **Continuar una Aventura:**
    -   Dentro de la página de una aventura, encontrarás un área de texto. Escribe una instrucción sobre lo que quieres que suceda a continuación (por ejemplo, "Los héroes investigan el misterioso asesinato en el puerto" o "Aparece un dragón que ataca la ciudad").
    -   Al pulsar "Continuar la Aventura", la IA generará el siguiente capítulo basándose en tu instrucción y en todo lo que ha sucedido antes.

## Estructura de Archivos

Cada vez que creas una aventura, se genera una nueva carpeta dentro de `Cronista/adventures/`. El nombre de la carpeta es una versión "slug" del título de la aventura.

Dentro de cada carpeta de aventura, encontrarás:

-   `context.json`: Almacena el título, la descripción del mundo y de los personajes.
-   `adventure.md`: Contiene la historia completa de la aventura en formato Markdown.
