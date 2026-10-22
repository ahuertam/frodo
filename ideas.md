# Ideas de agentes — backlog

Solo ideas que **reutilizan algo que ya existe en este repo** o que caen dentro del dominio tabletop /
creativo. El resto del brainstorming original (agentes de servicios, scraping, monetización) se movió a
`ahuertam/sniper`, que es privado: son ideas de negocio, no de producto, y no encajan junto a los agentes.

Para la línea de juegos de rol completa, ver [ideas2.md](./ideas2.md).

---

## 1. Agente de "Assets" para juegos y diseño

Generación masiva de recursos digitales para creativos.
- **Funcionamiento:** Stable Diffusion local para texturas, iconos y spritesheets (p. ej. "iconos de
  pociones"). Escala, recorta y empaqueta.
- **Se apoya en:** [Altamira](./Altamira) (llamada a Pollinations) y elmanejo de imagen de
  [Delineante](./Delineante). La parte nueva es el pipeline de recorte y empaquetado.
- **Monetización:** packs en Itch.io / Unity Asset Store.
- **Dificultad:** Media (requiere GPU).

## 2. Agente Narrador (audiolibros de dominio público)

Conversión de clásicos literarios a audio.
- **Funcionamiento:** descarga libros de Project Gutenberg (libres de derechos) y los narra con TTS
  neuronal local (Coqui TTS / XTTS) en vez de las voces cloud de Edge.
- **Se apoya en:** [Narrator](./Narrator). El TTS ya está resuelto y la segmentación viene de
  [Salomon](./Salomon); lo que falta es el motor local y la fuente Gutenberg.
- **Monetización:** subida a YouTube / Spotify.
- **Dificultad:** Media (ajustes de audio).