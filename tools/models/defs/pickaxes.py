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
    _shard(m, 4.5, 24.0, 27.0, 1.5, light, 22.5, z=(7.5, 8.5))
    _shard(m, 2.5, 22.5, 25.0, 1.0, shard, 45, z=(7.6, 8.4))
    _shard(m, 8.0, 25.0, 28.0, 1.5, light, 0, z=(7.5, 8.5), mirror=False)
    return m


def magma():
    m = Model("pickaxe_magma", "Магмовая кирка", "pickaxe")
    rock = Mat("stone", "#120d10", "#2b2226", "#4a3a3c", "#6a5558")
    rock2 = Mat("stone", "#1c1417", "#3a2c2f", "#5c494b")
    lava = Mat("glow", "#ff4a10", "#ff8a1f", "#ffd34d", glow=True)
    yel = Mat("flat", "#ffd34d", "#fff2a0", glow=True)
    char = Mat("wood", "#0f0907", "#211510", "#3b2519")
    ember = Mat("glow", "#ff3a0a", "#ff7a1a", "#ffc04a", glow=True)
    iron = Mat("metal", "#1c1618", "#403639", "#7a6d70", "#aa9ea0", edge="bevel")
    head = [
        "..bbbBbb",
        ".bBbblbb",
        "bbbblbyb",
        "bBblybbb",
        "bblbbbbb",
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
        "b": _d(rock, 6.5, 9.5), "B": _d(rock2, 6.2, 9.8), "l": _d(lava, 6.9, 9.1),
        "y": _d(yel, 6.9, 9.1), "k": _d(iron, 6.7, 9.3),
        "h": _d(char, 7.3, 8.7), "e": _d(ember, 7.0, 9.0),
    })
    # глыбы застывшей лавы на гребне и сердце-самоцвет на оправе
    _shard(m, 3.5, 24.5, 28.0, 2.5, rock2, 22.5, z=(7.0, 9.0))
    _shard(m, 6.0, 25.0, 27.5, 2.0, rock, -22.5, z=(7.3, 8.7))
    _shard(m, 8.0, 25.0, 29.0, 2.0, rock2, 0, z=(7.0, 9.0), mirror=False)
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
        "j": _d(dark, 6.7, 9.3), "h": _d(bone, 7.3, 8.7),
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
    return m


def amethyst():
    m = Model("pickaxe_amethyst", "Аметистовая кирка", "pickaxe")
    am = Mat("crystal", "#3b1670", "#7a3cc4", "#b878f0", "#efd6ff")
    am2 = Mat("crystal", "#24093f", "#5a2a99", "#9a58e0")
    am3 = Mat("crystal", "#6a2cb0", "#a566e8", "#d8a8ff", "#f6e6ff")
    rock = Mat("stone", "#1a1320", "#2f2638", "#4a3e58")
    core = Mat("flat", "#e8b8ff", "#ffffff", glow=True)
    wood = Mat("wood", "#2a1c2e", "#4a3350", "#6b4f72")
    head = [
        "........",
        "........",
        "........",
        "..rrrrrr",
        ".rrRRrcc",
        "aarr.rcc",
        "aa..rrrr",
        "a.....rr",
        "a.....rh",
        "......hh",
        ".......h",
        ".......h",
    ]
    shaft = ["h", "h", "h", "rr", "h", "h", "h", "h", "h", "h", "h", "h", "h", "h", "rr", "r"]
    _sprite(m, head, shaft, {
        "a": _d(am, 6.9, 9.1), "R": _d(am2, 6.5, 9.5), "r": _d(rock, 6.6, 9.4),
        "c": _d(core, 6.9, 9.1), "h": _d(wood, 7.3, 8.7),
    })
    # кластеры кристаллов, растущие из камня
    _shard(m, 2.5, 22.0, 27.0, 1.5, am3, 22.5, z=(7.4, 8.6))
    _shard(m, 4.0, 22.0, 26.0, 2.0, am, 0, z=(7.0, 9.0))
    _shard(m, 5.5, 22.0, 25.0, 1.5, am2, -22.5, z=(7.6, 8.4))
    _shard(m, 1.5, 21.0, 24.0, 1.5, am2, 45, z=(7.8, 8.8))
    _shard(m, 8.0, 22.0, 28.0, 2.0, am3, 0, z=(7.2, 8.8), mirror=False)
    _shard(m, 7.0, 22.0, 26.0, 1.5, am, 22.5, z=(7.0, 8.2), mirror=False)
    _shard(m, 9.0, 22.0, 26.0, 1.5, am, -22.5, z=(7.8, 9.0), mirror=False)
    _gem(m, 8, 19, 2.5, core, 9.4, 9.9)
    _gem(m, 8, 19, 2.5, core, 6.1, 6.6)
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
        "..l..lll",
        ".lwwlwww",
        "wwbwwbbw",
        "wbbbmmbb",
        "Wb.bbbbb",
        "W....bbb",
        "W.....bb",
        "......bb",
        ".......b",
        ".......b",
        ".......b",
        ".......b",
    ]
    shaft = ["b", "b", "v", "b", "v", "b", "b", "v", "b", "v", "b", "b", "b", "b", "bb", "b"]
    _sprite(m, head, shaft, {
        "w": _d(bark, 6.7, 9.3), "b": _d(bark, 7.0, 9.0), "W": _d(lite, 7.1, 8.9),
        "l": _d(leaf, 6.4, 9.6), "m": _d(moss, 6.4, 9.6), "v": _d(leaf2, 6.8, 9.2),
    })
    # листья, грибок и цветок
    _shard(m, 3.0, 24.0, 27.0, 2.0, leaf, 45, z=(7.2, 8.8))
    _shard(m, 5.0, 24.5, 27.0, 1.5, leaf2, 22.5, z=(7.5, 8.5))
    _shard(m, 1.5, 17.0, 20.0, 1.5, leaf, 45, z=(7.5, 8.5))
    m.box((7.5, 25.0, 7.5), (8.5, 26.5, 8.5), cream)
    m.box((6.5, 26.5, 6.7), (9.5, 27.5, 9.3), cap)
    m.box((7.0, 27.5, 7.2), (9.0, 28.0, 8.8), cap)
    _gem(m, 10.5, 9.5, 1.5, pink, 9.0, 9.7)
    return m


