# Ideas2: Agentes Creativos para Juegos de Rol (Coste 0 / Ejecución Local)

Este documento recopila ideas de nuevos agentes orientados a juegos de rol (mesa, solo-RPG, campañas online) que pueden reutilizar lo que ya existe en este repo o proponer módulos nuevos.

## Criterios
- **Coste:** 0€ (Ejecución local / capas gratuitas cuando apliquen).
- **Control:** Offline-first (Python, Ollama, assets locales).
- **Salida útil:** Markdown/JSON listos para guardar en campaña, imprimir o importar.

---

## 1. Director de Escena (Scene Director)
Un agente que convierte una intención (“quiero una escena de interrogatorio tensa”) en una escena jugable con ritmo.
- **Funcionamiento:** Genera objetivo de la escena, apuestas, 3 giros posibles, relojes de tensión, y 10 “reacciones” de PNJ. Opcional: variantes según sistema (OSR, 5e, Fate, PbtA).
- **Stack:** Narrator + Cronista + LLM local.
- **Monetización:** Packs de “Escenas listas” por género; servicio de prep express para DMs.
- **Dificultad:** Baja.

## 2. Motor de Rumores (Rumor Mill)
Un generador de ganchos que simula el “boca a boca” de una ciudad o región.
- **Funcionamiento:** Produce 30 rumores con etiquetas (verdadero/falso/medio), fuente probable (borracho, mercader, culto), y “pista verificable” en el mundo. Incluye una tabla d100 imprimible.
- **Stack:** Cronista (almacenamiento de campaña) + LLM local.
- **Monetización:** Tablas premium por ambientación (piratas, noir, grimdark).
- **Dificultad:** Baja.

## 3. PNJ Vivo (NPC Engine)
Un agente que crea PNJs que “se sostienen” sesión tras sesión.
- **Funcionamiento:** Genera rasgos, voz, secretos, necesidades, relación con 3 facciones, agenda semanal y un “modo de combate social” (qué hace si se le presiona). Mantiene estado y evoluciona según eventos.
- **Stack:** Charactor (base de personajes) + Cronista (estado) + LLM local.
- **Monetización:** Servicio para DMs: “50 PNJs persistentes para tu campaña”.
- **Dificultad:** Media.

## 4. Bardo Procedimental (Theme & Motif Bard)
Música y motivos narrativos para escenas, lugares y personajes.
- **Funcionamiento:** Asigna leitmotifs (instrumentación/tempo/tono) a personajes y facciones, y propone “cambios de tema” cuando sube la tensión. Exporta un “plan de audio” por sesión.
- **Stack:** Bardo + sfxDrama (capas de ambiente/FX) + biblioteca local de audio.
- **Monetización:** Packs de soundscapes temáticos; suscripción por “kits de sesión”.
- **Dificultad:** Media.

## 5. Cartógrafo de Bolsillo (Pocket Cartographer)
Mapas rápidos para jugar ya, con consistencia interna.
- **Funcionamiento:** A partir de 5 inputs (“ciudad portuaria”, “tensión entre gremios”), genera mapa lógico (distritos, puntos de interés, rutas) y versiones: DM (con secretos) y Jugadores (limpia). Entrega en JSON + Markdown.
- **Stack:** Magallanes + Delineante.
- **Monetización:** Mapas por encargo; packs de ciudades modulares.
- **Dificultad:** Media.

## 6. Arquitecto de Mazmorras (Dungeon Architect)
Generación de dungeons con ritmo, riesgo y recompensa.
- **Funcionamiento:** Define propósito (tumba, mina, laboratorio), crea “bloques” (entrada, amenaza, giro, tesoro), rellena salas con pistas interconectadas y una “regla de justicia” (por qué está así). Incluye 3 rutas alternativas.
- **Stack:** LLM local + salida compatible con Delineante/Magallanes.
- **Monetización:** Libro digital de dungeons generados; servicio a grupos.
- **Dificultad:** Media.

## 7. Guionista de Combates Interesantes (Encounter Composer)
Encuentros que no son solo “pegar hasta que caiga”.
- **Funcionamiento:** Para un nivel/tono dado, genera objetivo secundario, terreno con interacción, “amenaza de reloj”, y 3 “complicaciones” si el grupo arrasa. Incluye versión no-letal y social.
- **Stack:** Narrator + LLM local.
- **Monetización:** Packs de encuentros por sistema/bioma.
- **Dificultad:** Baja.

