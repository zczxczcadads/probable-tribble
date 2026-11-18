"""Облики кирок. Модель стоит вертикально: рукоять внизу (центр хвата около y=1.5), головка вверху."""
from kit import Mat, Model


def _sprite(m, head, shaft, key, depth=(7.2, 8.8)):
    """Левая половина головки зеркалится; рукоять задаётся строками, прижатыми к центру.
    Рисунок 28 строк: 12 строк головки и 16 строк рукояти, от y=-3 до y=25."""
    rows = []
    for r in head:
        r = r.ljust(8, ".")
        rows.append(r + r[::-1])
    for s in shaft:
        r = s.rjust(8, ".")
        rows.append(r + r[::-1])
    assert len(rows) == 28, len(rows)
    m.sprite(rows, key, at=(0, -3), depth=depth)


def _d(mat, z0, z1):
    return {"mat": mat, "depth": (z0, z1)}


def _shard(m, cx, y0, y1, w, mat, ang, z=(7.3, 8.7), mirror=True):
    """Остриё-кристалл: коробка, повёрнутая вокруг основания (cx, y0)."""
    zc = (z[0] + z[1]) / 2
    m.box((cx - w / 2, y0, z[0]), (cx + w / 2, y1, z[1]), mat, rot=("z", ang, (cx, y0, zc)), mirror=mirror)


def _gem(m, cx, cy, s, mat, z0, z1, ang=45):
    """Ромб-самоцвет, повёрнутый на 45°."""
    h = s / 2
    zc = (z0 + z1) / 2
    m.box((cx - h, cy - h, z0), (cx + h, cy + h, z1), mat, rot=("z", ang, (cx, cy, zc)))


def crystal():
    m = Model("pickaxe_crystal", "Кристальная кирка", "pickaxe")
    shard = Mat("crystal", "#0f6e7a", "#25b7c4", "#8ff0f0", "#effffd")
    dark = Mat("crystal", "#073f4d", "#0f6e7a", "#25b7c4")
    light = Mat("crystal", "#25b7c4", "#8ff0f0", "#effffd", "#ffffff")
    core = Mat("flat", "#b6fff6", "#ffffff", glow=True)
    wood = Mat("wood", "#3a2618", "#5c3d26", "#7d5636")
    gold = Mat("metal", "#6b4a12", "#b8862b", "#f0c95a", "#fff3b8", edge="bevel")
    head = [
        "..llllll",
        ".llssscc",
        "lssdddcc",
        "lsd..ggg",
        "lsd..GGg",
        "ld...ggg",
        "d....ggh",
        "d......h",
        "......hh",
        ".......h",
        ".......h",
        ".......h",
    ]
    shaft = ["h", "h", "h", "gg", "h", "h", "h", "h", "h", "h", "h", "h", "h", "h", "gg", "g"]
    _sprite(m, head, shaft, {
        "s": _d(shard, 6.7, 9.3), "l": _d(light, 6.4, 9.6), "d": _d(dark, 7.2, 8.8),
        "c": _d(core, 6.6, 9.4), "g": _d(gold, 6.6, 9.4), "G": _d(gold, 6.3, 9.7),
        "h": _d(wood, 7.3, 8.7),
    })
    _gem(m, 8, 18.5, 2, core, 9.4, 9.9)
    _gem(m, 8, 18.5, 2, core, 6.1, 6.6)
    # кристальные шипы по хребту головки
    _shard(m, 4.5, 24.0, 27.0, 1.5, shard, 22.5, z=(7.5, 8.5))
    _shard(m, 2.5, 22.5, 25.0, 1.0, shard, 45, z=(7.6, 8.4))
    _shard(m, 8.0, 25.0, 28.0, 1.5, shard, 0, z=(7.5, 8.5), mirror=False)
    return m


