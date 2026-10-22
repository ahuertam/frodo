from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os

from encounter_engine import EncounterInput, generate_encounter, LOCATIONS, SCENES_LONG_ARM
from exports import foundry_journal_entry, roll20_handout_text

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env.local"))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, "..", ".env.local"))

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.get("/")
def index():
    return render_template(
        "index.html",
        scenes_long_arm=SCENES_LONG_ARM,
        locations=LOCATIONS,
    )


@app.post("/api/generate")
def api_generate():
    payload = request.get_json(silent=True) or {}

    inp = EncounterInput(
        system=str(payload.get("system") or "Star Wars: Al Filo del Imperio"),
        module=str(payload.get("module") or "El Largo Brazo del Hutt"),
        scene=payload.get("scene") or None,
        mode=str(payload.get("mode") or "mixto"),
        seed=(str(payload.get("seed")) if payload.get("seed") is not None else None),
        party=str(payload.get("party") or "4-5 medio"),
        emphasis=str(payload.get("emphasis") or "variedad"),
        keywords=str(payload.get("keywords") or ""),
        title=str(payload.get("title") or ""),
        hook=str(payload.get("hook") or ""),
        objective=str(payload.get("objective") or ""),
        opposition=str(payload.get("opposition") or ""),
        pressure=str(payload.get("pressure") or ""),
        twist=str(payload.get("twist") or ""),
        terrain=str(payload.get("terrain") or ""),
        rewards=str(payload.get("rewards") or ""),
        kind=str(payload.get("kind") or "escena"),
        location=str(payload.get("location") or ""),
        from_location=str(payload.get("from_location") or ""),
        to_location=str(payload.get("to_location") or ""),
    )

    enc = generate_encounter(inp)

    return jsonify(
        {
            "encounter": enc.to_dict(),
            "markdown": enc.to_markdown(),
            "exports": {
                "foundry": foundry_journal_entry(enc),
                "roll20": roll20_handout_text(enc),
            },
        }
    )


if __name__ == "__main__":
    app.run(debug=True, port=5010)
