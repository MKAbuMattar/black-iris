#!/usr/bin/env python3
"""Generate the README SVG set: hero and section headers in en, es, ar, each
in light and dark, plus the logo. One source of truth for palette and copy.

Run: python3 .github/assets/readme/build.py
"""
import json
from pathlib import Path

# Every color comes from the Jordanian Identity Colors sheet beside this folder.
PALETTE = {c["key"]: c for c in json.loads((Path(__file__).parent.parent / "jordan-identity-colors.json").read_text())["colors"]}
def C(key): return PALETTE[key]["hex"]

IRIS = C("black-iris")        # structure: headings and keylines by day, the whole ground by night
PLATE = C("salt-white")       # the day ground, Dead Sea salt
GOLD = C("wadi-rum-sand")     # the beard of the flower, used once per asset

THEMES = {
    "light": dict(bg=PLATE, fg=IRIS, muted=C("basalt-black"), line=IRIS),
    "dark":  dict(bg=IRIS,  fg=PLATE, muted=C("amman-stone"), line=PLATE),
}

# Order of the ten swatches in the identity strip, as the sheet lists them.
STRIP = ["wadi-rum-sand", "dead-sea-blue", "black-iris", "olive-green", "keffiyeh-red",
         "petra-rose", "desert-camel", "amman-stone", "salt-white", "basalt-black"]

# One palette tone per mode family, used only as a small marker beside each row.
MODE_TONE = {
    "Shape": "black-iris", "Build": "black-iris", "Deslop": "petra-rose",
    "Gates": "keffiyeh-red", "Ideate": "dead-sea-blue", "Prompt": "olive-green",
    "Memory": "desert-camel", "Ship": "amman-stone", "Name": "amman-stone",
    "Review": "amman-stone", "Diagram": "wadi-rum-sand",
}
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', 'Noto Naskh Arabic', sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, monospace"

MODES = [
    ("Shape", "always on"), ("Build", "always on"), ("Deslop", "humanize"),
    ("Gates", "do not stop until done"), ("Ideate", "brainstorm"),
    ("Prompt", "write a prompt for"), ("Memory", "autodream"),
    ("Ship", "commit message"), ("Name", "rename"), ("Review", "review this diff"),
    ("Diagram", "diagram this"),
]

LANGS = {
    "en": dict(
        eyebrow="AGENT SKILL FOR CLAUDE CODE, CODEX, AND FRIENDS",
        promise1="One skill, twelve disciplines for a coding agent.",
        promise2="Answer first. Exact numbers. Warnings kept. Done means checked.",
        promise3="", rtl=False,
        table="ROUTING TABLE", table_sub="say it, get the mode",
        desc="One Claude Code skill with twelve disciplines for a coding agent. The routing table of modes is shown beside the name.",
        sections=[("01", "install", "Install", "one command per agent"),
                  ("02", "use", "Use", "say the trigger, get the mode"),
                  ("03", "store", "Where it writes", "~/.BLACK_IRIS_AGENTS, never your repo"),
                  ("04", "repo", "Repo", "skill, hook, manifests")],
    ),
    "es": dict(
        eyebrow="HABILIDAD DE AGENTE PARA CLAUDE CODE, CODEX Y MAS",
        promise1="Una habilidad, doce disciplinas para un agente de programacion.",
        promise2="Respuesta primero. Numeros exactos. Avisos intactos.",
        promise3="Hecho significa comprobado.", rtl=False,
        table="TABLA DE MODOS", table_sub="dilo, activa el modo",
        desc="Una habilidad de Claude Code con doce disciplinas para un agente de programacion. La tabla de modos aparece junto al nombre.",
        sections=[("01", "install", "Instalacion", "un comando por agente"),
                  ("02", "use", "Uso", "di el disparador, activa el modo"),
                  ("03", "store", "Donde escribe", "~/.BLACK_IRIS_AGENTS, nunca tu repo"),
                  ("04", "repo", "Repositorio", "habilidad, hook, manifiestos")],
    ),
    "ar": dict(
        eyebrow="مهارة وكيل لـ Claude Code وCodex وغيرهما",
        promise1="مهارة واحدة، اثنتا عشرة قاعدة عمل لوكيل البرمجة.",
        promise2="الجواب أولاً. أرقام دقيقة. التحذيرات باقية. المنجَز هو المُتحقَّق منه.",
        promise3="", rtl=True,
        table="جدول الأنماط", table_sub="قلها، يعمل النمط",
        desc="مهارة واحدة لـ Claude Code باثنتي عشرة قاعدة عمل لوكيل البرمجة. جدول الأنماط بجانب الاسم.",
        sections=[("01", "install", "التثبيت", "أمر واحد لكل وكيل"),
                  ("02", "use", "الاستخدام", "قل المحفّز، يعمل النمط"),
                  ("03", "store", "أين تكتب", "~/.BLACK_IRIS_AGENTS، لا مستودعك"),
                  ("04", "repo", "المستودع", "مهارة، خطاف، ملفات تعريف")],
    ),
}


