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
    # самоцвет на оправе
    m.box((7, 17.5, 9.4), (9, 19.5, 9.9), core, rot=("z", 45, (8, 18.5, 9.6)))
    m.box((7, 17.5, 6.1), (9, 19.5, 6.6), core, rot=("z", 45, (8, 18.5, 6.3)))
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
        ".bbBBbbb",
        "bBbbbblb",
        "bbbllbyb",
        "bbbylbbb",
        "bb.bbkkk",
        "bb...kkK",
        "b....kkk",
        "b.....kh",
        "......hh",
        ".......h",
        ".......h",
        ".......h",
    ]
    shaft = ["h", "h", "ee", "h", "h", "ee", "h", "h", "h", "ee", "h", "h", "h", "h", "kk", "k"]
    _sprite(m, head, shaft, {
        "b": _d(rock, 6.5, 9.5), "B": _d(rock2, 6.2, 9.8), "l": _d(lava, 6.9, 9.1),
        "y": _d(yel, 6.9, 9.1), "k": _d(iron, 6.7, 9.3), "K": _d(lava, 6.5, 9.5),
        "h": _d(char, 7.3, 8.7), "e": _d(ember, 7.0, 9.0),
    })
    return m


def royal():
    m = Model("pickaxe_royal", "Королевская кирка", "pickaxe")
    gold = Mat("metal", "#6b4a12", "#b8862b", "#f0c95a", "#fff3b8", edge="bevel")
    gold2 = Mat("metal", "#4a3208", "#8a6a1b", "#d9aa3a", edge="dark")
    ruby = Mat("gem", "#5a0614", "#c8102e", "#ff5a6e", "#ffc0c8", glow=True)
    wrap = Mat("wrap", "#24103f", "#4a2584", "#7d4ccc", "#b58cf0")
    head = [
        ".....g.r",
        "..ggggg.",
        ".ggbbggg",
        "ggbddrgg",
        "gb.gggrg",
        "gd...GGG",
        "g....ggw",
        "g.....ww",
        "......ww",
        "......ww",
        "......ww",
        "......ww",
    ]
    shaft = ["w", "w", "w", "gg", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "gg", "g"]
    _sprite(m, head, shaft, {
        "g": _d(gold, 6.7, 9.3), "b": _d(gold, 6.4, 9.6), "d": _d(gold2, 7.0, 9.0),
        "G": _d(gold, 6.4, 9.6), "r": _d(ruby, 6.3, 9.7), "w": _d(wrap, 7.2, 8.8),
    })
    return m


def bone():
    m = Model("pickaxe_bone", "Костяная кирка", "pickaxe")
    bone = Mat("bone", "#6e6048", "#b8aa8a", "#e6dcc0", "#fbf6e4")
    dark = Mat("bone", "#3e3426", "#7a6b52", "#b8aa8a")
    eye = Mat("glow", "#38d060", "#9dff7a", "#e8ffd8", glow=True)
    nose = Mat("flat", "#1a1410")
    head = [
        "...bbbbb",
        ".bbBBBBb",
        "bBb.....",
        "bb....bb",
        "b....bbb",
        "d...bebb",
        "d...bbnn",
        "......tT",
        "......jj",
        ".......h",
        ".......h",
        ".......h",
    ]
    shaft = ["h", "h", "jj", "h", "h", "h", "h", "h", "h", "h", "h", "h", "jj", "jj", "jj", "j"]
    _sprite(m, head, shaft, {
        "b": _d(bone, 6.8, 9.2), "B": _d(bone, 6.5, 9.5), "d": _d(dark, 7.0, 9.0),
        "e": _d(eye, 6.6, 9.4), "n": _d(nose, 7.0, 9.0), "t": _d(bone, 6.9, 9.1),
        "T": _d(dark, 6.9, 9.1), "j": _d(dark, 6.7, 9.3), "h": _d(bone, 7.3, 8.7),
    })
    return m


def amethyst():
    m = Model("pickaxe_amethyst", "Аметистовая кирка", "pickaxe")
    am = Mat("crystal", "#3b1670", "#7a3cc4", "#b878f0", "#efd6ff")
    am2 = Mat("crystal", "#24093f", "#5a2a99", "#9a58e0")
    rock = Mat("stone", "#1a1320", "#2f2638", "#4a3e58")
    core = Mat("flat", "#e8b8ff", "#ffffff", glow=True)
    wood = Mat("wood", "#2a1c2e", "#4a3350", "#6b4f72")
    head = [
        ".a...a..",
        ".aa..aa.",
        "aAa.aAaa",
        "aAaaaAaa",
        "aaarrrrr",
        "a.arrccc",
        "a..rrccc",
        "...rrrrh",
        "......hh",
        ".......h",
        ".......h",
        ".......h",
    ]
    shaft = ["h", "h", "h", "rr", "h", "h", "h", "h", "h", "h", "h", "h", "h", "h", "rr", "r"]
    _sprite(m, head, shaft, {
        "a": _d(am, 6.9, 9.1), "A": _d(am2, 6.5, 9.5), "r": _d(rock, 6.6, 9.4),
        "c": _d(core, 6.9, 9.1), "h": _d(wood, 7.3, 8.7),
    })
    return m


