from __future__ import annotations

from typing import Any
from html import escape

from encounter_engine import Encounter


def _p(text: str) -> str:
    return f"<p>{escape(text)}</p>" if text else ""


def encounter_to_html(enc: Encounter) -> str:
    parts: list[str] = []
    parts.append(f"<h1>{escape(enc.title)}</h1>")
    meta = f"<p><strong>Sistema:</strong> {escape(enc.system)}<br><strong>Fuente:</strong> {escape(enc.source)}<br><strong>Tipo:</strong> {escape(enc.kind)}"
    if enc.location:
        meta += f"<br><strong>Localización:</strong> {escape(enc.location)}"
    meta += "</p>"
    parts.append(meta)
    parts.append(f"<p><strong>Gancho:</strong> {escape(enc.hook)}</p>")

    parts.append("<h2>Objetivo(s)</h2>")
    parts.append("<ul>" + "".join([f"<li>{escape(o)}</li>" for o in enc.objectives]) + "</ul>")

    parts.append("<h2>Oposición</h2>")
    parts.append("<ul>" + "".join([f"<li>{escape(o)}</li>" for o in enc.opposition]) + "</ul>")

    parts.append("<h2>Terreno (5)</h2>")
    parts.append("<ul>" + "".join([f"<li>{escape(t)}</li>" for t in enc.terrain]) + "</ul>")

    parts.append("<h2>Presión</h2>")
    parts.append(_p(enc.pressure))

    parts.append("<h2>Giro</h2>")
    parts.append(_p(enc.twist))

    parts.append("<h2>Escalado</h2>")
    parts.append("<ul>" + "".join([
        f"<li><strong>Más fácil:</strong> {escape(enc.scaling_easier)}</li>",
        f"<li><strong>Más duro:</strong> {escape(enc.scaling_harder)}</li>",
    ]) + "</ul>")

    parts.append("<h2>Recompensas / Consecuencias</h2>")
    parts.append(_p(enc.rewards))

    parts.append("<h2>Beats (Inicio / Medio / Final)</h2>")
    parts.append("<ul>" + "".join([f"<li>{escape(b)}</li>" for b in enc.beats]) + "</ul>")

    if enc.tags:
        parts.append("<hr>")
        parts.append(f"<p><strong>Tags:</strong> {escape(', '.join(enc.tags))}</p>")

    return "\n".join([p for p in parts if p])


def foundry_journal_entry(enc: Encounter) -> dict[str, Any]:
    html = encounter_to_html(enc)
    return {
        "name": enc.title,
        "pages": [
            {
                "name": "Encuentro",
                "type": "text",
                "text": {
                    "format": 1,
                    "content": html,
                },
            }
        ],
    }


def roll20_handout_text(enc: Encounter) -> str:
    return enc.to_markdown()