def magma():
    m = Model("pickaxe_magma", "Магмовая кирка", "pickaxe")
    rock = Mat("stone", "#1a1416", "#3a2e31", "#5e4b4e", "#8a7276")
    rock2 = Mat("stone", "#241a1d", "#4a3a3d", "#74605f")
    lava = Mat("glow", "#ff4a10", "#ff8a1f", "#ffd34d", glow=True)
    yel = Mat("flat", "#ffd34d", "#fff2a0", glow=True)
    char = Mat("wood", "#0f0907", "#211510", "#3b2519")
    ember = Mat("glow", "#ff3a0a", "#ff7a1a", "#ffc04a", glow=True)
    iron = Mat("metal", "#1c1618", "#403639", "#7a6d70", "#aa9ea0", edge="bevel")
    head = [
        "..bbbBbb",
        ".bBbllbb",
        "bbblyblb",
        "bBlybbyb",
        "bbllbbbb",
        "bbb.bkkk",
        "bb...kkk",
        "b....kkk",
        "b.....kh",
        "......hh",
        ".......h",
        ".......h",
    ]
    shaft = ["h", "h", "ee", "h", "h", "ee", "h", "h", "h", "ee", "h", "h", "h", "h", "kk", "k"]
    _sprite(m, head, shaft, {
        "b": _d(rock, 6.3, 9.7), "B": _d(rock2, 6.0, 10.0), "l": _d(lava, 6.8, 9.2),
        "y": _d(yel, 6.8, 9.2), "k": _d(iron, 6.7, 9.3),
        "h": _d(char, 7.3, 8.7), "e": _d(ember, 7.0, 9.0),
    })
    # глыбы застывшей лавы на гребне и сердце-самоцвет на оправе
    _shard(m, 4.0, 25.0, 27.5, 2.0, rock2, 22.5, z=(7.2, 8.8))
    _shard(m, 8.0, 25.0, 28.0, 2.0, rock2, 0, z=(7.0, 9.0), mirror=False)
    _gem(m, 8, 18.5, 2.5, lava, 9.3, 9.9)
    _gem(m, 8, 18.5, 2.5, lava, 6.1, 6.7)
    m.box((7, -4, 7), (9, -3, 9), ember)
    return m


def royal():
    m = Model("pickaxe_royal", "Королевская кирка", "pickaxe")
    gold = Mat("metal", "#6b4a12", "#b8862b", "#f0c95a", "#fff3b8", edge="bevel")
    gold2 = Mat("metal", "#4a3208", "#8a6a1b", "#d9aa3a", edge="dark")
    ruby = Mat("gem", "#5a0614", "#c8102e", "#ff5a6e", "#ffc0c8", glow=True)
    wrap = Mat("wrap", "#24103f", "#4a2584", "#7d4ccc", "#b58cf0")
    head = [
        ".....g.g",
        "....gggg",
        "..gggbbg",
        ".ggbddgr",
        "ggbd.gGr",
        "gb...gGG",
        "gd...ggw",
        "g....ggw",
        "g.....ww",
        "......ww",
        "......ww",
        "......ww",
    ]
    shaft = ["w", "w", "w", "gg", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "gg", "g"]
    _sprite(m, head, shaft, {
        "g": _d(gold, 6.7, 9.3), "b": _d(gold, 6.4, 9.6), "d": _d(gold2, 7.0, 9.0),
        "G": _d(gold, 6.4, 9.6), "r": _d(ruby, 6.3, 9.7), "w": _d(wrap, 7.2, 8.8),
    })
    # шарики-рубины на зубцах короны и крупный рубин на оправе
    _gem(m, 5.5, 25.5, 1.0, ruby, 7.5, 8.5)
    _gem(m, 10.5, 25.5, 1.0, ruby, 7.5, 8.5)
    _gem(m, 8, 25.5, 1.0, ruby, 7.5, 8.5)
    _gem(m, 8, 19, 2.0, ruby, 9.4, 9.9)
    _gem(m, 8, 19, 2.0, ruby, 6.1, 6.6)
    m.box((7, -4, 7), (9, -3, 9), gold)
    return m




