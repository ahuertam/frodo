# EncounterComposer — Generador de encuentros ⚔️

## Qué hace
Genera un encuentro RPG de una página (modo **escena** o **interludio**) y lo exporta a **Foundry VTT**
(Journal Entry JSON) o **Roll20** (texto para handout). No guarda nada en disco. Web en `:5010`.

## Archivos clave

| Archivo | Función |
|---|---|
| `encounter_engine.py` | Motor determinista. Sin Flask, sin red. |
| `exports.py` | Serializadores a Foundry y Roll20 |
| `app.py` | Solo parsea el formulario y renderiza |
| `requirements.txt` | `flask`, `python-dotenv` |

## La decisión de diseño: aquí no hay LLM, a propósito

Es el único agente del repo que genera contenido estructurado **sin modelo**, y es deliberado:

- `@dataclass(frozen=True)` para el contrato de entrada — inmutable, autodescriptivo.
- `random.Random(seed)` en vez de `random` global — la misma semilla reproduce el mismo encuentro.
- Cascada de defaults para que una entrada vacía produzca un encuentro usable, no un error.
- La capa Flask no toca la lógica: `app.py` importa el motor y lo llama.

El criterio: cuando el contenido es estructurado, repetible y tiene que ser correcto, un LLM no aporta
— aporta varianza y alucinación. Cuando el contenido es abierto y la varianza es el objetivo (Magallanes,
Cronista), el LLM sí aporta.

## Export y escaping

`exports.py` interpola campos del encounter en JSON, HTML y texto plano. **Todo campo inyectado pasa por
`html.escape()`** antes de entrar en el handout de Roll20 — sin eso, un nombre con `<` rompe el render o
inyecta markup.

## Notas
- Sin dependencias de IA: `requirements.txt` solo trae Flask.
- `brazohut.txt` es material de referencia local, git-ignorado.