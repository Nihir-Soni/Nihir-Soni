# Generates the SVG assets for the profile README.
import os
OUT = "/home/claude/profile/assets"

SERIF = "'Iowan Old Style','Palatino Linotype',Palatino,'Book Antiqua',Georgia,serif"
SANS = "-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"

INK, TEAL, CYAN, CYAN_L = "#0F172A", "#164E63", "#22D3EE", "#A5F3FC"
BONE, SLATE = "#E8EEF2", "#94A3B8"
SEPIA, SEPIA_D = "#C9A36A", "#17120D"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(w, h, body, title, desc=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-labelledby="t d"><title id="t">{esc(title)}</title><desc id="d">{esc(desc)}</desc>{body}</svg>')


def chip(x, y, text, h=26, fs=13):
    w = round(len(text) * (fs * 0.56) + 22)
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="{CYAN}" fill-opacity=".09" '
            f'stroke="{CYAN}" stroke-opacity=".35"/>'
            f'<text x="{x + w/2}" y="{y + h/2 + fs*0.35}" text-anchor="middle" font-family="{SANS}" '
            f'font-size="{fs}" fill="{BONE}">{esc(text)}</text>'), w


# ---------- the photograph (shared motif: damaged scan vs restored) ----------
def defs_photo(p):
    return f'''
<linearGradient id="{p}skyC" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0B3A52"/><stop offset="1" stop-color="#67E8F9"/></linearGradient>
<linearGradient id="{p}skyD" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7A6446"/><stop offset="1" stop-color="#E2CFA6"/></linearGradient>
<radialGradient id="{p}stain"><stop offset="0" stop-color="#5a3b1a" stop-opacity=".6"/><stop offset="1" stop-color="#5a3b1a" stop-opacity="0"/></radialGradient>
<filter id="{p}grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="7"/>
<feColorMatrix type="matrix" values="0 0 0 0 .95  0 0 0 0 .85  0 0 0 0 .65  1.7 0 0 0 -.7"/></filter>
<filter id="{p}wob" x="-5%" y="-20%" width="110%" height="140%"><feTurbulence type="fractalNoise" baseFrequency=".05 .8" numOctaves="2" seed="4" result="n"/>
<feDisplacementMap in="SourceGraphic" in2="n" scale="5"/></filter>
<filter id="{p}blur" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="7"/></filter>'''


def scene(p, clean):
    """232 x 206 picture: a clock tower at dusk."""
    c = dict(sky=f"url(#{p}skyC)", sun="#E0FBFF", far="#0E4A63", near="#0A2740", tower="#0A1F33",
             lit="#164E63", face="#E0FBFF", hand="#0A1F33", ground="#07182B") if clean else \
        dict(sky=f"url(#{p}skyD)", sun="#F3E7C8", far="#5E4C35", near="#3B2F21", tower="#2B2118",
             lit="#4a3a28", face="#EBDDBA", hand="#2B2118", ground="#241C14")
    s = f'''<rect width="232" height="206" fill="{c['sky']}"/>
<circle cx="188" cy="48" r="16" fill="{c['sun']}" opacity=".9"/>
<path d="M0 140C40 110 80 130 120 118C160 106 200 124 232 112L232 206L0 206Z" fill="{c['far']}"/>
<rect x="98" y="44" width="36" height="110" fill="{c['tower']}"/>
<polygon points="94,44 116,16 138,44" fill="{c['tower']}"/>
<circle cx="116" cy="70" r="12" fill="{c['face']}"/>
<line x1="116" y1="70" x2="116" y2="62" stroke="{c['hand']}" stroke-width="1.8" stroke-linecap="round"/>
{'<line x1="116" y1="70" x2="123" y2="74" stroke="'+c['hand']+'" stroke-width="1.8" stroke-linecap="round"/>' if clean else ''}
<rect x="110" y="100" width="12" height="22" rx="6" fill="{c['lit']}"/>
<path d="M0 160C50 138 90 156 130 150C170 144 205 158 232 148L232 206L0 206Z" fill="{c['near']}"/>
<rect y="186" width="232" height="20" fill="{c['ground']}"/>'''
    if not clean:
        s += f'''
<circle cx="50" cy="150" r="64" fill="url(#{p}stain)"/><circle cx="205" cy="18" r="42" fill="url(#{p}stain)"/>
<path d="M40 0L44 206" stroke="#F6EBD0" stroke-width=".9" opacity=".55"/>
<path d="M168 0L165 124" stroke="#F6EBD0" stroke-width=".7" opacity=".5"/>
<path d="M206 58L208 206" stroke="#F6EBD0" stroke-width=".7" opacity=".35"/>
<path d="M0 118L232 111" stroke="#1b140c" stroke-width="1.3" opacity=".5"/>
<path d="M0 119.6L232 112.6" stroke="#F6EBD0" stroke-width=".8" opacity=".4"/>
<g fill="#F6EBD0" opacity=".7"><circle cx="24" cy="40" r="1.6"/><circle cx="78" cy="22" r="1.1"/><circle cx="150" cy="84" r="2"/><circle cx="190" cy="132" r="1.3"/><circle cx="62" cy="176" r="1.8"/><circle cx="214" cy="90" r="1.2"/></g>
<g fill="#1b140c" opacity=".6"><circle cx="34" cy="96" r="1.8"/><circle cx="132" cy="30" r="1.2"/><circle cx="176" cy="170" r="2.1"/><circle cx="96" cy="140" r="1.4"/></g>
<rect width="232" height="206" filter="url(#{p}grain)" opacity=".5"/>'''
    return s


