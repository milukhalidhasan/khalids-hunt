# Generates the floor-plan SVG (all geometry in inches) in English and Bengali and writes the pages.
import math, os

HERE = os.path.dirname(os.path.abspath(__file__))
W, D = 455, 426          # outer size of main block (in)
VER = 48                 # verandah depth (4')
STEP_D = 40              # 4 treads x 10"

BN_DIGITS = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")

def fmt(v, lang="en"):
    ft = int(v // 12); i = round(v - ft * 12)
    if i == 12: ft += 1; i = 0
    s = f"{ft}'" if i == 0 else f"{ft}'-{i}\""
    return s.translate(BN_DIGITS) if lang == "bn" else s

def n(v):
    return f"{v:.2f}".rstrip('0').rstrip('.')

S = []
def a(s): S.append(s)

def rect(x1, y1, x2, y2, cls, extra=""):
    a(f'<rect class="{cls}" x="{n(x1)}" y="{n(y1)}" width="{n(x2-x1)}" height="{n(y2-y1)}" {extra}/>')

def line(x1, y1, x2, y2, cls):
    a(f'<line class="{cls}" x1="{n(x1)}" y1="{n(y1)}" x2="{n(x2)}" y2="{n(y2)}"/>')

def text(x, y, s, cls, rot=False):
    t = f' transform="rotate(-90 {n(x)} {n(y)})"' if rot else ""
    a(f'<text class="{cls}" x="{n(x)}" y="{n(y)}"{t}>{s}</text>')

# ---------------------------------------------------------------- floors & walls
a('<g id="g-structure">')
rect(0, D, W, D + VER, "ver")
# steps
sx1, sx2 = 191.5, 263.5
rect(sx1, D + VER, sx2, D + VER + STEP_D, "ver step")
for k in range(1, 4):
    line(sx1, D + VER + 10 * k, sx2, D + VER + 10 * k, "stepline")
# verandah columns
for cx in (0, 151, 294, 445):
    rect(cx, D + VER - 10, cx + 10, D + VER, "wall")

rect(0, 0, W, D, "wall")
floors = [
    (10, 10, 154, 178, "fl"),      # bedroom 1
    (159, 10, 243, 130, "wet"),    # kitchen 7' x 10'
    (248, 10, 296, 94, "wet"),     # common bath 4' x 7'
    (248, 99, 296, 135, "fl"),     # basin niche
    (301, 10, 445, 178, "fl"),     # bedroom 2
    (99, 183, 356, 243, "fl"),     # middle band (dining side bays)
    (159, 135, 296, 303, "fl"),    # dining column
    (10, 183, 94, 243, "wet"),     # attached bath L
    (361, 183, 445, 243, "wet"),   # attached bath R
    (10, 248, 154, 416, "fl"),     # bedroom 3
    (301, 248, 445, 416, "fl"),    # bedroom 4
    (159, 308, 296, 416, "fl"),    # drawing room
]
for f in floors:
    rect(*f)

# ---------------------------------------------------------------- doors
def arc_path(cx, cy, p0, p1, r):
    a0 = math.atan2(p0[1] - cy, p0[0] - cx); a1 = math.atan2(p1[1] - cy, p1[0] - cx)
    d = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
    sweep = 1 if d > 0 else 0
    return f'M{n(p0[0])} {n(p0[1])} A{n(r)} {n(r)} 0 0 {sweep} {n(p1[0])} {n(p1[1])}'

def door(orient, w1, w2, s, e, hinge, swing):
    """orient h: wall spans y w1..w2, opening x s..e. v: wall spans x w1..w2, opening y s..e.
    hinge 's' or 'e'; swing +1 opens toward +axis side, -1 toward -axis side; None = open arch."""
    if orient == "h":
        rect(s, w1, e, w2, "opening")
        if swing is None: return
        face = w2 if swing > 0 else w1
        hx = s if hinge == "s" else e; ox = e if hinge == "s" else s
        r = e - s
        leaf_end = (hx, face + swing * r)
        line(hx, face, leaf_end[0], leaf_end[1], "leaf")
        a(f'<path class="swing" d="{arc_path(hx, face, leaf_end, (ox, face), r)}"/>')
    else:
        rect(w1, s, w2, e, "opening")
        if swing is None: return
        face = w2 if swing > 0 else w1
        hy = s if hinge == "s" else e; oy = e if hinge == "s" else s
        r = e - s
        leaf_end = (face + swing * r, hy)
        line(face, hy, leaf_end[0], leaf_end[1], "leaf")
        a(f'<path class="swing" d="{arc_path(face, hy, leaf_end, (face, oy), r)}"/>')

doors = [
    ("h", 416, 426, 206.5, 248.5, "s", -1),   # D1 main
    ("v", 154, 159, 139, 175, "e", -1),       # D2 bed1, opens flat against its south wall
    ("v", 296, 301, 139, 175, "e", +1),       # D2 bed2, opens flat against its south wall
    ("h", 243, 248, 114, 150, "e", +1),       # D2 bed3, opens flat against its east wall
    ("h", 243, 248, 305, 341, "s", +1),       # D2 bed4, opens flat against its west wall
    ("h", 130, 135, 199, 235, "e", -1),       # D2 kitchen
    ("h", 94, 99, 250, 280, "s", -1),         # D3 common bath
    ("h", 243, 248, 62, 92, "e", -1),         # D3 bath L (from bed3)
    ("h", 243, 248, 363, 393, "s", -1),       # D3 bath R (from bed4)
    ("v", 0, 10, 14, 50, "s", +1),            # D4 bed1 outside door in the north wall, opens flat against the east wall
    ("v", 0, 10, 252, 288, "s", +1),          # D4 bed3 outside door in the north wall, opens flat against the bath wall
    ("h", 303, 308, 250, 292, "s", None),     # O1 arch
]
for d_ in doors:
    door(*d_)

# ---------------------------------------------------------------- windows
def window(orient, w1, w2, s, e):
    if orient == "h":
        rect(s, w1, e, w2, "win")
        m = (w1 + w2) / 2
        line(s, m, e, m, "glass")
    else:
        rect(w1, s, w2, e, "win")
        m = (w1 + w2) / 2
        line(m, s, m, e, "glass")

windows = [
    ("h", 0, 10, 56, 110), ("v", 0, 10, 60, 114),         # bed1
    ("h", 0, 10, 371, 425), ("v", 445, 455, 60, 114),     # bed2
    ("v", 0, 10, 316, 370), ("h", 416, 426, 30, 84),      # bed3
    ("v", 445, 455, 300, 354), ("h", 416, 426, 371, 425), # bed4
    ("h", 416, 426, 166, 202), ("h", 416, 426, 253, 289), # drawing
    ("h", 0, 10, 183, 219),                               # kitchen
    ("h", 0, 10, 260, 284),                               # common bath vent
    ("v", 0, 10, 201, 225), ("v", 445, 455, 201, 225),    # attached bath vents
]
for w_ in windows:
    window(*w_)
a('</g>')

# ---------------------------------------------------------------- furniture
a('<g id="g-furn">')
def bed(x, y, L, Wd, head):  # head 'e' or 'w'
    rect(x, y, x + L, y + Wd, "furn", 'rx="2"')
    pw = (Wd - 12) / 2
    px = x + L - 14 if head == "e" else x + 2
    rect(px, y + 4, px + 12, y + 4 + pw, "furn2", 'rx="2"')
    rect(px, y + 8 + pw, px + 12, y + 8 + 2 * pw, "furn2", 'rx="2"')
    fx = x + 52 if head == "e" else x + L - 52
    line(fx, y, fx, y + Wd, "fline")
    line(fx, y, fx + (-10 if head == "e" else 10), y + 12, "fline")

bed(70, 30, 84, 72, "e"); bed(301, 30, 84, 72, "w")
bed(70, 312, 84, 60, "e"); bed(301, 312, 84, 60, "w")
for (x, y) in [(136, 12), (136, 102), (301, 12), (301, 102), (136, 294), (136, 372), (301, 294), (301, 372)]:
    rect(x, y, x + 18, y + 18, "furn", 'rx="1.5"')

def cupboard(x1, y1, x2, y2):
    rect(x1, y1, x2, y2, "furn")
    line(x1, y1, x2, y2, "fline"); line(x1, y2, x2, y1, "fline")
cupboard(10, 120, 32, 162); cupboard(423, 120, 445, 162)
cupboard(92, 398, 134, 416); cupboard(397, 248, 439, 270)
# dressing tables + stools
rect(80, 160, 116, 178, "furn"); a('<circle class="furn" cx="98" cy="150" r="6"/>')
rect(339, 160, 375, 178, "furn"); a('<circle class="furn" cx="357" cy="150" r="6"/>')
# study tables + chairs
rect(20, 392, 56, 416, "furn"); rect(29, 374, 47, 390, "furn", 'rx="2"')
rect(399, 392, 435, 416, "furn"); rect(408, 374, 426, 390, "furn", 'rx="2"')

# kitchen
rect(159, 10, 243, 34, "counter"); rect(219, 34, 243, 90, "counter")
rect(181, 14, 209, 30, "furn2", 'rx="1.5"')
a('<circle class="burner" cx="188" cy="22" r="4.5"/><circle class="burner" cx="202" cy="22" r="4.5"/>')
rect(222, 48, 240, 72, "furn2", 'rx="3"'); a('<circle class="burner" cx="231" cy="66" r="1.5"/>')
rect(161, 100, 189, 128, "furn"); line(161, 100, 189, 128, "fline")
rect(159, 50, 175, 96, "furn")
for yy in (65, 81): line(159, yy, 175, yy, "fline")

# toilets, drains, basin
# North-south runs along x on this drawing, so toilets run along x:
# tank against a side wall, bowl pointing +x (face > 0) or -x.
def wc(tank_x, cy, face):
    if face > 0:
        rect(tank_x, cy - 8, tank_x + 6, cy + 8, "furn2", 'rx="1"')
        a(f'<ellipse class="furn2" cx="{n(tank_x + 15.5)}" cy="{n(cy)}" rx="9.5" ry="7.5"/>')
    else:
        rect(tank_x - 6, cy - 8, tank_x, cy + 8, "furn2", 'rx="1"')
        a(f'<ellipse class="furn2" cx="{n(tank_x - 15.5)}" cy="{n(cy)}" rx="9.5" ry="7.5"/>')
wc(296, 24, -1); wc(10, 228, +1); wc(445, 228, -1)
def drain(cx, cy):
    a(f'<circle class="drain" cx="{n(cx)}" cy="{n(cy)}" r="3.2"/>')
    line(cx - 2.2, cy - 2.2, cx + 2.2, cy + 2.2, "fline"); line(cx - 2.2, cy + 2.2, cx + 2.2, cy - 2.2, "fline")
drain(258, 26); drain(30, 200); drain(425, 200)
rect(280, 110, 296, 130, "furn2", 'rx="2"'); a('<ellipse class="burner" cx="287" cy="120" rx="4.5" ry="6.5"/>')

# dining
rect(197.5, 225, 257.5, 261, "furn", 'rx="2"')
for (x, y, w, h) in [(205, 207, 18, 16), (232, 207, 18, 16), (205, 263, 18, 16), (232, 263, 18, 16),
                     (179, 234, 16, 18), (259.5, 234, 16, 18)]:
    rect(x, y, x + w, y + h, "furn", 'rx="2"')

# drawing room
rect(159, 330, 191, 408, "furn", 'rx="2"'); line(167, 330, 167, 408, "fline")
line(167, 356, 191, 356, "fline"); line(167, 382, 191, 382, "fline")
for yy in (334, 366):   # two armchairs against the right-hand wall
    rect(270, yy, 296, yy + 26, "furn", 'rx="2"'); line(290, yy, 290, yy + 26, "fline")
rect(209, 350, 245, 372, "furn", 'rx="1.5"')
a('</g>')

# skylight (always shown)
a('<rect class="sky" x="203.5" y="219" width="48" height="48"/>')

# everything above is the same in both languages
GEO = "".join(S)


def text_layers(lang):
    """Room names, tags, dimensions, compass and scale bar in one language."""
    S.clear()
    bn = lang == "bn"
    def q(t): return t.replace('"', '&quot;')
    def num(t): return t.translate(BN_DIGITS) if bn else t

    # ------------------------------------------------------------ room labels
    a('<g id="g-labels">')
    # (x, y of first line, English, Bengali, size, line gap)
    labels = [
        (75, 116, "BEDROOM 1", "শোবার ঘর ১", "12' × 14'", 10.5), (380, 116, "BEDROOM 2", "শোবার ঘর ২", "12' × 14'", 10.5),
        (66, 282, "BEDROOM 3", "শোবার ঘর ৩", "12' × 14'", 10.5), (395, 282, "BEDROOM 4", "শোবার ঘর ৪", "12' × 14'", 10.5),
        (197, 58, "KITCHEN", "রান্নাঘর", "7' × 10'", 10.5), (274, 42, "BATH", "বাথরুম", "4' × 7'", 9),
        (58, 195, "BATH", "বাথরুম", "7' × 5'", 9.5), (397, 195, "BATH", "বাথরুম", "7' × 5'", 9.5),
        (227.5, 147, "DINING", "ডাইনিং", "11'-5\" × 14'", 10.5), (228.5, 320, "DRAWING ROOM", "ড্রইং রুম", "11'-5\" × 9'", 10.5),
        (90, 444, "VERANDAH", "বারান্দা", "37'-11\" × 4'", 10.5),
    ]
    for x, y, en, bname, sz, g in labels:
        if bn:
            text(x, y + g * 0.5, bname, "rm"); text(x, y + g * 1.5, q(num(sz)), "sz")
        else:
            text(x, y, en, "rm"); text(x, y + g, bname, "bnl"); text(x, y + 2 * g, q(sz), "sz")
    if bn:
        text(264, 128, "বেসিন", "bnl")
        a('<text class="bnl" x="268" y="494" style="text-anchor:start">সিঁড়ি</text>')
        a('<text class="bnl" x="268" y="504" style="text-anchor:start">৪ ধাপ</text>')
    else:
        text(264, 123, "BASIN", "sz"); text(264, 132.5, "বেসিন", "bnl")
        a('<text class="sz" x="268" y="494" style="text-anchor:start">STEPS</text>')
        a('<text class="bnl" x="268" y="504" style="text-anchor:start">সিঁড়ি</text>')
    a('</g>')

    # ------------------------------------------------------------ tags (codes stay D1, W1... in both languages)
    a('<g id="g-tags">')
    tags = [
        (227.5, 441, "D1"), (168, 158, "D2"), (287, 158, "D2"), (132, 232, "D2"), (323, 232, "D2"),
        (196, 100, "D2"), (264, 111, "D3"), (77, 258, "D3"), (378, 258, "D3"),
        (271, 297, "O1"),
        (83, -6, "W1"), (398, -6, "W1"), (-12, 34.5, "D4"), (-12, 272.5, "D4"), (20, 89, "W1"), (435, 89, "W1"), (20, 345, "W1"), (435, 329, "W1"),
        (68, 406, "W1"), (387, 406, "W1"), (198, 406, "W2"), (262, 406, "W2"), (201, -6, "W3"),
        (272, -6, "V"), (20, 208, "V"), (435, 208, "V"), (258, 215, "SL"),
    ]
    for x, y, t in tags:
        text(x, y, t, "tag")
    if bn:
        a('<text class="tag" x="175" y="118" style="font-family:var(--f-bn)">ফ্রিজ</text>')
    else:
        text(175, 118, "FR", "tag")
    a('</g>')

    # ------------------------------------------------------------ dimensions
    a('<g id="g-dims">')
    def tick(x, y):
        line(x - 2.5, y + 2.5, x + 2.5, y - 2.5, "tick")

    def hchain(pts, y, from_y, labels_for):
        for p in pts:
            line(p, from_y, p, y - 4 if y < from_y else y + 4, "ext")
        line(pts[0] - 4, y, pts[-1] + 4, y, "dimline")
        for p in pts: tick(p, y)
        for (s, e) in labels_for:
            text((s + e) / 2, y - 3, q(fmt(e - s, lang)), "dimt")

    def vchain(pts, x, from_x, labels_for):
        for p in pts:
            line(from_x, p, x - 4 if x < from_x else x + 4, p, "ext")
        line(x, pts[0] - 4, x, pts[-1] + 4, "dimline")
        for p in pts:
            line(x - 2.5, p + 2.5, x + 2.5, p - 2.5, "tick")
        for (s, e) in labels_for:
            text(x - 3, (s + e) / 2, q(fmt(e - s, lang)), "dimt", rot=True)

    top = [0, 10, 154, 159, 243, 248, 296, 301, 445, 455]
    hchain(top, -30, -3, [(10, 154), (159, 243), (248, 296), (301, 445)])
    hchain([0, W], -58, -34, [(0, W)])
    bot = [0, 10, 154, 159, 296, 301, 445, 455]
    hchain(bot, D + VER + STEP_D + 20, D + VER + 3, [(10, 154), (159, 296), (301, 445)])
    left = [0, 10, 178, 183, 243, 248, 416, 426, D + VER]
    vchain(left, -30, -3, [(10, 178), (183, 243), (248, 416), (426, D + VER)])
    vchain([0, 426], -58, -34, [(0, 426)])
    a('</g>')

    # ------------------------------------------------------------ north arrow, compass, scale bar
    # front faces west: east is at the top of the sheet, north points left
    a('<g id="g-north" transform="translate(521 -52)">'
      '<circle class="nring" r="14"/>'
      '<path class="narrow" d="M-12 0 L8 6 L4 0 L8 -6 Z"/>'
      + ('' if bn else '<text class="rm" x="-25" y="3.5">N</text>') +
      '<text class="bnl" x="0" y="27">উত্তর</text></g>')
    if bn:
        text(227.5, -80, '<tspan class="cmpbn">পূর্ব · পিছন</tspan>', "cmp")
        text(227.5, 584, '<tspan class="cmpbn">পশ্চিম · সামনে</tspan>', "cmp")
        text(-84, 213, '<tspan class="cmpbn">উত্তর</tspan>', "cmp", rot=True)
        text(481, 213, '<tspan class="cmpbn">দক্ষিণ</tspan>', "cmp", rot=True)
    else:
        text(227.5, -80, 'EAST · BACK <tspan class="cmpbn">পূর্ব · পিছন</tspan>', "cmp")
        text(227.5, 584, 'WEST · FRONT <tspan class="cmpbn">পশ্চিম · সামনে</tspan>', "cmp")
        text(-84, 213, 'NORTH <tspan class="cmpbn">উত্তর</tspan>', "cmp", rot=True)
        text(481, 213, 'SOUTH <tspan class="cmpbn">দক্ষিণ</tspan>', "cmp", rot=True)
    a('<g transform="translate(336 558)">')
    for i in range(3):
        rect(i * 60, 0, i * 60 + 60, 5, "sb" + ("1" if i % 2 == 0 else "0"))
    scale = ["০", "৫ ফুট", "১০ ফুট", "১৫ ফুট"] if bn else ["0", "5 ft", "10 ft", "15 ft"]
    for i, lab in enumerate(scale):
        text(i * 60, 15, lab, "dimt")
    a('</g>')
    return "".join(S)


def build_svg(lang):
    if lang == "bn":
        title = "নিচতলার নকশা"
        desc = ("চার শোবার ঘরের একতলা বাড়ি, পশ্চিমমুখী, ৩৭ ফুট ১১ ইঞ্চি × ৩৫ ফুট ৬ ইঞ্চি, সামনে ৪ ফুট বারান্দা। "
                "চার কোণে চারটি শোবার ঘর, পেছনে (পূর্বে) রান্নাঘর ও কমন বাথরুম, উত্তর ও দক্ষিণ পাশে এটাচড বাথ, "
                "মাঝখানে স্কাইলাইটসহ ডাইনিং, সামনে (পশ্চিমে) ড্রইং রুম।")
    else:
        title = "Ground floor plan"
        desc = ("Single-storey four-bedroom house facing west, 37 ft 11 in by 35 ft 6 in, with a 4 ft front verandah. "
                "Bedrooms in the four corners, kitchen and common bath at the back (east), attached baths on the north and south sides, "
                "dining with skylight in the centre and drawing room at the front (west).")
    return ('<svg id="plan" viewBox="-100 -96 666 688" role="img" aria-labelledby="plan-title plan-desc" '
            'xmlns="http://www.w3.org/2000/svg">'
            f'<title id="plan-title">{title}</title><desc id="plan-desc">{desc}</desc>'
            + GEO + text_layers(lang) + '</svg>')


# Bengali pages reuse the English page's <head>, with the Bengali face swapped in for the Latin ones
BN_CSS = """
.bnpage,.bnpage h1,.bnpage h2,.bnpage .eyebrow,.bnpage .lead,.bnpage .tb-info dt,.bnpage .tb-info dd,.bnpage th,.bnpage td,.bnpage td.m,
.bnpage .notes li b,.bnpage .controls,.bnpage .controls .lbl,.bnpage .legend,.bnpage .foot,.bnpage .cap,.bnpage .capsub{font-family:var(--f-bn)}
.bnpage .eyebrow,.bnpage h2,.bnpage .tb-info dt,.bnpage th,.bnpage .notes li b,.bnpage .controls .lbl{letter-spacing:0;text-transform:none}
.bnpage h1{line-height:1.25}
.bnpage .eyebrow,.bnpage .tb-info dt,.bnpage th,.bnpage .controls .lbl{font-size:.8rem}
.bnpage #plan .rm{font-family:var(--f-bn);font-weight:600;font-size:10px;letter-spacing:0}
.bnpage #plan .sz{font-family:var(--f-bn);font-size:8.5px}
.bnpage #plan .dimt{font-family:var(--f-bn);font-size:9px}
.bnpage #plan .cmpbn{font-size:10px}
.bnpage .credit-lbl{font-family:var(--f-bn);letter-spacing:0;text-transform:none;font-size:.8rem}
.bnpage .credit-name{font-family:var(--f-bn);letter-spacing:0}
"""

OUT = os.path.dirname(HERE)   # the House_plan folder
tpl = open(os.path.join(HERE, "plan_template.html"), encoding="utf-8").read()
tpl_head, tpl_body = tpl.split('<main class="page">', 1)
tpl_body = '<main class="page">' + tpl_body
style = tpl.split("<style>", 1)[1].split("</style>", 1)[0]
fonts = [l for l in tpl.splitlines() if l.startswith("<link")]

bn_body = open(os.path.join(HERE, "plan_body_bn.html"), encoding="utf-8").read()
bn_head = (tpl_head.replace("<title>Four-Bedroom Village House</title>", "<title>গ্রামের বাড়ির নকশা</title>")
                   .replace("</style>", BN_CSS + "</style>"))
assert "গ্রামের বাড়ির নকশা" in bn_head


def write(path, s):
    open(path, "w", encoding="utf-8").write(s)


for lang, head, body, suffix in (("en", tpl_head, tpl_body, ""), ("bn", bn_head, bn_body, "-bn")):
    svg = build_svg(lang)
    body = body.replace("<!--SVG-->", svg)
    # 1) fragment for the published artifact (the host adds <html>/<head>/<body>)
    write(os.path.join(HERE, f"artifact-page{suffix}.html"), head + body)
    # 2) standalone page that opens in any browser
    write(os.path.join(OUT, f"village-house-plan{suffix}.html"),
          f'<!doctype html>\n<html lang="{lang}">\n<head>\n'
          '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
          + head + '</head>\n<body>\n' + body + '\n</body>\n</html>\n')
    # 3) drawing-only page, screenshotted to a PNG for WhatsApp
    credit_lbl = "নকশা করেছেন" if lang == "bn" else "Designed by"
    credit_name = "মোঃ খালিদ হাসান মিলু" if lang == "bn" else "Md. Khalid Hasan Milu"
    credit_aff = ("কৃষিবনায়ন ও পরিবেশ বিভাগ, গাজীপুর কৃষি বিশ্ববিদ্যালয়, গাজীপুর-১৭০৬, বাংলাদেশ" if lang == "bn" else
                  "Department of Agroforestry and Environment, Gazipur Agricultural University, Gazipur-1706, Bangladesh")
    credit = ('<div class="credit"><span class="credit-lbl">' + credit_lbl + '</span>'
              '<span class="credit-name">' + credit_name + '</span>'
              '<span class="credit-aff">' + credit_aff + '</span></div>')
    if lang == "bn":
        caption = ('<div class="wrap bnpage"><div class="cap">চার রুমের একতলা বাড়ির নকশা</div>'
                   '<div class="capsub">সামনে পশ্চিম দিক · সব মাপ দেয়ালের ভেতরের · বাইরের দেয়াল ১০&quot;, ভেতরের দেয়াল ৫&quot; · '
                   'বাইরের মাপ ৩৭\'-১১&quot; × ৩৫\'-৬&quot; + ৪\' বারান্দা</div>')
        extra_css = BN_CSS
    else:
        caption = ('<div class="wrap"><div class="cap">Four-bedroom village house · ground floor plan '
                   '<span class="capbn">চার রুমের একতলা বাড়ির নকশা</span></div>'
                   '<div class="capsub">Front faces west · sizes are clear inside walls · walls 10&quot; outer, 5&quot; inner · '
                   'outer size 37\'-11&quot; × 35\'-6&quot; + 4\' verandah</div>'
                   '<div class="capsub capbn2">সামনে পশ্চিম দিক · মাপ দেয়ালের ভেতরের · বাইরের দেয়াল ১০&quot;, ভেতরের দেয়াল ৫&quot;</div>')
        extra_css = ""
    write(os.path.join(HERE, f"drawing-only{suffix}.html"),
          f'<!doctype html>\n<html lang="{lang}" data-theme="light">\n<head>\n<meta charset="utf-8">\n'
          '<title>Village house plan drawing</title>\n' + "\n".join(fonts) + '\n<style>' + style +
          'body{margin:0;background:var(--sheet)}'
          '.wrap{width:1600px;padding:26px 30px;box-sizing:border-box}'
          '.cap{font:600 30px/1.2 var(--f-display);letter-spacing:.02em}'
          '.capsub{font:400 17px/1.4 var(--f-mono);color:var(--ink-2);margin-top:6px}'
          '.capbn{font:500 24px/1.1 var(--f-bn);letter-spacing:0;color:var(--ink-2);margin-left:10px}'
          '.capbn2{font-family:var(--f-bn);font-size:18px;margin-top:2px}'
          '#plan{min-width:0;width:100%}'
          '.wrap .credit{margin-top:6px}.wrap .credit-lbl{font-size:13px}.wrap.bnpage .credit-lbl{font-size:17px}.wrap .credit-name{font-size:26px}.wrap .credit-aff{font-size:18px}'
          + extra_css + '</style>\n</head>\n<body>\n'
          + caption + svg + credit + '</div>\n</body>\n</html>\n')
    print("ok", lang, len(svg))
