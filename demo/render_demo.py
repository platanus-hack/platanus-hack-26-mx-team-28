"""Renderiza el demo visual de Dominikito: cuento + preguntas como botones, estilo de `branding.md`.

Toma un Story y sus Dilemas (por defecto, los fixtures de eval/) y produce un HTML autocontenido que
se abre en el navegador. Las ilustraciones son placeholders (Nano Banana llega después).

Uso:
    python demo/render_demo.py            # usa fixtures, escribe demo/dominikito_demo.html
"""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "backend" / "eval" / "fixtures"
OUT = Path(__file__).resolve().parent / "dominikito_demo.html"

OPT_COLORS = ["blue", "orange", "green", "purple", "red"]
ILLUS_EMOJI = ["🚀", "🐵", "🪐", "⭐", "🌈", "🦕"]

CSS = """
:root{
  --cream:#F5F0E1; --cream2:#FBF8EF; --ink:#21364F;
  --blue:#3FA7DC; --blue-deep:#2D6CB6; --orange:#F4A12E; --yellow:#FBC740;
  --green:#74BE44; --red:#E23A2E; --purple:#9A45B8;
}
*{box-sizing:border-box}
body{
  margin:0; background:var(--cream); color:var(--ink);
  font-family:'Nunito',system-ui,sans-serif; font-weight:700;
  background-image:radial-gradient(rgba(33,54,79,.05) 1px,transparent 1px);
  background-size:14px 14px;
}
.wrap{max-width:680px;margin:0 auto;padding:24px 18px 80px}
header{text-align:center;margin:18px 0 26px}
.wordmark{font-family:'Baloo 2',cursive;font-weight:800;font-size:54px;line-height:1;letter-spacing:.5px}
.wordmark .b{color:var(--blue-deep)} .wordmark .o{color:var(--orange)}
.wordmark .g{color:var(--green)} .wordmark .p{color:var(--purple)} .wordmark .y{color:var(--yellow)}
.sub{margin-top:6px;color:var(--blue-deep);font-weight:800;opacity:.8}
.page{
  background:var(--cream2); border:3px solid var(--ink); border-radius:26px;
  padding:14px; margin:18px 0; box-shadow:0 8px 0 rgba(33,54,79,.12);
}
.illus{
  height:190px;border-radius:18px;border:2px solid var(--ink);
  background:linear-gradient(180deg,#bfe6fb,#e9f6ff);
  display:flex;align-items:center;justify-content:center;font-size:74px;position:relative;overflow:hidden;
}
.illus .star{position:absolute;color:#fff;opacity:.9;font-size:18px}
.illus .tag{position:absolute;bottom:8px;right:10px;font-size:11px;color:var(--blue-deep);
  background:rgba(255,255,255,.7);padding:2px 8px;border-radius:10px}
.story-text{font-size:21px;line-height:1.5;margin:14px 6px 6px}
.dilemma{margin:10px 4px 4px;border-top:2px dashed rgba(33,54,79,.25);padding-top:12px}
.prompt{font-family:'Baloo 2',cursive;font-size:23px;color:var(--blue-deep);margin:4px 0 12px}
.options{display:flex;flex-direction:column;gap:12px}
.opt{
  display:flex;align-items:center;gap:12px;text-align:left;cursor:pointer;
  font-family:'Nunito',sans-serif;font-weight:800;font-size:18px;color:var(--ink);
  border:3px solid var(--ink);border-radius:18px;padding:12px 14px;background:#fff;
  box-shadow:0 5px 0 rgba(33,54,79,.18);transition:transform .07s,box-shadow .07s;
}
.opt:hover{transform:translateY(-2px)} .opt:active{transform:translateY(2px);box-shadow:0 2px 0 rgba(33,54,79,.18)}
.opt .bul{flex:0 0 34px;height:34px;border-radius:50%;display:flex;align-items:center;justify-content:center;
  color:#fff;font-family:'Baloo 2',cursive;font-size:18px}
.opt-blue .bul{background:var(--blue)} .opt-orange .bul{background:var(--orange)}
.opt-green .bul{background:var(--green)} .opt-purple .bul{background:var(--purple)} .opt-red .bul{background:var(--red)}
.opt.sel{background:var(--yellow);box-shadow:0 2px 0 rgba(33,54,79,.3)}
.pole-tag{display:none;margin-left:auto;font-size:12px;background:var(--ink);color:#fff;padding:3px 8px;border-radius:10px}
body.dev .pole-tag{display:inline-block}
.devbar{position:fixed;top:12px;right:12px;z-index:10}
.devbar button{font-family:'Nunito';font-weight:800;border:2px solid var(--ink);background:#fff;
  border-radius:14px;padding:8px 12px;cursor:pointer}
.devlog{position:fixed;bottom:0;left:0;right:0;background:var(--ink);color:#cfe;display:none;
  font-family:ui-monospace,monospace;font-size:13px;padding:10px 14px;max-height:30vh;overflow:auto}
body.dev .devlog{display:block}
.note{text-align:center;color:var(--blue-deep);opacity:.7;font-size:13px;margin-top:6px}
"""

