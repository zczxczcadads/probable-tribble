"""Облики мечей. Модель стоит вертикально: рукоять внизу (центр хвата около y=1.5), клинок вверх."""
import math

from kit import Mat, Model


class Pix:
    """Холст клеток для sprite: x — столбец, y — высота в единицах модели (низ холста — y0)."""

    def __init__(self, w=13, h=31, y0=-2):
        self.w, self.h, self.y0 = w, h, y0
        self.g = [[" "] * w for _ in range(h)]

    def put(self, x, y, ch):
        j = int(y - self.y0)
        if 0 <= x < self.w and 0 <= j < self.h:
            self.g[self.h - 1 - j][x] = ch

    def row(self, y, x0, x1, ch):
        for x in range(x0, x1 + 1):
            self.put(x, y, ch)

    def col(self, x, y0, y1, ch):
        for y in range(y0, y1 + 1):
            self.put(x, y, ch)

    def sym(self, x, y, ch):
        self.put(x, y, ch)
        self.put(self.w - 1 - x, y, ch)

    def rows(self):
        return ["".join(r) for r in self.g]

    def at(self):
        return (8 - self.w / 2, self.y0)


def D(mat, a, b):
    return {"mat": mat, "depth": (a, b)}


def gem(m, mat, cx=8, cy=6, s=1.0, d=1.5):
    """Ромбовидный камень, торчащий из гарды в обе стороны."""
    m.box((cx - s, cy - s, 8 - d), (cx + s, cy + s, 8 + d), mat, rot=("z", 45, (cx, cy, 8)))


def frost():
    m = Model("sword_frost", "Ледяной клинок", "sword")
    ice = Mat("crystal", "#2a6fb0", "#58b4e6", "#a8e6ff", "#eaffff")
    core = Mat("flat", "#9fe4ff", "#ffffff", glow=True)
    guard = Mat("metal", "#27425e", "#4f7ba6", "#9cc7e8", "#e8f6ff")
    grip = Mat("wrap", "#1d2a44", "#31476e", "#4a6a9a")
    gem = Mat("gem", "#0b5ea8", "#28b4ff", "#b8f1ff", glow=True)
    m.sprite([
        "    i    ",
        "    i    ",
        "   iii   ",
        "   ici   ",
        "   ici   ",
        "  iici   ",
        "   ici   ",
        "   ici   ",
        "   icii  ",
        "   ici   ",
        "   ici   ",
        "   ici   ",
        "  iici   ",
        "   ici   ",
        "   icii  ",
        "   ici   ",
        "   ici   ",
        "   ici   ",
        "  iicii  ",
        " ggggggg ",
        "gg ggg gg",
        "    h    ",
        "    h    ",
        "    h    ",
        "    h    ",
        "    h    ",
        "   ppp   ",
        "    p    ",
    ], {
        "i": ice,
        "c": {"mat": core, "depth": (7.2, 8.8)},
        "g": {"mat": guard, "depth": (6.9, 9.1)},
        "h": {"mat": grip, "depth": (7.3, 8.7)},
        "p": {"mat": guard, "depth": (7.0, 9.0)},
    }, at=(3.5, -2), depth=(7.5, 8.5))
    m.box((7, 5, 6.5), (9, 7, 9.5), gem, rot=("z", 45, (8, 6, 8)))
    return m