def iris_mark(x, y, fill, scale=1.0):
    """Three standards up, three falls down, one gold beard. About 44 units tall at scale 1."""
    std = "M0,0 C-5,-8 -5,-18 0,-26 C5,-18 5,-8 0,0Z"
    fall = "M0,0 C-3,7 -9,12 -15,19 C-8,17 -3,13 0,8 C3,13 8,17 15,19 C9,12 3,7 0,0Z"
    parts = [f'<path d="{std}" transform="rotate({r})"/>' for r in (-32, 0, 32)]
    parts += [f'<path d="{fall}" transform="rotate({r})"/>' for r in (-20, 0, 20)]
    return (f'<g transform="translate({x} {y}) scale({scale})" fill="{fill}">' + "".join(parts) +
            f'<circle cx="0" cy="2" r="2.2" fill="{GOLD}"/></g>')


def hero(t, L):
    rtl = L["rtl"]
    # Arabic joins break under monospace tracking, so Arabic UI text uses the sans stack
    # with no letter-spacing and is anchored to the right edge of its block.
    ui_font = SANS if rtl else MONO
    ls = "" if rtl else ' letter-spacing="2"'
    ax = 'x="620" text-anchor="end"' if rtl else 'x="0"'
    table_ls = "" if rtl else ' letter-spacing="1.5"'
    p3 = f'<text {ax} y="248" font-family="{SANS}" font-size="20" fill="{t["fg"]}">{L["promise3"]}</text>' if L["promise3"] else ""
    strip = "".join(f'<rect x="{i * 24}" y="0" width="20" height="14" rx="2" fill="{C(k)}"'
                    + (f' stroke="{t["line"]}" stroke-width="1"' if C(k) == t["bg"] else "") + "/>"
                    for i, k in enumerate(STRIP))
    rows = []
    for i, (mode, trig) in enumerate(MODES):
        y = 74 + i * 22
        weight = "700" if i < 2 else "500"
        tone = C(MODE_TONE[mode])
        if tone == t["bg"]:
            tone = t["fg"]
        rows.append(f'<rect x="24" y="{y - 11}" width="10" height="10" rx="2" fill="{tone}"/>')
        rows.append(f'<text x="44" y="{y}" font-family="{SANS}" font-size="16" font-weight="{weight}" fill="{t["fg"]}">{mode}</text>')
        rows.append(f'<text x="160" y="{y}" font-family="{MONO}" font-size="14" fill="{t["muted"]}">{trig}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="400" viewBox="0 0 1200 400" role="img" aria-labelledby="title desc">
  <title id="title">black-iris</title>
  <desc id="desc">{L["desc"]}</desc>
  <rect width="1200" height="400" rx="24" fill="{t["bg"]}"/>
  <rect x="56" y="48" width="1088" height="3" fill="{t["line"]}"/>
  <g id="identity-strip" transform="translate(56 26)">{strip}</g>
  {iris_mark(72, 92, t["fg"], 1.0)}
  <g id="title-block" transform="translate(112 64)">
    <text {ax} y="16" font-family="{ui_font}" font-size="14"{ls} fill="{t["muted"]}">{L["eyebrow"]}</text>
    <text x="0" y="92" font-family="{SANS}" font-size="72" font-weight="800" letter-spacing="-2" fill="{t["fg"]}">black-iris</text>
    <text x="0" y="132" font-family="{SANS}" font-size="30" fill="{t["muted"]}">السوسنة السوداء</text>
    <text {ax} y="192" font-family="{SANS}" font-size="20" fill="{t["fg"]}">{L["promise1"]}</text>
    <text {ax} y="220" font-family="{SANS}" font-size="20" fill="{t["fg"]}">{L["promise2"]}</text>
    {p3}
    <text x="0" y="292" xml:space="preserve" font-family="{MONO}" font-size="14" fill="{t["muted"]}">{IRIS}    Jordanian Identity Colors    GPL-2.0-only    /black-iris</text>
  </g>
  <g id="project-proof" transform="translate(760 40)">
    <rect x="0" y="0" width="384" height="316" rx="14" fill="{t["bg"]}" stroke="{t["line"]}" stroke-width="2"/>
    <rect x="0" y="0" width="384" height="40" rx="14" fill="{t["line"]}"/>
    <rect x="0" y="26" width="384" height="14" fill="{t["line"]}"/>
    <text x="24" y="26" font-family="{ui_font}" font-size="14"{table_ls} fill="{t["bg"]}">{L["table"]}</text>
    <text x="360" y="26" text-anchor="end" font-family="{ui_font}" font-size="13" fill="{t["bg"]}">{L["table_sub"]}</text>
    {"".join(rows)}
  </g>
</svg>
'''


def section(t, num, title, sub, rtl=False):
    sub_font = SANS if rtl else MONO
    ls = "" if rtl else ' letter-spacing="2"'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="120" viewBox="0 0 1200 120" role="img" aria-labelledby="title desc">
  <title id="title">{title}</title>
  <desc id="desc">{title}. {sub}</desc>
  <rect width="1200" height="120" rx="18" fill="{t["bg"]}"/>
  <rect x="48" y="30" width="1104" height="3" fill="{t["line"]}"/>
  {iris_mark(62, 68, t["fg"], 0.72)}
  <text x="96" y="86" font-family="{SANS}" font-size="40" font-weight="800" letter-spacing="-1" fill="{t["fg"]}">{title}</text>
  <text x="1152" y="86" xml:space="preserve" text-anchor="end" font-family="{sub_font}" font-size="16"{ls} fill="{t["muted"]}">{num}    {sub}</text>
</svg>
'''


def logo(t):
    """256 square: the iris mark alone, large, on the ground of its theme."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256" role="img" aria-labelledby="title desc">
  <title id="title">black-iris logo</title>
  <desc id="desc">A geometric black iris, three standards up and three falls down, with a Wadi Rum sand beard, on the Jordanian identity palette.</desc>
  <rect width="256" height="256" rx="56" fill="{t["bg"]}"/>
  {iris_mark(128, 150, t["fg"], 4.6)}
</svg>
'''


def logo_mark():
    """Transparent mark in the iris color, for favicons and light surfaces."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 128 128" role="img" aria-labelledby="title">
  <title id="title">black-iris mark</title>
  {iris_mark(64, 78, IRIS, 2.4)}
</svg>
'''


if __name__ == "__main__":
    out = Path(__file__).parent
    n = 0
    for theme, t in THEMES.items():
        (out / f"logo-{theme}.svg").write_text(logo(t)); n += 1
        for lang, L in LANGS.items():
            (out / f"hero-{lang}-{theme}.svg").write_text(hero(t, L)); n += 1
            for num, slug, title, sub in L["sections"]:
                (out / f"section-{slug}-{lang}-{theme}.svg").write_text(section(t, num, title, sub, L["rtl"])); n += 1
    (out / "logo-mark.svg").write_text(logo_mark()); n += 1
    # The skill carries its own copy so metadata.logo resolves after any cp -R install.
    skill_assets = out.parent.parent.parent / "skills" / "black-iris" / "assets"
    skill_assets.mkdir(exist_ok=True)
    (skill_assets / "logo.svg").write_text(logo_mark()); n += 1
    print("wrote", n, "svgs")
    # logo.png for manifests that need a raster. Regenerated here, never hand-edited.
    import shutil, subprocess
    if shutil.which("rsvg-convert"):
        subprocess.run(["rsvg-convert", "-w", "512", "-h", "512", str(out / "logo-dark.svg"), "-o", str(out / "logo.png")], check=True)
        print("wrote logo.png")
    else:
        print("rsvg-convert not found; logo.png left as is")