def print_(p, clean, caption=True):
    paper, cap_fill, cap = ("#E8EEF2", "#0F172A", "restored") if clean else ("#D9C9A5", "#4a3b27", "damaged scan")
    torn = '' if clean else f'<polygon points="260,0 212,0 222,11 231,6 240,19 250,15 260,36" fill="{SEPIA_D}"/>'
    return f'''<rect x="6" y="9" width="260" height="270" rx="2" fill="#000" opacity=".4" filter="url(#{p}blur)"/>
<rect width="260" height="270" rx="2" fill="{paper}"/>
<g transform="translate(14 14)"><clipPath id="{p}img{int(clean)}"><rect width="232" height="206"/></clipPath>
<g clip-path="url(#{p}img{int(clean)})">{scene(p, clean)}</g></g>
{'<text x="130" y="248" text-anchor="middle" font-family="'+SERIF+'" font-style="italic" font-size="14" fill="'+cap_fill+'">'+cap+'</text>' if caption else ''}{torn}'''


# ---------- banner ----------
def banner():
    W, H = 1000, 340
    kt = 'keyTimes="0;.1;1" calcMode="spline" keySplines="0 0 1 1;.65 0 .25 1"'
    dur = "4.4s"

    def layer(clean):
        if clean:
            bg = (f'<rect width="{W}" height="{H}" fill="url(#bgC)"/><rect width="{W}" height="{H}" fill="url(#glowC)"/>')
            name_fill, tag_fill, filt = BONE, SLATE, ""
        else:
            bg = (f'<rect width="{W}" height="{H}" fill="{SEPIA_D}"/><rect width="{W}" height="{H}" fill="url(#glowD)"/>')
            name_fill, tag_fill, filt = SEPIA, "#8a7a5e", ' filter="url(#bwob)"'
        text = f'''<text x="52" y="172" font-family="{SERIF}" font-size="92" font-weight="500" letter-spacing="-2" fill="{name_fill}"{filt}>Nihir Soni</text>
<text font-family="{SANS}" font-size="21" fill="{tag_fill}"{filt}><tspan x="56" y="218">I build full-stack products and</tspan><tspan x="56" y="246">the machine learning inside them.</tspan></text>'''
        photo = f'<g transform="translate(698 28) rotate(3 130 135)">{print_("b", clean)}</g>'
        extra = f'<rect width="{W}" height="{H}" filter="url(#bgrain)" opacity=".35"/>' if not clean else ''
        return bg + text + photo + extra

    body = f'''<defs>
<linearGradient id="bgC" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{INK}"/><stop offset=".5" stop-color="{INK}"/><stop offset="1" stop-color="{TEAL}"/></linearGradient>
<radialGradient id="glowC" cx="830" cy="170" r="340" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{CYAN}" stop-opacity=".28"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
<radialGradient id="glowD" cx="830" cy="170" r="340" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#8a6a3a" stop-opacity=".25"/><stop offset="1" stop-color="#8a6a3a" stop-opacity="0"/></radialGradient>
<linearGradient id="beam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".35"/></linearGradient>
<filter id="bgrain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="11"/><feColorMatrix type="matrix" values="0 0 0 0 .95  0 0 0 0 .85  0 0 0 0 .65  1.7 0 0 0 -.7"/></filter>
<filter id="bwob" x="-5%" y="-20%" width="110%" height="140%"><feTurbulence type="fractalNoise" baseFrequency=".05 .8" numOctaves="2" seed="4" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="5"/></filter>
{defs_photo("b")}
<clipPath id="frame"><rect width="{W}" height="{H}" rx="20"/></clipPath>
<clipPath id="wipe"><rect x="0" y="0" width="{W}" height="{H}"><animate attributeName="width" values="0;0;{W}" {kt} dur="{dur}" begin="0s" fill="freeze"/></rect></clipPath>
</defs>
<g clip-path="url(#frame)">
<g>{layer(False)}</g>
<g clip-path="url(#wipe)">{layer(True)}</g>
<g transform="translate({W} 0)" opacity="0">
<animateTransform attributeName="transform" type="translate" values="-12 0;-12 0;{W} 0" {kt} dur="{dur}" begin="0s" fill="freeze"/>
<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.05;.93;1" dur="{dur}" begin="0s" fill="freeze"/>
<rect x="-70" width="70" height="{H}" fill="url(#beam)"/><rect x="-1.5" width="3" height="{H}" fill="{CYAN_L}"/></g>
</g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="20" fill="none" stroke="{CYAN}" stroke-opacity=".25"/>'''
    return svg(W, H, body, "Nihir Soni",
               "Banner: a damaged sepia scan of a clock tower photograph is restored to clean cyan as a scan line sweeps across.")