def drill():
    m = Model("pickaxe_drill", "Бур", "pickaxe")
    steel = Mat("metal", "#2c3440", "#5a6676", "#98a6b8", "#d2dcea", edge="bevel")
    steel2 = Mat("metal", "#1c222c", "#3c4654", "#6a788a", edge="dark")
    copper = Mat("metal", "#5a2a14", "#b4642c", "#e89a58", "#ffd0a0")
    yel = Mat("flat", "#e8b800", "#ffd400")
    blk = Mat("flat", "#14141a", "#24242c")
    led = Mat("glow", "#22d060", "#7dff9a", "#e0ffe8", glow=True)
    red = Mat("glow", "#d01818", "#ff5050", "#ffb0b0", glow=True)
    head = [
        "..sssSSS",
        ".ssSsddd",
        "ssSsdkkk",
        "dssdkkkk",
        "sd..kkkk",
        "d...kkkk",
        "s....kkk",
        "......kh",
        "......hh",
        ".......h",
        ".......h",
        ".......h",
    ]
    shaft = ["h", "h", "yy", "kk", "yy", "kk", "h", "h", "h", "h", "h", "h", "h", "h", "cc", "c"]
    _sprite(m, head, shaft, {
        "s": _d(steel, 6.6, 9.4), "S": _d(steel, 6.3, 9.7), "d": _d(steel2, 7.0, 9.0),
        "c": _d(copper, 7.0, 9.0), "k": _d(blk, 6.9, 9.1), "y": _d(yel, 6.9, 9.1),
        "h": _d(steel2, 7.3, 8.7),
    })
    # шестерня на оправе, медные трубы и индикатор
    gear = steel2
    m.box((6.0, 18.0, 9.1), (10.0, 22.0, 9.7), gear)
    m.box((6.0, 18.0, 9.1), (10.0, 22.0, 9.7), gear, rot=("z", 45, (8, 20, 9.4)))
    m.box((7.0, 19.0, 9.7), (9.0, 21.0, 10.1), led)
    m.box((6.0, 18.0, 5.9), (10.0, 22.0, 6.5), gear)
    m.box((6.0, 18.0, 5.9), (10.0, 22.0, 6.5), gear, rot=("z", 45, (8, 20, 6.2)))
    m.box((9.0, -1.0, 7.6), (10.0, 15.5, 8.4), copper)
    m.box((9.0, 15.5, 7.6), (13.0, 16.5, 8.4), copper)
    m.box((12.5, 16.5, 7.6), (13.5, 19.0, 8.4), copper)
    m.box((12.8, 12.0, 7.7), (13.3, 12.6, 8.3), red)
    m.box((7.0, 15.0, 8.8), (9.0, 16.0, 9.2), led)
    return m


