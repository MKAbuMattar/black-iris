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
    "Gates": "keffiyeh-red", "Ideate": "olive-green", "Prompt": "wadi-rum-sand",
    "Memory": "desert-camel", "Council": "dead-sea-blue", "Jerash": "amman-stone", "Siq": "petra-rose", "Context": "basalt-black", "Ship": "amman-stone", "Name": "amman-stone",
    "Review": "amman-stone", "Diagram": "wadi-rum-sand",
}
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', 'Noto Naskh Arabic', sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, monospace"

MODES = [
    ("Shape", "always on"), ("Build", "always on"), ("Deslop", "humanize"),
    ("Gates", "do not stop until done"), ("Ideate", "brainstorm"),
    ("Prompt", "write a prompt for"), ("Council", "council this"), ("Memory", "autodream"),
    ("Context", "analyze this log"), ("Jerash", "race this"), ("Siq", "handoff"),
    ("Ship", "commit message"), ("Name", "rename"), ("Review", "review this diff"),
    ("Diagram", "diagram this"),
]

LANGS = {
    "en": dict(
        eyebrow="AGENT SKILL FOR CLAUDE CODE, CODEX, AND FRIENDS",
        promise1="One skill, fifteen disciplines for a coding agent.",
        promise2="Answer first. Exact numbers. Warnings kept. Done means checked.",
        promise3="", rtl=False,
        table="ROUTING TABLE", table_sub="say it, get the mode",
        desc="One Claude Code skill with fifteen disciplines for a coding agent. The routing table of modes is shown beside the name.",
        sections=[("01", "install", "Install", "one command per agent"),
                  ("02", "use", "Use", "say the trigger, get the mode"),
                  ("03", "store", "Where it writes", "~/.BLACK_IRIS_AGENTS, never your repo"),
                  ("04", "repo", "Repo", "skill, hook, manifests")],
    ),
    "es": dict(
        eyebrow="HABILIDAD DE AGENTE PARA CLAUDE CODE, CODEX Y MAS",
        promise1="Una habilidad, quince disciplinas para un agente de programacion.",
        promise2="Respuesta primero. Numeros exactos. Avisos intactos.",
        promise3="Hecho significa comprobado.", rtl=False,
        table="TABLA DE MODOS", table_sub="dilo, activa el modo",
        desc="Una habilidad de Claude Code con quince disciplinas para un agente de programacion. La tabla de modos aparece junto al nombre.",
        sections=[("01", "install", "Instalacion", "un comando por agente"),
                  ("02", "use", "Uso", "di el disparador, activa el modo"),
                  ("03", "store", "Donde escribe", "~/.BLACK_IRIS_AGENTS, nunca tu repo"),
                  ("04", "repo", "Repositorio", "habilidad, hook, manifiestos")],
    ),
    "ar": dict(
        eyebrow="مهارة وكيل لـ Claude Code وCodex وغيرهما",
        promise1="مهارة واحدة، خمس عشرة قاعدة عمل لوكيل البرمجة.",
        promise2="الجواب أولاً. أرقام دقيقة. التحذيرات باقية. المنجَز هو المُتحقَّق منه.",
        promise3="", rtl=True,
        table="جدول الأنماط", table_sub="قلها، يعمل النمط",
        desc="مهارة واحدة لـ Claude Code بخمس عشرة قاعدة عمل لوكيل البرمجة. جدول الأنماط بجانب الاسم.",
        sections=[("01", "install", "التثبيت", "أمر واحد لكل وكيل"),
                  ("02", "use", "الاستخدام", "قل المحفّز، يعمل النمط"),
                  ("03", "store", "أين تكتب", "~/.BLACK_IRIS_AGENTS، لا مستودعك"),
                  ("04", "repo", "المستودع", "مهارة، خطاف، ملفات تعريف")],
    ),
}



# ---------------------------------------------------------------------------
# Marks. One primitive: the petal lens, two circular arcs of equal radius
# between a base point and a tip. The master iris and every mode glyph are
# built from it on a 256 canvas, drawn in G_INK with G_PAPER for cut-outs, and
# recoloured on output. Designed with the logo-design skill: black first, then
# the Jordanian palette; audited at 99 to 100 on every glyph.
import math
G_INK, G_PAPER = "#111111", "#FFFFFF"