JS = """
function choose(btn){
  const group = btn.closest('.options');
  group.querySelectorAll('.opt').forEach(b=>b.classList.remove('sel'));
  btn.classList.add('sel');
  const log = document.getElementById('devlog');
  const line = document.createElement('div');
  line.textContent = '→ ['+btn.dataset.dim+'] eligió: \"'+btn.dataset.txt+'\"  ⇒  polo='+btn.dataset.pole;
  log.appendChild(line);
}
function toggleDev(){ document.body.classList.toggle('dev'); }
"""


def _stars(n: int) -> str:
    pos = [(12, 18), (80, 30), (30, 70), (88, 78), (55, 12), (68, 60)]
    return "".join(
        f'<span class="star" style="left:{x}%;top:{y}%">{"✦" if i % 2 else "✧"}</span>'
        for i, (x, y) in enumerate(pos[:n])
    )


def _wordmark() -> str:
    # D o m i n i k i t o  con colores de marca
    classes = ["b", "o", "b", "g", "o", "b", "p", "p", "p", "p"]
    letters = "Dominikito"
    return "".join(f'<span class="{c}">{ch}</span>' for ch, c in zip(letters, classes))


def render(story: dict, dilemmas: list[dict]) -> str:
    by_page = {d["page"]: d for d in dilemmas}
    parts: list[str] = []
    for i, page in enumerate(story["pages"]):
        emoji = ILLUS_EMOJI[i % len(ILLUS_EMOJI)]
        parts.append('<section class="page">')
        parts.append(f'<div class="illus">{_stars(5)}<span>{emoji}</span>'
                     f'<span class="tag">ilustración: Nano Banana · próximamente</span></div>')
        parts.append(f'<p class="story-text">{html.escape(page["text"])}</p>')
        d = by_page.get(page["page"]) if page.get("is_checkpoint") else None
        if d:
            parts.append('<div class="dilemma">')
            parts.append(f'<p class="prompt">{html.escape(d["prompt"])}</p>')
            parts.append('<div class="options">')
            for j, opt in enumerate(d["options"]):
                color = OPT_COLORS[j % len(OPT_COLORS)]
                parts.append(
                    f'<button class="opt opt-{color}" data-dim="{html.escape(d["primary_dimension"])}" '
                    f'data-pole="{html.escape(opt["pole"])}" data-txt="{html.escape(opt["text"])}" '
                    f'onclick="choose(this)">'
                    f'<span class="bul">{html.escape(opt["id"])}</span>'
                    f'<span>{html.escape(opt["text"])}</span>'
                    f'<span class="pole-tag">{html.escape(opt["pole"])}</span></button>'
                )
            parts.append('</div></div>')
        parts.append('</section>')

    body = "\n".join(parts)
    title = html.escape(story.get("title", "Cuento"))
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Dominikito · {title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;800&family=Nunito:wght@600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body>
<div class="devbar"><button onclick="toggleDev()">\U0001f441️ modo papás</button></div>
<div class="wrap">
  <header><div class="wordmark">{_wordmark()}</div>
  <div class="sub">{title}</div>
  <div class="note">Demo · las preguntas son del Agente 2 (mapeo de polos visible en “modo papás”)</div></header>
  {body}
</div>
<div class="devlog" id="devlog"><b>Modo papás · registro de decisiones (no visible para el niño)</b></div>
<script>{JS}</script>
</body></html>"""


def main() -> None:
    story = json.loads((FIXTURES / "story_dino.json").read_text(encoding="utf-8"))
    dilemmas = json.loads((FIXTURES / "dilemmas_dino.json").read_text(encoding="utf-8"))["dilemmas"]
    OUT.write_text(render(story, dilemmas), encoding="utf-8")
    print(f"OK: {OUT}")


if __name__ == "__main__":
    main()
