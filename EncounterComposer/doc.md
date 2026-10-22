# Encounter Composer (web local)

## Qué hace

Genera un encuentro de 1 página para **Star Wars: Al Filo del Imperio**, con presets inspirados en escenas de *El Largo Brazo del Hutt*.

Modos:

- Escena: encuentro principal ligado a una escena del módulo
- Interludio: encuentro corto entre dos localizaciones (transiciones)

Incluye exportación:

- Foundry VTT: JSON de Journal Entry
- Roll20: TXT (para copiar/pegar en un handout)

No guarda nada en disco: genera y descarga en tu navegador.

## Ejecutar

```bash
cd EncounterComposer
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Abre:

http://127.0.0.1:5010/