def pt(cx, cy, ang, dist):
    a = math.radians(ang)            # 0 = up, clockwise positive
    return (round(cx + dist * math.sin(a), 2), round(cy - dist * math.cos(a), 2))

def lens(base, ang, length, r, fill=G_INK):
    """Petal from `base` pointing at `ang`, `length` long, arcs of radius r."""
    tip = pt(base[0], base[1], ang, length)
    b = f"{base[0]} {base[1]}"; t = f"{tip[0]} {tip[1]}"
    return f'<path fill="{fill}" d="M{b} A{r} {r} 0 0 1 {t} A{r} {r} 0 0 1 {b} Z"/>'

G_C = (128, 140)
# --- Concept A: six lenses. Slender standards up, fuller falls down, a beard hole at the heart.
def master_a(fill=G_INK, hole=G_PAPER):
    s = [lens(G_C, a, 100, 66, fill) for a in (-36, 0, 36)]
    f = [lens(G_C, a, 78, 44, fill) for a in (124, 180, 236)]
    return "".join(s + f) + f'<circle cx="{G_C[0]}" cy="{G_C[1]}" r="9" fill="{hole}"/>'

# --- Concept A family: every mode glyph from the same lens, one idea each.
P = (128, 128)
def mode(name):
    if name == "deslop":   # the petal with its tip cut off flat; the removed tip floats away
        return (f'<path fill="{G_INK}" d="M112 224 A118 118 0 0 1 75.08 112 L148.92 112 A118 118 0 0 1 112 224 Z"/>'
                + lens((172, 84), 30, 64, 44))
    if name == "gates":    # a petal passing between two posts
        return (f'<rect x="40" y="48" width="28" height="168" rx="6" fill="{G_INK}"/>'
                f'<rect x="188" y="48" width="28" height="168" rx="6" fill="{G_INK}"/>' + lens((128, 208), 0, 152, 100))
    if name == "ideate":   # five slim petals diverging from one point, gaps between, unequal reach
        return "".join(lens((128, 220), a, l, 1.05 * l) for a, l in ((-64, 132), (-32, 168), (0, 188), (32, 168), (64, 132)))
    if name == "council":  # five advisors facing a chairman
        return "".join(lens(pt(128, 132, a, 116), a + 180, 84, 56) for a in (0, 72, 144, 216, 288)) + f'<circle cx="128" cy="132" r="22" fill="{G_INK}"/>'
    if name == "prompt":   # a petal lying on its side, then a caret
        return lens((40, 128), 90, 132, 86) + f'<rect x="188" y="64" width="28" height="128" rx="6" fill="{G_INK}"/>'
    if name == "memory":   # three slim petals laid down as strata, clear gaps
        return "".join(lens((32, y), 90, 192, 220) for y in (64, 128, 192))
    if name == "context":  # bulk above, the derived answer below
        return lens((24, 84), 90, 208, 136) + lens((88, 196), 90, 80, 52)
    if name == "ship":     # a petal as a sail on a hull
        return lens((140, 188), -8, 156, 104) + f'<rect x="40" y="196" width="176" height="28" rx="14" fill="{G_INK}"/>'
    if name == "name":     # a petal tag with its hole
        return lens((56, 200), 45, 200, 130) + f'<circle cx="158" cy="98" r="16" fill="{G_PAPER}"/>'
    if name == "jerash":   # the hippodrome track, one petal holding the lane
        track = (f'<path fill="{G_INK}" d="M40 220 V116 A88 88 0 0 1 216 116 V220 H184 V116 '
                 f'A56 56 0 0 0 72 116 V220 Z"/>')
        return track + lens((128, 212), 0, 124, 84)
    if name == "siq":      # the gorge: two leaning walls, one petal rising through the gap
        walls = (f'<path fill="{G_INK}" d="M32 224 L32 70 L84 40 L100 100 L100 224 Z"/>'
                 f'<path fill="{G_INK}" d="M224 224 L224 70 L172 40 L156 100 L156 224 Z"/>')
        return walls + lens((128, 224), 0, 200, 260)
    if name == "review":   # the petal as an eye, a pupil held open
        return lens((24, 128), 90, 208, 150) + f'<circle cx="128" cy="128" r="34" fill="{G_PAPER}"/><circle cx="128" cy="128" r="16" fill="{G_INK}"/>'
    raise KeyError(name)