def blood():
    m = Model("sword_blood", "Кровавый жнец", "sword")
    blade = Mat("metal", "#3a0710", "#7a1020", "#b8202e", "#f06a6a")
    dark = Mat("metal", "#1e0308", "#4a0a14", "#7a1424", "#a8283a")
    tooth = Mat("metal", "#2a050c", "#6a0e1c", "#b0202e", "#ff7070")
    core = Mat("flat", "#ff2a2a", "#ffa090", glow=True)
    hilt = Mat("metal", "#0c0c10", "#1c1c24", "#33333f", "#5a5a68")
    wrap = Mat("wrap", "#08080b", "#16161d", "#2a2a36")
    ruby = Mat("gem", "#6a0010", "#d0102a", "#ff5a6a", "#ffd0d0", glow=True)
    p = Pix()
    for y in range(7, 25):
        p.row(y, 4, 8, "m")
        p.put(4, y, "l")
        p.put(8, y, "d")
        p.put(6, y, "c")
    p.row(24, 5, 7, "m")
    p.put(5, 24, "l"); p.put(6, 24, "c"); p.put(7, 24, "d")
    p.row(25, 5, 7, "m")
    p.put(5, 25, "l"); p.put(6, 25, "c"); p.put(7, 25, "d")
    p.put(6, 26, "l")
    for a in (22, 19, 16, 13, 10):
        p.put(9, a, "t"); p.put(10, a, "t"); p.put(9, a - 1, "t")
    for a in (21, 17, 12):
        p.put(3, a, "d")
    p.row(7, 1, 2, "g"); p.row(7, 10, 11, "g")
    p.row(6, 1, 11, "g")
    p.row(5, 2, 10, "g")
    for x in (1, 11):
        p.put(x, 4, "g"); p.put(x, 3, "g")
    p.col(6, 0, 4, "h")
    for y in (0, 2, 4):
        p.put(6, y, "k")
    p.row(-1, 5, 7, "p")
    p.put(6, -2, "r")
    m.sprite(p.rows(), {
        "l": D(blade, 7.5, 8.5), "m": D(dark, 7.4, 8.6), "d": D(dark, 7.6, 8.4),
        "c": D(core, 7.2, 8.8), "t": D(tooth, 7.5, 8.5),
        "g": D(hilt, 6.9, 9.1), "h": D(wrap, 7.3, 8.7), "k": D(hilt, 7.0, 9.0),
        "p": D(hilt, 7.0, 9.0), "r": D(ruby, 6.8, 9.2),
    }, at=p.at(), depth=(7.5, 8.5))
    gem(m, ruby)
    return m


def emerald():
    m = Model("sword_emerald", "Изумрудный страж", "sword")
    blade = Mat("metal", "#0b4a2a", "#1c8a4c", "#3fd07a", "#b8ffd0")
    edge = Mat("metal", "#063a20", "#0f6a38", "#28a860", "#7af0a8")
    gold = Mat("metal", "#6b4a10", "#b8861c", "#f2c94c", "#fff0a0", edge="bevel")
    wing = Mat("metal", "#8a6218", "#d9a62c", "#ffe27a", "#fffbd0")
    jewel = Mat("gem", "#04602c", "#10c060", "#7affb0", "#ddffee", glow=True)
    wrap = Mat("wrap", "#0f2a1a", "#1c4a2e", "#2e7048")
    p = Pix()
    for y in range(8, 22):
        p.row(y, 3, 9, "m")
        p.put(3, y, "e"); p.put(9, y, "e"); p.put(6, y, "f")
    for y in (22, 23):
        p.row(y, 4, 8, "m")
        p.put(4, y, "e"); p.put(8, y, "e"); p.put(6, y, "f")
    for y in (24, 25):
        p.row(y, 5, 7, "m")
        p.put(5, y, "e"); p.put(7, y, "e"); p.put(6, y, "f")
    p.put(6, 26, "e")
    p.put(6, 12, "j"); p.put(6, 17, "j")
    p.row(7, 4, 8, "G")
    p.row(6, 1, 11, "G")
    p.row(5, 3, 9, "G")
    p.row(4, 5, 7, "G")
    p.row(7, 0, 2, "w"); p.row(7, 10, 12, "w")
    p.row(8, 0, 1, "w"); p.row(8, 11, 12, "w")
    p.put(0, 9, "w"); p.put(12, 9, "w")
    p.put(3, 6, "j"); p.put(9, 6, "j")
    p.col(6, 0, 3, "h")
    for y in (1, 3):
        p.row(y, 5, 7, "G")
    p.put(6, 1, "G")
    p.row(-1, 5, 7, "G")
    p.put(6, -2, "j")
    m.sprite(p.rows(), {
        "m": D(blade, 7.3, 8.7), "e": D(edge, 7.6, 8.4), "f": D(gold, 7.1, 8.9),
        "j": D(jewel, 6.8, 9.2), "G": D(gold, 6.9, 9.1), "w": D(wing, 7.2, 8.8),
        "h": D(wrap, 7.3, 8.7),
    }, at=p.at(), depth=(7.5, 8.5))
    gem(m, jewel, s=1.2, d=1.6)
    return m