# ---------- stack ----------
def stack():
    W = 960
    layers = [
        ("Interface", "what people see", ["HTML", "CSS", "React", "Next.js", "Tailwind CSS"]),
        ("Server", "where the logic lives", ["Node.js", "Express", "Prisma"]),
        ("Data", "where it is kept", ["PostgreSQL", "MySQL", "MongoDB"]),
        ("Models", "where it learns", ["PyTorch", "TensorFlow", "OpenCV"]),
        ("Languages", "what it is written in", ["C++", "Python", "Java", "JavaScript", "TypeScript"]),
        ("Workflow", "how it ships", ["Git", "GitHub", "VS Code"]),
    ]
    LH, GAP, PAD = 56, 8, 24
    H = PAD * 2 + len(layers) * LH + (len(layers) - 1) * GAP
    b = f'''<defs><linearGradient id="spine" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN_L}"/><stop offset="1" stop-color="#0E7490"/></linearGradient></defs>
<rect width="{W}" height="{H}" rx="20" fill="{INK}"/><rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="20" fill="none" stroke="{TEAL}"/>
<rect x="24" y="{PAD}" width="4" height="{H-2*PAD}" rx="2" fill="url(#spine)"/>'''
    for i, (name, sub, items) in enumerate(layers):
        y = PAD + i * (LH + GAP)
        cy = y + LH / 2
        b += f'<rect x="40" y="{y}" width="{W-64}" height="{LH}" rx="12" fill="{CYAN}" fill-opacity="{0.07 - i*0.008:.3f}" stroke="{CYAN}" stroke-opacity=".16"/>'
        b += f'<circle cx="26" cy="{cy}" r="6" fill="{INK}" stroke="{CYAN}" stroke-width="2"/>'
        b += f'<text x="60" y="{cy-2}" font-family="{SERIF}" font-size="22" font-weight="500" fill="{BONE}">{name}</text>'
        b += f'<text x="60" y="{cy+16}" font-family="{SANS}" font-size="12.5" fill="{SLATE}">{sub}</text>'
        x = 270
        for it in items:
            c, w = chip(x, cy - 14, it, h=28, fs=14)
            b += c
            x += w + 10
    return svg(W, H, b, "Tech stack",
               "Layers from interface to models: React and Next.js; Node and Express; PostgreSQL, MySQL, MongoDB; PyTorch, TensorFlow, OpenCV; plus languages and tools.")