def bone():
    m = Model("pickaxe_bone", "Костяная кирка", "pickaxe")
    bone = Mat("bone", "#6e6048", "#b8aa8a", "#e6dcc0", "#fbf6e4")
    dark = Mat("bone", "#3e3426", "#7a6b52", "#b8aa8a")
    eye = Mat("glow", "#38d060", "#9dff7a", "#e8ffd8", glow=True)
    skull = Mat("bone", "#7a6c52", "#c4b694", "#ece2c6", "#fbf6e4", edge="bevel")
    head = [
        "...BBBBB",
        ".BBbbbbb",
        "BBb.rrrr",
        "Bb.rr...",
        "b.rr....",
        "b.r.....",
        "b.......",
        "b.......",
        "........",
        ".......h",
        ".......h",
        ".......h",
    ]
    shaft = ["h", "h", "jj", "h", "h", "h", "h", "h", "h", "h", "h", "h", "jj", "jjj", "jjj", "jj"]
    _sprite(m, head, shaft, {
        "B": _d(bone, 6.5, 9.5), "b": _d(bone, 6.8, 9.2), "r": _d(dark, 7.0, 9.0),
        "j": _d(bone, 6.6, 9.4), "h": _d(bone, 7.3, 8.7),
    })
    # череп на стыке головки и рукояти: глазницы светятся
    art = [
        "..........",
        "..........",
        ".DDD..DDD.",
        ".DDD..DDD.",
        ".DDD..DDD.",
        "..........",
        "....DD....",
        "..........",
        "..........",
        "..........",
    ]
    m.box((5.5, 17.0, 6.8), (10.5, 22.0, 9.4), skull, art={"south": art, "north": art}, key={"D": "#1a1410"})
    m.box((6.5, 16.0, 7.2), (9.5, 17.0, 9.0), dark)
    m.box((6.25, 19.75, 9.4), (7.25, 20.75, 9.7), eye)
    m.box((8.75, 19.75, 9.4), (9.75, 20.75, 9.7), eye)
    m.box((6.25, 19.75, 6.5), (7.25, 20.75, 6.8), eye)
    m.box((8.75, 19.75, 6.5), (9.75, 20.75, 6.8), eye)
    return m




def amethyst():
    m = Model("pickaxe_amethyst", "Аметистовая кирка", "pickaxe")
    am = Mat("crystal", "#3b1670", "#7a3cc4", "#b878f0", "#efd6ff")
    am2 = Mat("crystal", "#24093f", "#5a2a99", "#9a58e0")
    am3 = Mat("crystal", "#6a2cb0", "#a566e8", "#d8a8ff", "#f6e6ff")
    rock = Mat("stone", "#1f1628", "#392d46", "#5c4c70")
    core = Mat("flat", "#e8b8ff", "#ffffff", glow=True)
    wood = Mat("wood", "#2e2036", "#523c60", "#7a5c8a")
    head = [
        "........",
        "........",
        "........",
        ".arrrrrr",
        "aarRRrcc",
        "aaar.rcc",
        "aa..rrrr",
        "a.....rr",
        "a.....rh",
        "......hh",
        ".......h",
        ".......h",
    ]
    shaft = ["h", "h", "h", "aa", "h", "h", "h", "h", "h", "h", "h", "h", "h", "h", "aa", "a"]
    _sprite(m, head, shaft, {
        "a": _d(am, 6.9, 9.1), "R": _d(am2, 6.5, 9.5), "r": _d(rock, 6.6, 9.4),
        "c": _d(core, 6.9, 9.1), "h": _d(wood, 7.3, 8.7),
    })
    # кластеры кристаллов, растущие из камня
    _shard(m, 2.5, 22.0, 27.0, 1.5, am3, 22.5, z=(7.4, 8.6))
    _shard(m, 4.0, 22.0, 26.0, 2.0, am, 0, z=(7.0, 9.0))
    _shard(m, 5.5, 22.0, 25.0, 1.5, am2, -22.5, z=(7.6, 8.4))
    _shard(m, 8.0, 22.0, 28.0, 2.0, am3, 0, z=(7.2, 8.8), mirror=False)
    _shard(m, 7.0, 22.0, 26.0, 1.5, am, 22.5, z=(7.0, 8.2), mirror=False)
    _shard(m, 9.0, 22.0, 26.0, 1.5, am, -22.5, z=(7.8, 9.0), mirror=False)
    _gem(m, 8, 19, 2.5, core, 9.4, 9.9)
    _gem(m, 8, 19, 2.5, core, 6.1, 6.6)
    _gem(m, 8, -3.5, 2.5, am3, 7.2, 8.8)
    return m