def frost():
    m = Model("pickaxe_frost", "Ледоруб", "pickaxe")
    ice = Mat("crystal", "#2a6fa8", "#5ab4e8", "#a8e4ff", "#f0fbff")
    ice2 = Mat("crystal", "#1a4a7a", "#3a8acc", "#7acaf0")
    snow = Mat("fur", "#b8d0e0", "#e4f0f8", "#ffffff")
    core = Mat("flat", "#b0f4ff", "#ffffff", glow=True)
    wood = Mat("wood", "#3a3c4a", "#5a6076", "#8a94b0")
    head = [
        "..wwwwww",
        ".wiiwiww",
        "wiiIiiic",
        "iIi.iiic",
        "ii...i.c",
        "i.......",
        "i.....gh",
        "......gh",
        "......hh",
        ".......h",
        ".......h",
        ".......h",
    ]
    shaft = ["h", "h", "f", "h", "h", "f", "h", "h", "h", "h", "h", "h", "h", "h", "ff", "f"]
    _sprite(m, head, shaft, {
        "i": _d(ice, 6.8, 9.2), "I": _d(ice2, 6.5, 9.5), "w": _d(snow, 6.4, 9.6),
        "c": _d(core, 6.8, 9.2), "h": _d(wood, 7.3, 8.7), "f": _d(snow, 7.0, 9.0),
        "g": _d(ice2, 6.8, 9.2),
    })
    # сосульки под головкой
    for x, y0 in ((2.0, 18.0), (4.0, 17.0), (6.0, 19.0)):
        m.box((x, y0 + 1.5, 7.5), (x + 1.0, 21.0, 8.5), ice, mirror=True)
        m.box((x + 0.25, y0, 7.75), (x + 0.75, y0 + 1.5, 8.25), ice, mirror=True)
    _gem(m, 8, 18.5, 2.5, core, 9.4, 9.9)
    _gem(m, 8, 18.5, 2.5, core, 6.1, 6.6)
    return m


def ender():
    m = Model("pickaxe_ender", "Кирка Края", "pickaxe")
    obs = Mat("stone", "#07040e", "#150b24", "#2a1648", "#4b2a7a")
    obs2 = Mat("stone", "#0d0618", "#1f1038", "#3a2266")
    eyeg = Mat("glow", "#18a888", "#3de8c0", "#a8ffe8", glow=True)
    pupil = Mat("flat", "#052a26", "#0a4a40")
    part = Mat("glow", "#a040e8", "#d070ff", "#f0b8ff", glow=True)
    wood = Mat("wood", "#0d0a16", "#201a34", "#3a3058")
    head = [
        "..oooooo",
        ".oOooeee",
        "oOooeEEE",
        "ooo.eEqq",
        "oo..eEqq",
        "o...eEEE",
        "o....eee",
        ".......h",
        "......hh",
        ".......h",
        ".......h",
        ".......h",
    ]
    shaft = ["h", "h", "h", "pp", "h", "h", "h", "h", "h", "h", "h", "h", "h", "h", "pp", "p"]
    _sprite(m, head, shaft, {
        "o": _d(obs, 6.6, 9.4), "O": _d(obs2, 6.3, 9.7), "e": _d(eyeg, 6.5, 9.5),
        "E": _d(eyeg, 6.7, 9.3), "q": _d(pupil, 6.4, 9.6), "p": _d(part, 7.0, 9.0),
        "h": _d(wood, 7.3, 8.7),
    })
    # осколки обсидиана и частицы портала
    _shard(m, 3.0, 24.0, 27.5, 2.0, obs2, 22.5, z=(7.2, 8.8))
    _shard(m, 5.5, 24.5, 27.0, 1.5, obs, -22.5, z=(7.4, 8.6))
    for x, y, z in ((1.5, 26.5, 7.5), (13.5, 26.0, 8.0), (14.5, 14.5, 7.8), (3.0, 14.0, 8.4), (9.5, 29.0, 8.0)):
        _gem(m, x, y, 0.8, part, z - 0.4, z + 0.4)
    return m


def star():
    m = Model("pickaxe_star", "Звёздная кирка", "pickaxe")
    night = Mat("metal", "#0a1230", "#16275a", "#2a448c", "#5a7ad0")
    night2 = Mat("metal", "#060a1e", "#0e1840", "#1c2e6a", edge="dark")
    gold = Mat("metal", "#6b4a12", "#b8862b", "#f0c95a", "#fff3b8", edge="bevel")
    glow = Mat("flat", "#fff0a0", "#ffffff", glow=True)
    wood = Mat("wood", "#0f1634", "#1c2a58", "#32478a")
    head = [
        "..gggggg",
        ".gnnnnnn",
        "gnnnnNNN",
        "gnnN....",
        "gnN.....",
        "gn......",
        "gn..gggg",
        "n....ggh",
        "n.....hh",
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
    m.box((6.5, 19.5, 7.3), (9.5, 22.5, 8.7), glow)
    m.box((6.5, 19.5, 7.3), (9.5, 22.5, 8.7), glow, rot=("z", 45, (8, 21, 8)))
    for x, y in ((3.5, 23.0), (5.0, 20.0)):
        m.box((x - 0.25, y - 1.0, 9.3), (x + 0.25, y + 1.0, 9.6), gold, mirror=True)
        m.box((x - 1.0, y - 0.25, 9.3), (x + 1.0, y + 0.25, 9.6), gold, mirror=True)
    return m


def build():
    return [crystal(), magma(), royal(), bone(), amethyst(), forest(), drill(), frost(), ender(), star()]