# ---------- project cards ----------
def card_frame(w, h):
    return (f'<rect width="{w}" height="{h}" rx="18" fill="{INK}"/>'
            f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="18" fill="none" stroke="{TEAL}"/>')


def wide_card():
    W, H = 880, 290
    b = f'<defs>{defs_photo("w")}<clipPath id="half"><rect x="0" y="0" width="116" height="270"/></clipPath><clipPath id="halfR"><rect x="116" y="0" width="144" height="270"/></clipPath>' \
        f'<linearGradient id="conf" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{SEPIA}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient></defs>'
    b += card_frame(W, H)
    b += f'<text x="40" y="84" font-family="{SERIF}" font-size="44" font-weight="500" letter-spacing="-.5" fill="{BONE}">TIMEKEEPER</text>'
    lines = ["Restores and colorizes damaged historical", "photographs, and calibrates how far to trust", "each result. Capstone project built with a team", "at Samsung Innovation Campus."]
    for i, l in enumerate(lines):
        b += f'<text x="40" y="{124 + i*24}" font-family="{SANS}" font-size="16" fill="{SLATE}">{l}</text>'
    x = 40
    for t in ["Computer vision", "Deep learning"]:
        c, w = chip(x, 226, t, h=28, fs=13.5)
        b += c
        x += w + 10
    b += f'<text x="40" y="272" font-family="{SANS}" font-size="12.5" fill="{SLATE}" opacity=".8">github.com/Nihir-Soni/TIMEKEEPER</text>'
    # split photograph
    b += f'<g transform="translate(540 10) scale(.9)"><g clip-path="url(#half)">{print_("w", False, caption=False)}</g><g clip-path="url(#halfR)">{print_("w", True, caption=False)}</g>' \
         f'<rect x="115" y="0" width="2" height="270" fill="{CYAN_L}"/><circle cx="116" cy="135" r="9" fill="{INK}" stroke="{CYAN_L}" stroke-width="2"/></g>'
    b += f'<rect x="540" y="262" width="234" height="6" rx="3" fill="url(#conf)"/>'
    b += f'<text x="540" y="284" font-family="{SANS}" font-size="12" fill="{SLATE}">less sure</text><text x="774" y="284" text-anchor="end" font-family="{SANS}" font-size="12" fill="{SLATE}">more sure</text>'
    return svg(W, H, b, "TIMEKEEPER",
               "Card for TIMEKEEPER: a photograph split between its damaged scan and restored version, with a confidence scale.")


def small_card(slug, title, lines, tags, motif, alt):
    W, H = 280, 280
    b = card_frame(W, H) + motif
    b += f'<text x="24" y="136" font-family="{SERIF}" font-size="27" font-weight="500" fill="{BONE}">{title}</text>'
    for i, l in enumerate(lines):
        b += f'<text x="24" y="{162 + i*19}" font-family="{SANS}" font-size="14" fill="{SLATE}">{l}</text>'
    x = 24
    for t in tags:
        c, w = chip(x, 216, t, h=24, fs=12.5)
        b += c
        x += w + 8
    b += f'<text x="24" y="258" font-family="{SANS}" font-size="12" fill="{SLATE}" opacity=".8">github.com/Nihir-Soni/{slug}</text>'
    return svg(W, H, b, title, alt)


def motif_orca():
    return f'''<text x="24" y="44" font-family="{SANS}" font-size="12.5" fill="{SLATE}">before</text><text x="256" y="44" text-anchor="end" font-family="{SERIF}" font-size="15" fill="{BONE}">32 s</text>
<rect x="24" y="52" width="232" height="12" rx="6" fill="#475569"/>
<text x="24" y="88" font-family="{SANS}" font-size="12.5" fill="{SLATE}">after</text><text x="256" y="88" text-anchor="end" font-family="{SERIF}" font-size="15" fill="{CYAN_L}">0.02 s</text>
<rect x="24" y="96" width="3" height="12" rx="1.5" fill="{CYAN}"/><rect x="18" y="90" width="15" height="24" rx="7" fill="{CYAN}" opacity=".18"/>'''


def motif_vault():
    return f'''<path d="M52 28L84 40V70C84 88 70 102 52 108C34 102 20 88 20 70V40Z" fill="{CYAN}" fill-opacity=".1" stroke="{CYAN}" stroke-width="2.5" stroke-linejoin="round" transform="translate(4 0)"/>
<path d="M56 54V82M42 68H70" stroke="{CYAN_L}" stroke-width="3.5" stroke-linecap="round"/>'''


def motif_amr():
    return f'<text x="20" y="100" font-family="{SERIF}" font-size="68" font-weight="700" letter-spacing="-1" fill="{TEAL}">AMR</text>'


def main():
    files = {
        "banner.svg": banner(),
        "stack.svg": stack(),
        "card-timekeeper.svg": wide_card(),
        "card-orca.svg": small_card("ORCA-2.0", "ORCA-2.0",
                                    ["Solo build with a live demo.", "A timeline benchmark fell from", "32 seconds to 0.02."],
                                    ["Solo", "Live demo"], motif_orca(), "ORCA-2.0: a benchmark fell from 32 seconds to 0.02 seconds."),
        "card-medaivault.svg": small_card("MedAiVault", "MedAiVault",
                                          ["Where medical data meets AI.", "Source and write-up are in", "the repository."],
                                          ["Healthcare", "AI"], motif_vault(), "MedAiVault: medical data and AI."),
        "card-amr.svg": small_card("AMR", "AMR",
                                   ["Source and write-up are in", "the repository."],
                                   [], motif_amr(), "AMR project card."),
    }
    for n, s in files.items():
        with open(os.path.join(OUT, n), "w") as f:
            f.write(s)
    print({n: len(s) for n, s in files.items()})


main()