def forest():
    m = Model("pickaxe_forest", "Кирка леса", "pickaxe")
    bark = Mat("wood", "#2a1a0e", "#4a3220", "#6b4a2e")
    lite = Mat("wood", "#5a4026", "#8a6a3e", "#b8955a")
    leaf = Mat("cloth", "#1d5a1f", "#2f8f34", "#6fd05a")
    moss = Mat("fur", "#2f5a1a", "#4f8a2a", "#8acf4a")
    head = [
        "..l..lll",
        "..lwwwll",
        ".wbwbwww",
        "wbwmmbbb",
        "wb.bbbbb",
        "Wb....bb",
        "W.....bb",
        "W......b",
        "......bb",
        ".......b",
        ".......b",
        ".......b",
    ]
    shaft = ["b", "b", "v", "b", "v", "b", "b", "v", "b", "v", "b", "b", "b", "b", "bb", "b"]
    _sprite(m, head, shaft, {
        "w": _d(bark, 6.7, 9.3), "b": _d(bark, 7.0, 9.0), "W": _d(lite, 7.1, 8.9),
        "l": _d(leaf, 6.4, 9.6), "m": _d(moss, 6.4, 9.6), "v": _d(leaf, 6.9, 9.1),
    })
    return m


def drill():
    m = Model("pickaxe_drill", "Бур", "pickaxe")
    steel = Mat("metal", "#2c3440", "#5a6676", "#98a6b8", "#d2dcea", edge="bevel")
    steel2 = Mat("metal", "#1c222c", "#3c4654", "#6a788a", edge="dark")
    copper = Mat("metal", "#5a2a14", "#b4642c", "#e89a58", "#ffd0a0")
    yel = Mat("flat", "#e8b800", "#ffd400")
    blk = Mat("flat", "#14141a", "#24242c")
    head = [
        "..ssssss",
        ".ssSSSss",
        "ssSssdss",
        "ssd.....",
        "sd....cc",
        "d.....kk",
        ".....kkh",
        "......hh",
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
        ".wiiiiii",
        "wiIIiiic",
        "iIi.iiic",
        "ii..iicc",
        "i...i.ii",
        "i...i..h",
        ".......h",
        "......hh",
        ".......h",
        ".......h",
        ".......h",
    ]
    shaft = ["h", "h", "f", "h", "h", "f", "h", "h", "h", "h", "h", "h", "h", "h", "ff", "f"]
    _sprite(m, head, shaft, {
        "i": _d(ice, 6.8, 9.2), "I": _d(ice2, 6.5, 9.5), "w": _d(snow, 6.4, 9.6),
        "c": _d(core, 6.8, 9.2), "h": _d(wood, 7.3, 8.7), "f": _d(snow, 7.0, 9.0),
    })
    return m


def ender():
    m = Model("pickaxe_ender", "Кирка Края", "pickaxe")
    obs = Mat("stone", "#07040e", "#150b24", "#2a1648", "#4b2a7a")
    obs2 = Mat("stone", "#0d0618", "#1f1038", "#3a2266")
    eyeg = Mat("glow", "#18a888", "#3de8c0", "#a8ffe8", glow=True)
    part = Mat("glow", "#a040e8", "#d070ff", "#f0b8ff", glow=True)
    wood = Mat("wood", "#0d0a16", "#201a34", "#3a3058")
    head = [
        "..oooooo",
        ".oOooeee",
        "oOooeEEE",
        "ooo.eEpp",
        "oo..eEpp",
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
        "E": _d(eyeg, 6.7, 9.3), "p": _d(part, 7.0, 9.0), "h": _d(wood, 7.3, 8.7),
    })
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
        "gnnNNnnn",
        "gnN..nnn",
        "gn....gg",
        "g.....gG",
        "......gh",
        ".......h",
        "......hh",
        ".......h",
        ".......h",
        ".......h",
    ]
    shaft = ["h", "h", "g", "h", "h", "h", "h", "h", "h", "h", "h", "h", "h", "h", "gg", "g"]
    _sprite(m, head, shaft, {
        "n": _d(night, 6.7, 9.3), "N": _d(night2, 7.0, 9.0), "g": _d(gold, 6.5, 9.5),
        "G": _d(glow, 6.4, 9.6), "h": _d(wood, 7.3, 8.7),
    })
    return m


def build():
    return [crystal(), magma(), royal(), bone(), amethyst(), forest(), drill(), frost(), ender(), star()]