def forest():
    m = Model("pickaxe_forest", "Кирка леса", "pickaxe")
    bark = Mat("wood", "#3a2412", "#6b4a2e", "#9a7448")
    lite = Mat("wood", "#8a6a3e", "#c4a060", "#ecd29a")
    leaf = Mat("cloth", "#1f6b22", "#3fb040", "#8aec5a")
    leaf2 = Mat("cloth", "#15501a", "#2a8a30", "#5ac040")
    moss = Mat("fur", "#2f5a1a", "#4f8a2a", "#8acf4a")
    cap = Mat("cloth", "#8a1010", "#d02828", "#ff6a5a")
    cream = Mat("flat", "#e8dcc0", "#fff4dc")
    pink = Mat("glow", "#e0507a", "#ff90b0", "#fff0f4", glow=True)
    head = [
        "..lLl.ll",
        ".lwwwlww",
        "wwbwwbbw",
        "wbbbwbbb",
        "Wb.wbbbb",
        "W...bbbb",
        "W....bbb",
        ".....mmb",
        ".......b",
        ".......b",
        ".......b",
        ".......b",
    ]
    shaft = ["b", "b", "v", "b", "v", "b", "b", "v", "b", "v", "b", "b", "b", "m", "mm", "b"]
    _sprite(m, head, shaft, {
        "w": _d(bark, 6.5, 9.5), "b": _d(bark, 6.9, 9.1), "W": _d(lite, 7.1, 8.9),
        "l": _d(leaf, 6.3, 9.7), "L": _d(leaf2, 6.1, 9.9), "m": _d(moss, 6.4, 9.6),
        "v": _d(leaf2, 6.8, 9.2),
    })
    # грибок на гребне и цветок на рукояти
    m.box((7.5, 25.0, 7.5), (8.5, 26.5, 8.5), cream)
    m.box((6.5, 26.5, 6.7), (9.5, 27.5, 9.3), cap)
    m.box((7.0, 27.5, 7.2), (9.0, 28.0, 8.8), cap)
    m.box((9.0, 9.5, 7.7), (9.5, 12.8, 8.3), leaf2)
    _gem(m, 10.0, 13.0, 1.5, pink, 7.6, 8.4)
    _gem(m, 6.0, 13.0, 1.5, leaf, 7.6, 8.4)
    return m


