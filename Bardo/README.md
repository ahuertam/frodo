### Modo de Escucha en Tiempo Real (Audio con Deepgram)

Bardo puede escuchar el audio de tu micrófono en tiempo real y transcribirlo para generar imágenes sobre la marcha.

**Requisitos:**

-   Tener una clave de API de Deepgram configurada en el archivo `.env.local` con el nombre `DEEPGRAM_API_KEY`.
-   Tener un micrófono conectado y configurado en tu sistema.

**Cómo usarlo:**

1.  Crea un nuevo archivo de Python (por ejemplo, `run_realtime.py`) con el siguiente contenido:

    ```python
    import asyncio
    from Bardo.bardo import Bardo

    async def main():
        bardo = Bardo()
        await bardo.listen_realtime()

    if __name__ == "__main__":
        asyncio.run(main())
    ```

2.  Ejecuta el script desde tu terminal:

    ```bash
    python3 run_realtime.py
    ```

3.  Bardo abrirá una conexión con Deepgram y empezará a escuchar el audio de tu micrófono. Habla con claridad y, cuando termines una frase, Bardo la procesará. Si la frase contiene alguna de las palabras clave, se generará una nueva imagen en la galería.

4.  Para detener la escucha, vuelve a la terminal y pulsa la tecla `Enter`.