def amethyst():
    m = Model("sword_amethyst", "Аметистовый осколок", "sword")
    body = Mat("crystal", "#3b1a78", "#7a3ccf", "#b57cff", "#ead6ff")
    shade = Mat("crystal", "#240e50", "#4a2290", "#7a44c8", "#a876ee")
    light = Mat("crystal", "#6a3cb8", "#a46cf0", "#d8b0ff", "#ffffff")
    core = Mat("flat", "#c070ff", "#fff0ff", glow=True)
    metal = Mat("metal", "#1a1030", "#2e2050", "#4c3a80", "#8b78c8")
    wrap = Mat("wrap", "#1a0f33", "#2c1a55", "#4a2e82")
    shard = Mat("crystal", "#4a22a0", "#8c4ee0", "#c696ff", "#f4e6ff", glow=True)
    span = {7: (5, 7), 8: (4, 8), 9: (4, 8), 10: (3, 8), 11: (3, 8), 12: (4, 9), 13: (4, 9),
            14: (4, 8), 15: (5, 9), 16: (5, 9), 17: (5, 10), 18: (5, 9), 19: (5, 8), 20: (5, 8),
            21: (6, 8), 22: (6, 8), 23: (6, 8), 24: (7, 8), 25: (7, 8), 26: (7, 7)}
    p = Pix()
    for y, (l, r) in span.items():
        p.row(y, l, r, "c")
        p.put(l, y, "h")
        if r > l:
            p.put(r, y, "d")
        if 9 <= y <= 23:
            p.put((l + r) // 2, y, "k")
    p.row(6, 2, 10, "g"); p.row(5, 3, 9, "g")
    p.col(6, 0, 4, "w")
    for y in (0, 2, 4):
        p.row(y, 5, 7, "g")
    p.row(-1, 5, 7, "g"); p.put(6, -2, "k")
    m.sprite(p.rows(), {
        "c": D(body, 7.3, 8.7), "h": D(light, 7.6, 8.4), "d": D(shade, 7.5, 8.5),
        "k": D(core, 7.0, 9.0), "g": D(metal, 6.9, 9.1), "w": D(wrap, 7.3, 8.7),
    }, at=p.at(), depth=(7.5, 8.5))
    # кристаллы, растущие из гарды и из клинка
    m.box((3.2, 6, 7.1), (5.7, 12, 8.9), shard, rot=("z", 22.5, (4.5, 6, 8)))
    m.box((3.2, 6, 7.4), (5, 9.5, 8.6), shard, rot=("z", 45, (4.2, 6, 8)))
    m.box((10.3, 6, 7.0), (12.8, 11, 9.0), shard, rot=("z", -22.5, (11.5, 6, 8)))
    m.box((10.8, 6, 7.4), (12.6, 9.5, 8.6), shard, rot=("z", -45, (11.8, 6, 8)))
    m.box((4.0, 10.5, 7.5), (5.3, 14.5, 8.5), shard, rot=("z", 22.5, (4.8, 10.5, 8)))
    m.box((11.6, 12.5, 7.4), (12.8, 16.5, 8.6), shard, rot=("z", -22.5, (12.2, 12.5, 8)))
    m.box((7.0, 4.5, 6.8), (9.0, 7.0, 9.2), shard, rot=("z", 45, (8, 5.8, 8)))
    return m


def solar():
    m = Model("sword_solar", "Клинок солнца", "sword")
    orange = Mat("metal", "#8a2a05", "#d9500c", "#ff8a1c", "#ffc060")
    gold = Mat("metal", "#a8660a", "#ecab1c", "#ffd84a", "#fff3a0")
    core = Mat("flat", "#fff2a0", "#ffffff", glow=True)
    ring = Mat("metal", "#7a2a06", "#c24a0c", "#ff8a24", "#ffcf70")
    disc = Mat("metal", "#a86c0c", "#f0b428", "#ffe070", "#fff8c0")
    ray = Mat("metal", "#b8560a", "#ff9a1c", "#ffd048", "#fff0a0")
    wrap = Mat("wrap", "#5a2a0c", "#8a4a16", "#bf7a2a")
    p = Pix()
    cx, cy = 6, 7
    for y in range(3, 12):
        for x in range(13):
            d = math.hypot(x - cx, y - cy)
            if d <= 1.6:
                p.put(x, y, "k")
            elif d <= 2.6:
                p.put(x, y, "D")
            elif d <= 3.5:
                p.put(x, y, "O")
    for x, y in [(0, 7), (1, 7), (2, 7), (10, 7), (11, 7), (12, 7), (1, 11), (2, 10), (10, 10), (11, 11),
                 (1, 3), (2, 4), (10, 4), (11, 3), (5, 2), (7, 2)]:
        p.put(x, y, "r")
    for y in range(11, 28):
        off = [0, 1, 1, 0, -1, -1][(y - 11) % 6]
        c = 6 + off
        if y >= 24:
            c = 6
        w = 2 if y < 23 else 1
        if y == 27:
            w = 0
        for x in range(c - w, c + w + 1):
            p.put(x, y, "y")
        p.put(c - w, y, "o"); p.put(c + w, y, "o"); p.put(c, y, "w")
    p.col(6, -1, 3, "h")
    for y in (-1, 1):
        p.row(y, 5, 7, "b")
    p.row(-2, 5, 7, "b")
    p.put(6, -2, "k")
    m.sprite(p.rows(), {
        "k": D(core, 6.6, 9.4), "D": D(disc, 7.0, 9.0), "O": D(ring, 7.1, 8.9),
        "r": D(ray, 7.5, 8.5), "o": D(orange, 7.5, 8.5), "y": D(gold, 7.3, 8.7),
        "w": D(core, 7.0, 9.0), "h": D(wrap, 7.3, 8.7), "b": D(gold, 7.0, 9.0),
    }, at=p.at(), depth=(7.5, 8.5))
    return m


def abyss():
    m = Model("sword_abyss", "Клинок бездны", "sword")
    dark = Mat("metal", "#04141a", "#0a2a33", "#12485a", "#2a7a8c")
    mid = Mat("metal", "#0a2e38", "#14505e", "#1f7a8a", "#44aab8")
    rune = Mat("flat", "#27e0ff", "#b8faff", glow=True)
    tent = Mat("metal", "#071c24", "#0f3a48", "#1a6070", "#2f8c9c")
    sucker = Mat("gem", "#0d6a7c", "#2ec8e0", "#9cf4ff", glow=True)
    eye = Mat("gem", "#0b7a90", "#38e6ff", "#c8fbff", "#ffffff", glow=True)
    pupil = Mat("flat", "#02060a", "#08202a")
    wrap = Mat("wrap", "#050f14", "#0c2630", "#164050")
    p = Pix()
    for y in range(8, 24):
        p.row(y, 4, 8, "m")
        p.put(4, y, "d"); p.put(8, y, "d")
    for y in (14, 15, 19, 20):
        p.put(9, y, "d")
    for y in (24, 25):
        p.row(y, 5, 7, "m")
        p.put(5, y, "d"); p.put(7, y, "d")
    p.put(6, 26, "d")
    for y in (10, 11, 13, 15, 16, 18, 20, 21, 23):
        p.put(6, y, "r")
    for x, y in [(5, 11), (7, 13), (5, 16), (7, 18), (5, 21), (7, 9), (5, 14)]:
        p.put(x, y, "r")
    for x in range(0, 5):
        p.sym(x, 7, "t"); p.sym(x, 5, "t")
    for x, y in [(3, 6), (4, 6), (0, 8), (0, 9), (1, 9), (2, 9), (0, 4), (0, 3), (1, 3), (2, 3)]:
        p.sym(x, y, "t")
    for x, y in [(2, 9), (2, 3), (2, 5)]:
        p.sym(x, y, "s")
    p.row(5, 5, 7, "e"); p.row(6, 5, 7, "e"); p.row(7, 5, 7, "e")
    for x, y in [(5, 5), (7, 5), (5, 7), (7, 7)]:
        p.put(x, y, "t")
    p.put(6, 6, "P")
    p.col(6, 0, 4, "h")
    for y in (0, 2, 4):
        p.put(6, y, "t")
    p.row(-1, 5, 7, "t"); p.put(6, -2, "s")
    m.sprite(p.rows(), {
        "m": D(mid, 7.4, 8.6), "d": D(dark, 7.5, 8.5), "r": D(rune, 7.2, 8.8),
        "t": D(tent, 7.0, 9.0), "s": D(sucker, 6.8, 9.2), "e": D(eye, 6.6, 9.4),
        "P": D(pupil, 6.3, 9.7), "h": D(wrap, 7.3, 8.7),
    }, at=p.at(), depth=(7.5, 8.5))
    return m


def sakura():
    m = Model("sword_sakura", "Клинок сакуры", "sword")
    edge = Mat("metal", "#e9a8c4", "#f8d4e4", "#ffffff", "#ffffff")
    body = Mat("metal", "#a8446e", "#e0749e", "#f7aac6", "#fde0ec")
    spine = Mat("metal", "#6a2444", "#a8446e", "#d36a96", "#f0a0c0")
    gold = Mat("metal", "#7a5a14", "#c9a14a", "#ffe08a", "#fff6c8")
    tsuba = Mat("metal", "#3a1a2c", "#6a3a52", "#c9a14a", "#ffe08a")
    jewel = Mat("gem", "#a82a5e", "#ff5c9a", "#ffc0dc", "#ffffff", glow=True)
    wrap1 = Mat("wrap", "#7a1e48", "#a8326a", "#d05a90")
    wrap2 = Mat("wrap", "#e8b0c8", "#f8d4e4", "#ffffff")
    cord = Mat("cloth", "#a8326a", "#e0649a", "#ff9cc4")
    p = Pix(h=35, y0=-7)
    for y in range(9, 28):
        c = 6 + int(round(((y - 9) / 18) ** 2 * 2.5))
        if y <= 25:
            p.put(c - 1, y, "e"); p.put(c, y, "b"); p.put(c + 1, y, "s")
        elif y == 26:
            p.put(c - 1, y, "e"); p.put(c, y, "b")
        else:
            p.put(c, y, "e")
    p.row(7, 5, 7, "g"); p.row(8, 5, 7, "g")
    p.row(6, 4, 8, "t"); p.row(5, 3, 9, "t"); p.row(4, 4, 8, "t")
    p.put(6, 5, "j")
    for y in range(0, 4):
        for x in range(5, 8):
            p.put(x, y, "a" if (x + y) % 2 == 0 else "c")
    p.row(-1, 5, 7, "g"); p.put(6, -2, "j")
    p.col(6, -4, -3, "f"); p.row(-5, 5, 7, "f"); p.put(5, -6, "f"); p.put(7, -6, "f")
    m.sprite(p.rows(), {
        "e": D(edge, 7.5, 8.5), "b": D(body, 7.4, 8.6), "s": D(spine, 7.3, 8.7),
        "g": D(gold, 7.2, 8.8), "t": D(tsuba, 6.9, 9.1), "j": D(jewel, 6.6, 9.4),
        "a": D(wrap1, 7.2, 8.8), "c": D(wrap2, 7.3, 8.7), "f": D(cord, 7.5, 8.5),
    }, at=p.at(), depth=(7.5, 8.5))
    petal = Mat("gem", "#c9407a", "#ff8fb8", "#ffd0e2", "#ffffff")
    for x, y, z, a in [(12.6, 13, 8.9, 45), (3.0, 18, 7.1, 45), (13.2, 21, 8.2, 45),
                       (2.6, 11, 8.6, 45), (11.8, 3.5, 7.0, 45), (3.6, 23, 8.8, 45)]:
        m.box((x - 0.5, y - 0.5, z - 0.25), (x + 0.5, y + 0.5, z + 0.25), petal, rot=("z", a, (x, y, z)))
    return m


def nature():
    m = Model("sword_nature", "Клинок леса", "sword")
    leaf = Mat("flat", "#2e7a22", "#4cb83a", "#8be85a", "#d0ff90")
    leaf_body = Mat("flat", "#1f5a1a", "#34902c", "#58c840", "#9aea6a")
    vein = Mat("wood", "#6a4a20", "#9a7236", "#c8a058", "#e8c888")
    vine = Mat("wood", "#183a14", "#245a1c", "#3a8a2c", "#62b84a")
    leaf2 = Mat("flat", "#3a9a2a", "#66d248", "#a8f870", "#e0ffb0")
    bark = Mat("wood", "#3a2410", "#5e3c1c", "#8a5c2c", "#b88a4a")
    seed = Mat("gem", "#4a9a10", "#b0f030", "#f0ff90", "#ffffff", glow=True)
    petal = Mat("gem", "#c83a78", "#ff7aac", "#ffc0d8", "#ffffff")
    heart = Mat("flat", "#ffe060", "#fffbb0", glow=True)
    half = {8: 1, 9: 2, 10: 2, 11: 3, 12: 3, 13: 3, 14: 3, 15: 3, 16: 3, 17: 2, 18: 2, 19: 2,
            20: 1, 21: 1, 22: 1, 23: 1, 24: 0, 25: 0, 26: 0}
    p = Pix()
    for y, h in half.items():
        for x in range(6 - h, 6 + h + 1):
            p.put(x, y, "b")
        p.put(6 - h, y, "e"); p.put(6 + h, y, "e"); p.put(6, y, "v")
    for x, y in [(5, 11), (7, 11), (4, 12), (8, 12), (5, 14), (7, 14), (4, 15), (8, 15), (5, 17), (7, 17)]:
        p.put(x, y, "v")
    for x, y in zip(range(3, 10), range(11, 18)):
        p.put(x, y, "V")
    for x, y in zip(range(9, 3, -1), range(18, 24)):
        p.put(x, y, "U")
    for x, y in [(2, 11), (2, 12), (1, 12), (10, 17), (10, 18), (11, 18), (3, 23), (3, 24), (2, 24)]:
        p.put(x, y, "L")
    p.row(6, 1, 11, "w"); p.row(5, 3, 9, "w")
    p.row(7, 0, 1, "L"); p.put(0, 8, "L"); p.put(1, 8, "L")
    p.put(2, 7, "w"); p.put(10, 7, "w")
    for x, y in [(11, 8), (10, 8), (12, 8), (11, 9), (11, 7)]:
        p.put(x, y, "f")
    p.put(11, 8, "y")
    p.col(6, 0, 4, "h")
    for y in (1, 3):
        p.put(6, y, "V")
    p.row(-1, 5, 7, "w"); p.put(6, -2, "z")
    m.sprite(p.rows(), {
        "b": D(leaf_body, 7.4, 8.6), "e": D(leaf, 7.6, 8.4), "v": D(vein, 7.5, 8.5),
        "V": D(vine, 7.7, 9.2), "U": D(vine, 6.7, 8.2), "L": D(leaf2, 7.7, 8.3),
        "w": D(bark, 6.9, 9.1), "f": D(petal, 7.2, 8.8), "y": D(heart, 6.8, 9.2),
        "h": D(bark, 7.3, 8.7), "z": D(seed, 6.8, 9.2),
    }, at=p.at(), depth=(7.5, 8.5))
    gem(m, seed, s=0.9, d=1.4)
    return m


def thunder():
    m = Model("sword_thunder", "Громовой клинок", "sword")
    edge = Mat("metal", "#1a5ac8", "#3a8cff", "#8cc8ff", "#e0f4ff")
    body = Mat("metal", "#0c2e8a", "#1c58d0", "#3a90ff", "#70b8ff")
    shade = Mat("metal", "#081c5a", "#0f3a9a", "#2060d0", "#4a8cf0")
    bolt = Mat("flat", "#ffe030", "#fffbb0", glow=True)
    guard = Mat("metal", "#0a1230", "#16224a", "#2a3c7a", "#5870b8")
    wrap = Mat("wrap", "#0a1030", "#152050", "#243a80")
    spark = Mat("flat", "#fff060", "#ffffff", glow=True)
    p = Pix()
    off = {8: 0, 9: 0, 10: 0, 11: 1, 12: 2, 13: 2, 14: 1, 15: 0, 16: -1, 17: -2, 18: -2, 19: -1,
           20: 0, 21: 1, 22: 2, 23: 2, 24: 2, 25: 1, 26: 1, 27: 0}
    prev = 0
    for y in range(8, 28):
        c = 6 + off[y]
        w = 2 if y <= 23 else (1 if y <= 25 else 0)
        for x in range(c - w, c + w + 1):
            p.put(x, y, "b")
        p.put(c - w, y, "e")
        if w:
            p.put(c + w, y, "d")
        lo, hi = min(c, 6 + prev), max(c, 6 + prev)
        for x in range(lo, hi + 1):
            p.put(x, y, "y")
        prev = off[y]
    p.row(6, 1, 11, "g"); p.row(5, 2, 10, "g")
    p.put(1, 7, "g"); p.put(11, 7, "g")
    for x, y in [(0, 7), (0, 8), (12, 7), (12, 8), (0, 6), (12, 6), (2, 4), (1, 3), (10, 4), (11, 3), (3, 4), (9, 4)]:
        p.put(x, y, "z")
    p.col(6, 0, 4, "h")
    for y in (0, 2, 4):
        p.put(6, y, "z")
    p.row(-1, 5, 7, "g"); p.put(6, -2, "z")
    m.sprite(p.rows(), {
        "b": D(body, 7.4, 8.6), "e": D(edge, 7.6, 8.4), "d": D(shade, 7.5, 8.5),
        "y": D(bolt, 7.35, 8.65), "g": D(guard, 6.9, 9.1), "z": D(bolt, 7.2, 8.8),
        "h": D(wrap, 7.3, 8.7),
    }, at=p.at(), depth=(7.5, 8.5))
    gem(m, bolt, s=0.9, d=1.4)
    for x, y, z in [(13.4, 12, 8.6), (2.4, 16, 7.4), (13.0, 22, 8.0), (2.6, 24, 8.8),
                    (13.6, 17, 7.3), (2.2, 10.5, 8.5)]:
        m.box((x - 0.4, y - 0.4, z - 0.2), (x + 0.4, y + 0.4, z + 0.2), spark, rot=("z", 45, (x, y, z)))
    return m


def lunar():
    m = Model("sword_lunar", "Лунный серп", "sword")
    edge = Mat("metal", "#7a8ac8", "#b8c4f0", "#eef2ff", "#ffffff")
    body = Mat("metal", "#1a1450", "#2e2488", "#4a3cb0", "#7a6ae0")
    shade = Mat("metal", "#0e0a30", "#1c1660", "#2e2488", "#4a3cb0")
    silver = Mat("metal", "#6a74a8", "#aab4e0", "#e8ecff", "#ffffff")
    star = Mat("flat", "#fff6c0", "#ffffff", glow=True)
    moonstone = Mat("gem", "#8a9ae0", "#d0dcff", "#f4f8ff", "#ffffff", glow=True)
    wrap = Mat("wrap", "#0e0a30", "#1c1660", "#2e2488")
    p = Pix()
    for y in range(7, 17):
        p.put(4, y, "e"); p.row(y, 5, 7, "b"); p.put(8, y, "d")
        p.put(6, y, "n")
    for y in (10, 13):
        p.put(6, y, "k")
    p.put(6, 8, "k"); p.put(6, 15, "k")
    cx, cy, r1 = 6, 21, 6.0
    ix, iy, r2 = 8.3, 21.6, 4.7
    for y in range(15, 27):
        for x in range(13):
            if math.hypot(x - cx, y - cy) <= r1 and math.hypot(x - ix, y - iy) > r2:
                p.put(x, y, "c")
    for x, y in [(8, 22), (8, 23), (8, 21), (7, 22), (9, 22), (11, 26), (10, 18)]:
        p.put(x, y, "k")
    p.row(4, 5, 7, "a")
    p.row(5, 4, 8, "a"); p.row(6, 2, 10, "a")
    p.row(7, 1, 3, "a"); p.row(7, 9, 11, "a")
    p.row(8, 0, 1, "a"); p.row(8, 11, 12, "a")
    p.put(0, 9, "a"); p.put(12, 9, "a")
    p.col(6, 0, 4, "h")
    for y in (0, 2, 4):
        p.row(y, 5, 7, "a")
    p.put(6, 4, "a")
    p.row(-1, 5, 7, "a"); p.put(6, -2, "k")
    m.sprite(p.rows(), {
        "e": D(edge, 7.5, 8.5), "b": D(body, 7.4, 8.6), "d": D(shade, 7.5, 8.5),
        "n": D(shade, 7.7, 8.3), "k": D(star, 7.2, 8.8), "c": D(silver, 7.2, 8.8), "a": D(silver, 6.9, 9.1),
        "h": D(wrap, 7.3, 8.7),
    }, at=p.at(), depth=(7.5, 8.5))
    gem(m, moonstone, cy=6, s=1.0, d=1.5)
    return m


def build():
    return [frost(), blood(), emerald(), amethyst(), solar(), abyss(), sakura(), nature(), thunder(), lunar()]