def _drill_head():
    """Корпус-шестерёнка по центру и ступенчатые свёрла по бокам (клетки светлые/тёмные — витки)."""
    cone = {5: (0, 7), 4: (1, 7), 3: (3, 8), 2: (4, 8), 1: (5, 9), 0: (7, 9)}
    rows = []
    for r in range(12):
        s = ""
        for c in range(8):
            if c >= 6 and r <= 6:
                s += "H"
            elif c in cone and cone[c][0] <= r <= cone[c][1]:
                s += "S" if ((r + c) // 2) % 2 == 0 else "d"
            elif r == 7 and c >= 6:
                s += "k"
            elif c == 7 and r > 7:
                s += "h"
            else:
                s += "."
        rows.append(s)
    return rows


def drill():
    m = Model("pickaxe_drill", "Бур", "pickaxe")
    steel = Mat("metal", "#2c3440", "#5a6676", "#98a6b8", "#d2dcea", edge="bevel")
    steel2 = Mat("metal", "#1c222c", "#3c4654", "#6a788a", edge="dark")
    grip = Mat("metal", "#3c4654", "#6a788a", "#98a6b8", "#c8d4e2")
    copper = Mat("metal", "#5a2a14", "#b4642c", "#e89a58", "#ffd0a0")
    yel = Mat("flat", "#e8b800", "#ffd400")
    blk = Mat("flat", "#14141a", "#24242c")
    led = Mat("glow", "#22d060", "#7dff9a", "#e0ffe8", glow=True)
    red = Mat("glow", "#d01818", "#ff5050", "#ffb0b0", glow=True)
    shaft = ["h", "h", "h", "h", "h", "h", "yy", "kk", "yy", "kk", "h", "h", "h", "h", "cc", "c"]
    _sprite(m, _drill_head(), shaft, {
        "S": _d(steel, 6.4, 9.6), "d": _d(steel2, 6.9, 9.1), "H": _d(steel, 6.4, 9.6),
        "c": _d(copper, 7.0, 9.0), "k": _d(blk, 6.7, 9.3), "y": _d(yel, 6.9, 9.1),
        "h": _d(grip, 7.3, 8.7),
    })
    # шестерня на корпусе, медные трубы и индикаторы
    gear = steel2
    for z0, z1 in ((9.6, 10.2), (5.8, 6.4)):
        m.box((6.5, 20.0, z0), (9.5, 23.0, z1), gear)
        m.box((6.5, 20.0, z0), (9.5, 23.0, z1), gear, rot=("z", 45, (8, 21.5, (z0 + z1) / 2)))
    m.box((7.25, 20.75, 10.2), (8.75, 22.25, 10.6), led)
    m.box((9.0, 9.5, 7.6), (9.9, 17.0, 8.4), copper)
    m.box((6.1, 9.5, 7.6), (7.0, 17.0, 8.4), copper)
    m.box((9.0, 9.0, 7.7), (9.9, 9.5, 8.3), red)
    m.box((6.1, 9.0, 7.7), (7.0, 9.5, 8.3), red)
    m.box((7.25, 17.25, 9.3), (8.75, 17.75, 9.6), led)
    return m


def frost():
    m = Model("pickaxe_frost", "Ледоруб", "pickaxe")
    ice = Mat("crystal", "#2a6fa8", "#5ab4e8", "#a8e4ff", "#f0fbff")
    ice2 = Mat("crystal", "#1a4a7a", "#3a8acc", "#7acaf0")
    snow = Mat("fur", "#b8d0e0", "#e4f0f8", "#ffffff")
    core = Mat("flat", "#b0f4ff", "#ffffff", glow=True)
    wood = Mat("wood", "#26324c", "#46608c", "#86a6d4")
    head = [
        "....wwww",
        "..wwiiww",
        ".wiiIiic",
        "wiiI.iic",
        "iiI....c",
        "iI.....c",
        "i......h",
        "i.....gh",
        "......gh",
        ".......h",
        ".......h",
        ".......h",
    ]
    shaft = ["h", "h", "f", "h", "h", "f", "h", "h", "h", "h", "h", "h", "h", "h", "ff", "f"]
    _sprite(m, head, shaft, {
        "i": _d(ice, 6.7, 9.3), "I": _d(ice2, 6.4, 9.6), "w": _d(snow, 6.3, 9.7),
        "c": _d(core, 6.9, 9.1), "h": _d(wood, 7.3, 8.7), "f": _d(snow, 7.0, 9.0),
        "g": _d(ice2, 6.8, 9.2),
    })
    # сосульки под головкой и шапки снега
    for x, top, tip in ((3.0, 21.0, 17.5), (5.0, 21.0, 16.5)):
        m.box((x, tip + 2.0, 7.5), (x + 1.0, top, 8.5), ice, mirror=True)
        m.box((x + 0.25, tip, 7.75), (x + 0.75, tip + 2.0, 8.25), ice, mirror=True)
    m.box((3.5, 25.0, 7.2), (5.5, 26.0, 8.8), snow, mirror=True)
    m.box((7.0, 25.0, 7.0), (9.0, 26.5, 9.0), snow)
    _gem(m, 8, 19.0, 2.5, core, 9.4, 9.9)
    _gem(m, 8, 19.0, 2.5, core, 6.1, 6.6)
    return m


def ender():
    m = Model("pickaxe_ender", "Кирка Края", "pickaxe")
    obs = Mat("stone", "#0e0720", "#1e0f38", "#3a1f66", "#6a3ab0")
    obs2 = Mat("stone", "#160a2c", "#2a1650", "#4e2c8a")
    eyeg = Mat("glow", "#18a888", "#3de8c0", "#a8ffe8", glow=True)
    pupil = Mat("flat", "#052a26", "#0a4a40")
    part = Mat("glow", "#a040e8", "#d070ff", "#f0b8ff", glow=True)
    wood = Mat("wood", "#150f26", "#2c2248", "#4a3c74")
    head = [
        "..oooooo",
        ".ooOooee",
        "ooOooeEE",
        "oooooeEq",
        "oooooeEq",
        "oo.ooeEE",
        "o...ooee",
        "o...oooh",
        "......hh",
        ".......h",
        ".......h",
        ".......h",
    ]
    shaft = ["h", "h", "h", "pp", "h", "h", "h", "h", "h", "h", "h", "h", "h", "h", "pp", "p"]
    _sprite(m, head, shaft, {
        "o": _d(obs, 6.5, 9.5), "O": _d(obs2, 6.2, 9.8), "e": _d(eyeg, 6.4, 9.6),
        "E": _d(eyeg, 6.6, 9.4), "q": _d(pupil, 6.3, 9.7), "p": _d(part, 7.0, 9.0),
        "h": _d(wood, 7.3, 8.7),
    })
    # осколки обсидиана и частицы портала
    _shard(m, 3.0, 25.0, 28.5, 2.0, obs2, 22.5, z=(7.2, 8.8))
    _shard(m, 5.5, 25.0, 27.5, 1.5, obs, -22.5, z=(7.4, 8.6))
    _shard(m, 1.5, 17.0, 19.0, 1.5, obs2, 45, z=(7.4, 8.6))
    for x, y, z in ((1.0, 27.0, 7.5), (14.0, 26.0, 8.0), (14.5, 14.0, 7.8), (2.0, 14.0, 8.4), (9.5, 29.5, 8.0)):
        _gem(m, x, y, 0.8, part, z - 0.4, z + 0.4)
    return m


def star():
    m = Model("pickaxe_star", "Звёздная кирка", "pickaxe")
    night = Mat("metal", "#0a1230", "#16275a", "#2a448c", "#5a7ad0")
    night2 = Mat("metal", "#060a1e", "#0e1840", "#1c2e6a", edge="dark")
    gold = Mat("metal", "#6b4a12", "#b8862b", "#f0c95a", "#fff3b8", edge="bevel")
    glow = Mat("flat", "#ffc830", "#fff0a0", glow=True)
    wood = Mat("wood", "#0f1634", "#1c2a58", "#32478a")
    head = [
        "..gggggg",
        ".gnnnnnn",
        "gnnnnnnn",
        "gnnNnNNN",
        "gnN.....",
        "gn......",
        "gn......",
        "n...gggg",
        "n....ggh",
        ".......h",
        ".......h",
        ".......h",
    ]
    shaft = ["h", "h", "g", "h", "h", "h", "h", "h", "h", "h", "h", "h", "h", "h", "gg", "g"]
    _sprite(m, head, shaft, {
        "n": _d(night, 6.7, 9.3), "N": _d(night2, 7.0, 9.0), "g": _d(gold, 6.5, 9.5),
        "h": _d(wood, 7.3, 8.7),
    })
    # светящаяся звезда в чаше полумесяца и золотые искры
    m.box((6.5, 18.5, 7.3), (9.5, 21.5, 8.7), glow)
    m.box((6.5, 18.5, 7.3), (9.5, 21.5, 8.7), glow, rot=("z", 45, (8, 20, 8)))
    m.box((7.7, 17.5, 7.7), (8.3, 22.5, 8.3), glow)
    m.box((5.5, 19.7, 7.75), (10.5, 20.3, 8.25), glow)
    for x, y in ((3.5, 23.0), (5.0, 20.0)):
        for z0 in (9.3, 6.4):
            m.box((x - 0.25, y - 1.0, z0), (x + 0.25, y + 1.0, z0 + 0.3), gold, mirror=True)
            m.box((x - 1.0, y - 0.25, z0 + 0.05), (x + 1.0, y + 0.25, z0 + 0.25), gold, mirror=True)
    return m


def build():
    return [crystal(), magma(), royal(), bone(), amethyst(), forest(), drill(), frost(), ender(), star()]