# Measured bounding boxes from the logo-design audit: centre offset from 128
# (dx, dy with the optical raise already folded in) and width, height.
GLYPH_BOX = {"siq": [0.0, -4.0, 192, 200], "jerash": [0.0, -1.0, 176, 192], 'symbol': [0.0, -6.0, 130, 178], 'context': [0.0, -2.2, 208, 179], 'council': [0.0, 2.1, 221, 210], 'deslop': [-11.2, -3.3, 133, 195], 'gates': [0.0, -9.0, 176, 168], 'ideate': [0.0, -3.1, 237, 188], 'memory': [0.0, -5.0, 192, 172], 'name': [1.3, -6.3, 142, 142], 'prompt': [0.0, -5.0, 176, 128], 'review': [0.0, -5.0, 208, 84], 'ship': [0.0, -5.8, 176, 190]}


def glyph(key, ink, paper):
    body = master_a() if key == "symbol" else mode(key)
    return body.replace(G_INK, ink).replace(G_PAPER, paper)


def placed(key, ink, paper, cx, cy, size):
    """The glyph with its longest side `size` units, optically centred on (cx, cy)."""
    dx, dy, w, h = GLYPH_BOX[key]
    gx, gy = 128 - dx, 128 - (dy + 5)
    s = size / max(w, h)
    return (f'<g transform="translate({cx} {cy}) scale({s:.4f}) translate({-gx} {-gy})">'
            f'{glyph(key, ink, paper)}</g>')

def iris_mark(x, y, fill, scale=1.0):
    """The master iris, about 44 units tall at scale 1, centred on (x, y), with a
    Wadi Rum Sand beard. Same signature the hero and section headers always used."""
    return placed("symbol", fill, GOLD, x, y, 44 * scale)


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
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="468" viewBox="0 0 1200 468" role="img" aria-labelledby="title desc">
  <title id="title">black-iris</title>
  <desc id="desc">{L["desc"]}</desc>
  <rect width="1200" height="468" rx="24" fill="{t["bg"]}"/>
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
    <rect x="0" y="0" width="384" height="408" rx="14" fill="{t["bg"]}" stroke="{t["line"]}" stroke-width="2"/>
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
  <desc id="desc">A black iris built from one petal lens: three slender standards up, three fuller falls down, a Wadi Rum Sand beard.</desc>
  <rect width="256" height="256" rx="56" fill="{t["bg"]}"/>
  {placed("symbol", t["fg"], GOLD, 128, 123, 176)}
</svg>
'''


MODE_KEYS = {"Deslop": "deslop", "Gates": "gates", "Ideate": "ideate", "Prompt": "prompt",
             "Council": "council", "Memory": "memory", "Context": "context", "Ship": "ship",
             "Name": "name", "Review": "review", "Jerash": "jerash", "Siq": "siq"}


def lum(h):
    r, g, b = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def mode_icon(title, key):
    """A mode's icon: its glyph on a tile in the mode's palette tone. The glyph takes
    Salt White or Black Iris, whichever contrasts more with the tile."""
    ground = C(MODE_TONE[title])
    ink = max((PLATE, IRIS), key=lambda c: contrast(c, ground))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256" role="img" aria-labelledby="title">
  <title id="title">black-iris {key}</title>
  <rect width="256" height="256" rx="56" fill="{ground}"/>
  {placed(key, ink, ground, 128, 123, 160)}
</svg>
'''


def logo_mark():
    """Transparent mark in the iris color, for favicons and light surfaces."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 128 128" role="img" aria-labelledby="title">
  <title id="title">black-iris mark</title>
  {placed("symbol", IRIS, GOLD, 64, 62, 116)}
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
    # One icon per mode command; each skills/black-iris-<mode>/SKILL.md points here.
    (skill_assets / "modes").mkdir(exist_ok=True)
    for title, key in MODE_KEYS.items():
        (skill_assets / "modes" / f"{key}.svg").write_text(mode_icon(title, key)); n += 1
    print("wrote", n, "svgs")
    # logo.png for manifests that need a raster. Regenerated here, never hand-edited.
    import shutil, subprocess
    if shutil.which("rsvg-convert"):
        subprocess.run(["rsvg-convert", "-w", "512", "-h", "512", str(out / "logo-dark.svg"), "-o", str(out / "logo.png")], check=True)
        print("wrote logo.png")
    else:
        print("rsvg-convert not found; logo.png left as is")