## 8. Traductor de Sistemas (System Adapter)
Convierte material entre sistemas manteniendo intención y balance razonable.
- **Funcionamiento:** Toma un monstruo/PNJ/objeto y lo adapta a otro sistema: conserva rol (tanque, controlador, emboscador), recalcula números y propone diales de dificultad. Incluye “explicación de conversión” en 5 bullets.
- **Stack:** Salomon (si actúa como árbitro/reglas) + LLM local.
- **Monetización:** Servicio de adaptación para creadores de contenido; bundles de conversiones.
- **Dificultad:** Alta (depende del sistema).

## 9. Editor de Handouts (Prop Forge)
Convierte lore en materiales de mesa: cartas, notas, diarios, anuncios.
- **Funcionamiento:** Genera handouts en Markdown listos para imprimir, con variaciones (manchado, cifrado, incompleto). Produce también “pistas falsas” con coherencia.
- **Stack:** LLM local + assets de tipografías/plantillas locales.
- **Monetización:** Packs de handouts por campaña; tienda de props digitales.
- **Dificultad:** Media.

## 10. Director de Misterios (Mystery Runner)
Estructura un misterio para que sea resoluble sin railroading.
- **Funcionamiento:** Construye red de pistas (mínimo 3 pistas por conclusión), sospechosos con coartadas, y “fallos seguros” (si los jugadores se pierden, cómo reinyectar información). Entrega una matriz de pistas.
- **Stack:** Narrator + Cronista + LLM local.
- **Monetización:** Paquetes de misterios one-shot; servicio para clubes/tiendas.
- **Dificultad:** Alta (requiere consistencia).

## 11. Simulador de Facciones (Faction Simulator)
Un “mundo que se mueve” entre sesiones sin que el DM se vuelva loco.
- **Funcionamiento:** Define facciones con recursos, objetivos, estilo y tolerancia al riesgo. Entre sesiones corre un “turno de facciones” y actualiza: rumores, cambios de control, conflictos y oportunidades.
- **Stack:** Cronista (estado de campaña) + LLM local.
- **Monetización:** Herramienta premium para DMs (plantillas por género).
- **Dificultad:** Media.

## 12. Inspector de Continuidad (Continuity Sniper)
Detecta contradicciones en la campaña y propone arreglos elegantes.
- **Funcionamiento:** Lee el registro (resúmenes, NPCs, eventos) y encuentra inconsistencias (“X murió”, “Y nunca conoció a Z”). Sugiere 2 retcons suaves y 1 explicación diegética.
- **Stack:** Cronista + LLM local.
- **Monetización:** Servicio para campañas largas; “auditorías” de canon.
- **Dificultad:** Media.

## 13. Maestro de Climas y Viajes (Weather & Travel Master)
Viajes que importan sin ser tediosos.
- **Funcionamiento:** Genera clima, eventos de camino, consumo de recursos, decisiones significativas (atajo vs seguridad) y señales de mundo (ruinas, patrullas). Incluye modo “rápido” y modo “granular”.
- **Stack:** LLM local + tablas exportables a Markdown.
- **Monetización:** Packs de viajes por bioma/estación.
- **Dificultad:** Baja.

## 14. Controlador de Mesa Online (VTT Packager)
Empaqueta sesión en un set importable (notas, tokens, handouts, música).
- **Funcionamiento:** A partir del prep (Markdown/JSON), genera estructura de carpetas, nombres consistentes, y manifiesto. Puede integrar mapas, handouts y pistas de audio en un “kit de sesión”.
- **Stack:** Cronista + Magallanes + Bardo + sfxDrama.
- **Monetización:** Kits por sesión; servicio para streams.
- **Dificultad:** Alta (formatos VTT).

## 15. Modo Solo-RPG (Oracle Weaver)
Oráculos, tablas y “empujones narrativos” para jugar en solitario.
- **Funcionamiento:** Genera oráculo sí/no con matiz, tablas de complicaciones, temas, NPCs y escenas. Mantiene un log de “hechos” para que la historia no se contradiga.
- **Stack:** Narrator + Cronista + LLM local.
- **Monetización:** Packs de oráculos por género; app offline.
- **Dificultad:** Media.

---

## Notas de integración (rápidas)
- **Cronista** como núcleo de memoria: eventos, estado de facciones, PNJs persistentes y continuidad.
- **Narrator** para estructura jugable: escenas, misterios, encuentros.
- **Charactor** para fichas: PNJs/PCs, relaciones, inventarios base.
- **Magallanes/Delineante** para mapa lógico + representación.
- **Bardo/sfxDrama** para la capa sensorial: música, ambiente y efectos.
