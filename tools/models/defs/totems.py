"""Облики тотемов: фигурки в кубе 16×16×16, лицом на юг (+Z)."""
from kit import Mat, Model


def spike(m, c, axis, sign, mat, tip_mat):
    """Колючка: основание 1×1 и острый кончик; c — центр основания на грани, axis — куда торчит."""
    for start, length, half, part in ((0.0, 1.2, 0.5, mat), (1.2, 1.0, 0.25, tip_mat)):
        a, b = list(c), list(c)
        for i in range(3):
            if i != axis:
                a[i] -= half
                b[i] += half
        lo, hi = start, start + length
        a[axis] = c[axis] + (lo if sign > 0 else -hi)
        b[axis] = c[axis] + (hi if sign > 0 else -lo)
        m.box(tuple(a), tuple(b), part)


def angel():
    m = Model("totem_angel", "Ангел-хранитель", "totem")
    gold = Mat("metal", "#8a5a12", "#d49a2a", "#ffd95e", "#fff6c2", edge="bevel")
    robe = Mat("band", "#b9c4dc", "#e6ecf7", "#ffffff")
    skin = Mat("flat", "#d9a583", "#f2cfae", "#ffe6cf")
    hair = Mat("fur", "#b8791c", "#f0c14a", "#ffe89a")
    feather = Mat("flat", "#aab8d6", "#e9f0ff", "#ffffff")
    deep = Mat("flat", "#8e9fc4", "#c4d2ec", "#eef3ff")
    tip = Mat("metal", "#b8791c", "#f0c14a", "#ffe89a")
    gem = Mat("gem", "#a82a52", "#e8508a", "#ffa0c0", glow=True)
    halo = Mat("glow", "#e0a81e", "#ffe168", "#fffbd6", glow=True)
    # Постамент, туловище, пояс с камнем и руки.
    m.box((4, 0, 4), (12, 0.5, 12), gold)
    m.box((5, 0.5, 5), (11, 1.5, 11), gold)
    m.box((5.5, 1.5, 6), (10.5, 8, 10), robe, art={"south": [
        "..........", "..........", "....22....", "...2112...", "....22....",
        "..........", "..........", "..........", "..........", "..........", "..........", "..........", ".........."]})
    m.box((5.2, 1.5, 5.7), (10.8, 2.5, 10.3), gold)
    m.box((5.3, 4.2, 5.8), (10.7, 5, 10.2), gold)
    m.box((7.25, 4.1, 10.2), (8.75, 5.1, 10.5), gem)
    m.box((4.5, 4, 7), (5.5, 7.5, 9), robe, mirror=True)
    m.box((4.5, 3.5, 7), (5.5, 4, 9), skin, mirror=True)
    # Голова, чёлка и волосы с боковыми прядями.
    m.box((5.5, 8, 5.5), (10.5, 13, 10.5), skin, key={"e": "#3a2a55", "m": "#c9736a", "w": "#ffffff", "c": "#f2a08e"}, art={"south": [
        "..........", "..........", "..........", "..........",
        ".we....ew.", ".ee....ee.", "c........c", "....mm....", "..........", ".........."]})
    m.box((5.2, 11.6, 5.2), (10.8, 13.4, 10.8), hair)
    m.box((5.2, 9, 5.2), (10.8, 11.6, 6.5), hair)
    m.box((5.0, 9, 6.5), (5.5, 12, 9.5), hair, mirror=True)
    m.box((5.2, 10.8, 10.5), (7, 11.6, 10.9), hair)
    m.box((8, 10.8, 10.5), (9.2, 11.6, 10.9), hair)
    m.box((6.5, 7.2, 5.2), (9.5, 9, 6.0), hair)
    m.disc(8, 8, 3, (14.4, 15), halo, hole=1.9)
    # Крылья: глубокий слой с золотыми кончиками и верхний слой перьев.
    m.sprite([
        "gww        wwg",
        "wwww      wwww",
        "wwwww    wwwww",
        "wwwwww  wwwwww",
        " wwwww  wwwww ",
        " wwwww  wwwww ",
        "  wwww  wwww  ",
        "   ww    ww   ",
        "   g      g   ",
    ], {"w": deep, "g": tip}, at=(1, 3), depth=(4.6, 5.4), side=2)
    m.sprite([
        "ff      ff",
        "fff    fff",
        "ffff  ffff",
        " fff  fff ",
        " fff  fff ",
        "  ff  ff  ",
    ], {"f": feather}, at=(3, 4), depth=(5.4, 6), side=2)
    return m


def demon():
    m = Model("totem_demon", "Демон", "totem")
    stone = Mat("stone", "#0e0c14", "#221e2c", "#3a3446", "#544c64", edge="bevel")
    lava = Mat("glow", "#e0430a", "#ff7a1a", "#ffc23a", "#fff0a0", glow=True)
    red = Mat("flat", "#4a0b10", "#8c1620", "#c42a2a", "#f05a42", edge="bevel")
    dark = Mat("flat", "#0c0508", "#241018", "#3d1822", "#5c2432")
    horn = Mat("metal", "#140a0c", "#2e1a1c", "#6a4838", "#d8c4a0", edge="bevel")
    wing = Mat("cloth", "#2a0610", "#5a0e1c", "#86182a", "#ac2a3a")
    bone = Mat("metal", "#2e1a1c", "#6a4838", "#a88c68", "#d8c4a0")
    eye = Mat("glow", "#ffb000", "#ffe03a", "#fff6a0", glow=True)
    # Постамент с лавовыми трещинами.
    m.box((3.5, 0, 3.5), (12.5, 1.5, 12.5), stone)
    m.box((4.5, 1.5, 4.5), (11.5, 2, 11.5), stone)
    m.box((5, 0.4, 12.5), (7, 1.1, 12.7), lava)
    m.box((8.5, 0.7, 12.5), (11, 1.2, 12.7), lava)
    m.box((12.5, 0.6, 5), (12.7, 1.1, 8), lava)
    m.box((3.3, 0.5, 6), (3.5, 1.0, 9.5), lava)
    # Ноги, туловище, руки.
    m.box((5.5, 2, 6.5), (7.5, 3.5, 10), dark)
    m.box((8.5, 2, 6.5), (10.5, 3.5, 10), dark)
    m.box((5.5, 3.5, 6), (10.5, 7.5, 10), red, key={"b": "#f0a070", "d": "#7a1420"}, art={"south": [
        "..........", "..........", "..........", "...bbbb...",
        "...bddb...", "...bddb...", "...bbbb...", ".........."]})
    m.box((4.5, 4, 7), (5.5, 6.8, 9), red, mirror=True)
    m.box((4.3, 3.4, 6.8), (5.5, 4, 9.2), dark, mirror=True)
    # Голова с жёлтыми глазами и клыками.
    m.box((5, 7.5, 5.5), (11, 12.5, 10.5), red, key={"k": "#140508", "m": "#3a0710", "w": "#fff4d8"}, art={"south": [
        "............", "............", "..kkk..kkk..", "............", "............",
        "............", "....kkkk....", "...mmmmmm...", "...mwmmwm...", "............"]})
    m.box((6, 9.9, 10.5), (7.5, 10.9, 10.7), eye, mirror=True)
    m.box((4.5, 8.5, 7), (5, 10.5, 9.5), red, mirror=True)
    m.box((5.5, 7.5, 5), (10.5, 12, 5.5), dark)
    m.box((6.5, 12.5, 6), (9.5, 13, 9), dark)
    # Изогнутые рога.
    m.box((5.2, 12.5, 6.3), (6.6, 13.5, 7.9), horn, mirror=True)
    m.box((4.4, 13.5, 6.5), (5.8, 14.8, 7.7), horn, mirror=True)
    m.box((4.6, 14.8, 6.7), (5.5, 16, 7.5), bone, mirror=True)
    # Крылья летучей мыши: перепонка и костяные рёбра.
    m.sprite([
        "b.......",
        "bb......",
        "bbbb....",
        "brbbb...",
        "brrbbb..",
        "brrrbbb.",
        "brbrrbbb",
        "brbrbrr.",
        "b.b.b.r.",
        "b...b...",
    ], {"b": {"mat": bone, "depth": (4.2, 5.4)}, "r": {"mat": wing, "depth": (4.6, 5.1)}}, at=(0, 3.5), depth=(4.6, 5.1), side=1)
    m.sprite([
        ".......b",
        "......bb",
        "....bbbb",
        "...bbbrb",
        "..bbbrrb",
        ".bbbrrrb",
        "bbbrrbrb",
        ".rrbrbrb",
        ".r.b.b.b",
        "...b...b",
    ], {"b": {"mat": bone, "depth": (4.2, 5.4)}, "r": {"mat": wing, "depth": (4.6, 5.1)}}, at=(8, 3.5), depth=(4.6, 5.1), side=1)
    # Хвост со стрелкой.
    m.box((7.5, 2.5, 4.5), (8.5, 3.5, 6), red)
    m.box((7.5, 3.5, 3.7), (8.5, 4.5, 4.7), red)
    m.box((7.5, 4.5, 3.2), (8.5, 5.7, 4.2), red)
    m.box((7.3, 5.8, 2.8), (8.7, 7.2, 4.2), horn, rot=("x", 45, (8, 6.5, 3.5)))
    return m


def frost():
    m = Model("totem_frost", "Ледяной дух", "totem")
    ice = Mat("crystal", "#2a68a8", "#5cb0e8", "#9adcff", "#e4fbff", edge="bevel")
    deep = Mat("crystal", "#1c4a88", "#3c88c8", "#78c4f4", "#c8f0ff", edge="bevel")
    snow = Mat("cloth", "#8ea8c8", "#c4d8ee", "#e8f2fc", "#ffffff")
    core = Mat("glow", "#38c8ff", "#8ae8ff", "#d8faff", "#ffffff", glow=True)
    shard = Mat("crystal", "#3a7ad0", "#7cc8ff", "#c0eeff", "#ffffff", glow=True)
    # Снежное основание с ледяными стружками.
    m.box((3.5, 0, 3.5), (12.5, 1.5, 12.5), snow)
    m.box((4.5, 1.5, 4.5), (11.5, 2, 11.5), snow)
    m.box((3, 0.2, 10), (5, 1.2, 12), snow)
    m.box((11.2, 1.5, 9.5), (12.5, 2.8, 11), ice, rot=("z", 22.5, (11.8, 2, 10)))
    m.box((3.8, 1.5, 4), (4.8, 3, 5), ice, rot=("z", -22.5, (4.3, 2, 4.5)))
    # Тело-кристалл, ядро, лицо.
    m.box((6, 2, 6), (10, 5.5, 10), deep)
    m.box((7.25, 2.6, 10), (8.75, 4.2, 10.4), core, rot=("z", 45, (8, 3.4, 10.2)))
    m.box((5, 5.5, 5), (11, 11.5, 11), ice, key={"e": "#2a4a7a", "p": "#f4a0b4", "m": "#2a4a7a"}, art={"south": [
        "............", "............", "............", "............", "............",
        "..eeee..eeee", "............", "..pp....pp..", "....mmmm....", "............", "............", "............"]})
    m.box((4, 6.5, 7), (5, 9.5, 9), deep, mirror=True)
    m.box((4.3, 4.5, 7), (5, 6.5, 9), ice, mirror=True)
    # Ледяная корона из сосулек.
    m.box((7.25, 11.5, 7.25), (8.75, 14.5, 8.75), ice, rot=("y", 45, (8, 12, 8)))
    m.box((6.2, 11.5, 9.4), (7, 13.5, 10.2), ice, mirror=True)
    m.box((5.2, 11.5, 5.2), (6, 13, 6), ice, mirror=True)
    m.box((7, 11.5, 5.2), (9, 13.5, 6), deep)
    m.box((5.3, 11.5, 7.8), (6, 12.8, 8.6), deep, mirror=True)
    # Спина и парящие осколки.
    m.box((7, 3, 4.2), (9, 7.5, 5), deep)
    m.box((7.4, 7.5, 3.6), (8.6, 10.5, 4.4), ice, rot=("x", -22.5, (8, 8.5, 4)))
    m.box((1.5, 6, 6.5), (2.7, 10, 7.5), shard, rot=("z", 22.5, (2, 8, 7)))
    m.box((13.3, 8, 7), (14.5, 12.5, 8), shard, rot=("z", -22.5, (13.9, 10, 7.5)))
    m.box((11.6, 3.8, 11.5), (12.5, 6.3, 12.3), shard, rot=("z", -22.5, (12, 5, 12)))
    m.box((2.2, 2.6, 11), (3.0, 4.6, 11.8), shard, rot=("z", 22.5, (2.6, 3.6, 11.4)))
    m.box((10.5, 11, 3.5), (11.4, 13.5, 4.3), shard, rot=("x", 22.5, (11, 12, 4)))
    return m


def golden():
    m = Model("totem_golden", "Золотой идол", "totem")
    gold = Mat("metal", "#7a4c0c", "#c8901e", "#ffd24a", "#fff4b0", edge="bevel")
    dgold = Mat("metal", "#5a3408", "#a8700e", "#e0a82a", "#ffe07a", edge="bevel")
    sand = Mat("stone", "#7a5a30", "#b08a4c", "#d8b472", "#f0d898", edge="bevel")
    red = Mat("band", "#7a1018", "#c02830", "#e85a50")
    emerald = Mat("glow", "#0a8a4a", "#20d878", "#7affb0", "#d8ffe8", glow=True)
    ruby = Mat("gem", "#9a1030", "#e83050", "#ff8098", glow=True)
    sun = Mat("metal", "#a03a08", "#e8701a", "#ffa030", "#ffd070", edge="bevel")
    # Ступенчатый храм.
    m.box((2.5, 0, 2.5), (13.5, 1, 13.5), sand)
    m.box((3.5, 1, 3.5), (12.5, 2, 12.5), sand)
    m.box((4.5, 2, 4.5), (11.5, 2.5, 11.5), dgold)
    m.box((2.3, 1, 2.3), (3.5, 1.6, 3.5), emerald, mirror=True)
    m.box((2.3, 1, 12.5), (3.5, 1.6, 13.7), emerald, mirror=True)
    m.box((3.5, 0.4, 13.5), (12.5, 0.8, 13.7), red)
    # Приземистое тело с солнечным знаком.
    m.box((5, 2.5, 5.5), (11, 6.5, 10.5), gold, key={"r": "#7a4c0c", "y": "#fff4b0"}, art={"south": [
        "............", "............", "....rrrr....", "...ryyyyr...", "...ryyyyr...",
        "....rrrr....", "............", "............"]})
    m.box((3.5, 3, 6.5), (5, 6, 9.5), gold, mirror=True)
    m.box((3.3, 2.7, 6.3), (5, 3.5, 9.7), dgold, mirror=True)
    m.box((4.8, 5.8, 5.3), (11.2, 6.5, 10.7), dgold)
    # Маска-голова с изумрудными глазами.
    m.box((4.5, 6.5, 5), (11.5, 12.5, 10.5), gold, key={"k": "#4a2a06", "w": "#fff4b0", "n": "#c8901e"}, art={"south": [
        "..............", "kkkkk....kkkkk", "..............", "..............", "..............",
        "..............", "......kk......", "......nn......", "..............",
        "..kkkkkkkkkk..", "..kwkwkwkwkw..", "..kkkkkkkkkk.."]})
    m.box((5.5, 9, 10.5), (7.5, 10.2, 10.7), emerald, mirror=True)
    m.box((7.4, 12.5, 7), (8.6, 13.2, 9), ruby)
    m.box((5, 12.5, 6), (11, 13, 10), dgold)
    # Солнечный диск и лучи позади головы.
    m.sprite([
        ".......rr.......",
        "..r....rr....r..",
        "...r.oooooo.r...",
        "....oooooooo....",
        "...oooooooooo...",
        "rr.oooooooooo.rr",
        "rrroooooooooorrr",
        "rrroooooooooorrr",
        "rr.oooooooooo.rr",
        "...oooooooooo...",
        "....oooooooo....",
        "...r.oooooo.r...",
        "..r....rr....r..",
        ".......rr.......",
    ], {"r": {"mat": sun, "depth": (3.6, 4.6)}, "o": {"mat": dgold, "depth": (4.4, 5)}}, at=(0, 2), depth=(4.4, 5), side=1)
    # Знак солнца на обратной стороне диска.
    m.sprite([
        ".rrrr.",
        "rr..rr",
        "r.rr.r",
        "r.rr.r",
        "rr..rr",
        ".rrrr.",
    ], {"r": sun}, at=(5, 6), depth=(3.9, 4.4))
    return m


def forest():
    m = Model("totem_forest", "Дух леса", "totem")
    bark = Mat("wood", "#2a1a0e", "#5a3a1e", "#7e5530", "#a07844", edge="bevel")
    darkbark = Mat("wood", "#1c1008", "#3a2412", "#5a3a1e", "#7e5530")
    leaf = Mat("fur", "#1a5020", "#2c8a30", "#58c048", "#a0e868", edge="bevel")
    leaf2 = Mat("fur", "#2a6a22", "#48a838", "#82d658", "#c0f080")
    moss = Mat("stone", "#2a4a1e", "#46782c", "#68a040", "#90c868", edge="bevel")
    eye = Mat("glow", "#20b848", "#58f080", "#b8ffc8", glow=True)
    cap = Mat("flat", "#a01818", "#d82a2a", "#f85a50")
    stem = Mat("flat", "#c8b890", "#e8dcc0", "#fff4e0")
    # Мшистая основа с корнями и грибом.
    m.box((3.5, 0, 3.5), (12.5, 1.5, 12.5), moss)
    m.box((4.5, 1.5, 4.5), (11.5, 2, 11.5), moss)
    m.box((11.5, 1.5, 8), (13, 2.3, 9), darkbark)
    m.box((4.5, 2, 10.8), (6, 2.6, 11.8), darkbark)
    m.box((3.8, 1.5, 10), (4.8, 3.2, 11), stem)
    m.box((2.8, 3.2, 9.2), (5.8, 4.4, 12.2), cap, key={"w": "#fff4e0"}, art={"up": [
        "......", "..ww..", "......", "w....w", "......", "..w..."]})
    # Туловище из коры и руки-ветки.
    m.box((5.5, 2, 6), (10.5, 7, 10), bark, key={"k": "#2a1a0e", "l": "#58c048"}, art={"south": [
        "..........", "..........", "..kk......", ".kkk......", "..kk......",
        "......ll..", "..........", "..........", "..........", ".........."]})
    m.box((4.5, 4, 7), (5.5, 7, 9), bark, mirror=True)
    m.box((4, 6.5, 6.6), (5.4, 7.6, 9.4), leaf2, mirror=True)
    # Голова с зелёными глазами.
    m.box((5, 7, 5.5), (11, 12, 10.5), bark, key={"m": "#1c1008"}, art={"south": [
        "............", "............", "............", "............", "............",
        "............", "............", "....mmmm....", "............", "............"]})
    m.box((6, 9, 10.5), (7.5, 10, 10.7), eye, mirror=True)
    m.box((7.5, 7.3, 10.5), (8.5, 8, 10.7), darkbark)
    # Лиственные волосы.
    m.box((4.5, 12, 5), (11.5, 13.5, 11), leaf)
    m.box((4.2, 9.5, 5.2), (5, 12, 10.8), leaf, mirror=True)
    m.box((4.8, 8.5, 5), (11.2, 12, 5.8), leaf2)
    m.box((5, 12.6, 5.5), (7, 14.4, 7.5), leaf2, rot=("y", 45, (6, 13, 6.5)))
    m.box((9, 12.6, 8.5), (11, 14.4, 10.5), leaf2, rot=("y", 45, (10, 13, 9.5)))
    m.box((6.5, 12.6, 7), (9.5, 14, 10), leaf, rot=("y", 22.5, (8, 13, 8.5)))
    m.box((5.2, 11.8, 10.6), (7.2, 12.6, 11.3), leaf2)
    m.box((8.8, 11.8, 10.6), (10.8, 12.4, 11.3), leaf2)
    # Крошечные рога-ветки.
    m.box((5.7, 14, 7.2), (6.3, 15.5, 7.8), bark, rot=("z", 22.5, (6, 14, 7.5)), mirror=True)
    m.box((4.6, 14.6, 7.2), (5.2, 15.9, 7.8), bark, rot=("z", -22.5, (4.9, 14.8, 7.5)), mirror=True)
    # Плащ из листвы на спине.
    m.sprite([
        "..ll..ll..",
        ".llllllll.",
        "lllllllll.",
        ".llllllll.",
        "..llllll..",
    ], {"l": leaf}, at=(3, 3.5), depth=(4.4, 5.4))
    return m


def ocean():
    m = Model("totem_ocean", "Страж глубин", "totem")
    teal = Mat("flat", "#0e4a4a", "#1a7a78", "#2aa8a0", "#6adcc8", edge="bevel")
    belly = Mat("band", "#2a6a60", "#58a898", "#98d8c0")
    orange = Mat("metal", "#a03c10", "#e8782a", "#ffb347", "#ffe0a0")
    tipm = Mat("metal", "#c85a14", "#ff9a3a", "#ffd078", "#fff0c0")
    sand = Mat("stone", "#8a7448", "#c8b078", "#e8d6a0", "#f8ecc8", edge="bevel")
    coral = Mat("flat", "#a02860", "#e0508a", "#ff90b8")
    coral2 = Mat("flat", "#a04010", "#e87a30", "#ffb870")
    purple = Mat("flat", "#4a2890", "#7a50d0", "#b090f8")
    rock = Mat("stone", "#1a3a42", "#2e5a64", "#4a8490", "#6ab0b8", edge="bevel")
    eye = Mat("glow", "#e87a18", "#ffb030", "#ffe070", "#fff6c0", glow=True)
    fin = Mat("flat", "#0e5a58", "#1a8a86", "#40c0b4", "#8ae8d8", edge="bevel")
    # Песчаное дно с кораллами.
    m.box((3, 0, 3), (13, 1.5, 13), sand)
    m.box((4, 1.5, 4), (12, 2, 12), sand)
    m.box((3.5, 1.5, 10.2), (5, 3.5, 11.7), coral)
    m.box((4, 3.5, 10.8), (4.8, 4.5, 11.6), coral)
    m.box((10.8, 1.5, 10.5), (12.2, 3, 11.8), coral2)
    m.box((11.2, 3, 10.9), (12, 4.2, 11.7), coral2)
    m.box((11.5, 1.5, 4.5), (12.5, 2.8, 5.5), purple)
    m.box((6, 2, 6), (10, 3.5, 10), rock)
    m.box((9.8, 2, 11.6), (11, 2.6, 12.4), orange, rot=("y", 45, (10.4, 2.3, 12)))
    # Тело и огромный глаз.
    m.box((4.5, 3.5, 4), (11.5, 10.5, 11), teal)
    m.box((5.5, 3.7, 11), (10.5, 4.7, 11.2), belly)
    m.box((5.5, 5.5, 11), (10.5, 9.5, 11.5), eye, key={"p": "#0a1418", "o": "#a84a08"}, art={"south": [
        "..oooooo..",
        ".oo....oo.",
        "o........o",
        "o..pppp..o",
        "o..pppp..o",
        "o........o",
        ".oo....oo.",
        "..oooooo..",
    ]})
    # Колючки со всех сторон.
    for x in (6, 10):
        for z in (6.5, 9.5):
            spike(m, (x, 10.5, z), 1, 1, orange, tipm)
    for y in (5, 8.5):
        for z in (5.5, 9.5):
            spike(m, (4.5, y, z), 0, -1, orange, tipm)
            spike(m, (11.5, y, z), 0, 1, orange, tipm)
    for x in (6, 10):
        for y in (5, 9):
            spike(m, (x, y, 4), 2, -1, orange, tipm)
    spike(m, (5.5, 10, 11), 2, 1, orange, tipm)
    spike(m, (10.5, 10, 11), 2, 1, orange, tipm)
    # Боковые плавники и хвост.
    m.box((2.2, 5, 6.8), (4.5, 8, 7.8), fin, rot=("y", -22.5, (4.5, 6.5, 7.3)), mirror=True)
    m.sprite([
        "ff..",
        "fff.",
        "ffff",
        ".fff",
        ".fff",
        "ffff",
        "fff.",
        "ff..",
    ], {"f": fin}, at=(0, 3), depth=(7.5, 8.5), plane="zy")
    return m


def heart():
    m = Model("totem_heart", "Крылатое сердце", "totem")
    gold = Mat("metal", "#8a5a12", "#d49a2a", "#ffd95e", "#fff6c2", edge="bevel")
    outer = Mat("gem", "#7a0a28", "#b81e44", "#e0486a", "#ff7a9a")
    mid = Mat("gem", "#a8163c", "#e03a62", "#ff6a8a", "#ffa0b8")
    core = Mat("gem", "#c8284e", "#ff5078", "#ff8aa8", "#ffc0d0", glow=True)
    shine = Mat("glow", "#ffd0dc", "#ffe8ee", "#ffffff", glow=True)
    wing = Mat("flat", "#e0e8fa", "#ffffff", "#ffffff")
    wing2 = Mat("flat", "#c0cce8", "#f2f6ff", "#ffffff")
    # Тонкая золотая подставка.
    m.box((5, 0, 5), (11, 1, 11), gold)
    m.box((6, 1, 6), (10, 1.6, 10), gold)
    m.box((7.2, 1.6, 7.2), (8.8, 4.2, 8.8), gold)
    m.box((6.2, 3.6, 6.2), (9.8, 4.4, 9.8), gold)
    # Сердце: три слоя глубины, ближе к центру — выпуклее.
    m.sprite([
        ".aaa..aaa.",
        "abbbaabbba",
        "abhsbbbbba",
        "abscccbcba",
        "abccccccba",
        ".abcccccb.",
        "..abccbba.",
        "...abbba..",
        "....aba...",
        ".....a....",
    ], {
        "a": {"mat": outer, "depth": (6.3, 9.7)},
        "b": {"mat": mid, "depth": (5.6, 10.4)},
        "c": {"mat": core, "depth": (5.0, 11.0)},
        "h": {"mat": shine, "depth": (5.0, 11.2)},
        "s": {"mat": shine, "depth": (5.0, 11.2)},
    }, at=(3, 4.4), depth=(6.3, 9.7))
    # Маленькие белые крылья позади сердца, два слоя перьев.
    m.sprite([
        "w.....",
        "ww....",
        "www...",
        "wwwww.",
        ".wwwww",
        "..www.",
    ], {"w": wing2}, at=(0, 9), depth=(4.2, 4.9), side=2)
    m.sprite([
        ".....w",
        "....ww",
        "...www",
        ".wwwww",
        "wwwww.",
        ".www..",
    ], {"w": wing2}, at=(10, 9), depth=(4.2, 4.9), side=2)
    m.sprite([
        ".ww..",
        ".www.",
        "..www",
        "...ww",
    ], {"w": wing}, at=(0.5, 9), depth=(4.9, 5.6), side=2)
    m.sprite([
        "..ww.",
        ".www.",
        "www..",
        "ww...",
    ], {"w": wing}, at=(10.5, 9), depth=(4.9, 5.6), side=2)
    return m


def skull():
    m = Model("totem_skull", "Череп", "totem")
    bone = Mat("bone", "#8a7a5a", "#c8ba94", "#eee4c8", "#fff8e8", edge="bevel")
    dbone = Mat("bone", "#6a5a40", "#a89870", "#d0c29c", "#eee4c8")
    base = Mat("stone", "#0c0a12", "#1c1a26", "#30303c", "#4a4a58", edge="bevel")
    wax = Mat("flat", "#c8b890", "#eee4c8", "#fffaf0")
    eye = Mat("glow", "#d82810", "#ff7a1a", "#ffd04a", glow=True)
    flame = Mat("glow", "#ff7a10", "#ffb020", "#ffe060", "#fff6b0", glow=True)
    gold = Mat("metal", "#8a5a12", "#d49a2a", "#ffd95e", "#fff6c2")
    # Тёмный постамент и разбросанные кости.
    m.box((3, 0, 3), (13, 2, 13), base)
    m.box((6.5, 2, 6.5), (9.5, 2.5, 9.5), base)
    m.box((3.5, 2, 10.5), (8.5, 2.8, 11.3), dbone, rot=("y", 22.5, (6, 2.4, 10.9)))
    m.box((9, 2, 10.2), (12.2, 2.8, 11), dbone, rot=("y", -45, (10.6, 2.4, 10.6)))
    m.box((4.2, 2, 4.8), (7, 2.7, 5.6), dbone, rot=("y", 45, (5.6, 2.3, 5.2)))
    m.box((10, 2, 5.2), (11.4, 3.2, 6.6), bone)
    # Челюсть с зубами и череп с глазницами.
    m.box((5.5, 2.5, 6), (10.5, 5, 10.5), bone, key={"t": "#8a7a5a", "k": "#1a1218"}, art={"south": [
        "..........", ".t.t..t.t.", "ktkttkttkt", "..........", ".........."]})
    m.box((5, 5, 5), (11, 11, 11), bone, key={"k": "#14101a", "c": "#8a7a5a"}, art={"south": [
        "............", "............", "....c.......", "...c........", "............",
        "..kkk..kkk..", "..kkk..kkk..", "..kkk..kkk..", ".....kk.....", ".....kk.....", "............", "............"]})
    m.box((4.6, 6.5, 6), (5, 10.5, 10), bone, mirror=True)
    m.box((5.5, 11, 5.5), (10.5, 12, 10.5), bone)
    m.box((5.8, 6.8, 11), (7.2, 7.8, 11.15), eye, mirror=True)
    m.box((5.5, 5, 4.6), (10.5, 8, 5), dbone)
    # Свеча с пламенем.
    m.box((6.5, 12, 6.5), (9.5, 12.5, 9.5), gold)
    m.box((7, 12.5, 7), (9, 14.5, 9), wax)
    m.box((7.85, 14.5, 7.85), (8.15, 15, 8.15), base)
    m.box((7.4, 15, 7.4), (8.6, 16, 8.6), flame)
    return m


def ender():
    m = Model("totem_ender", "Идол Края", "totem")
    obs = Mat("stone", "#07030e", "#160a28", "#2a1450", "#46267a", edge="bevel")
    obs2 = Mat("stone", "#0e0618", "#201038", "#38206a", "#58349a", edge="bevel")
    endstone = Mat("stone", "#8a7e48", "#c4b872", "#e4dca0", "#f6f0c0", edge="bevel")
    eye = Mat("glow", "#0a6a52", "#20b890", "#6af0c0", "#d0fff0", glow=True)
    rim = Mat("metal", "#07030e", "#1c0e34", "#3a2070", "#5a3a9a")
    pupil = Mat("flat", "#020006", "#08020e", "#14081e")
    shard = Mat("crystal", "#5a1cb0", "#9a4cf0", "#d09cff", "#f4dcff", glow=True)
    rune = Mat("glow", "#b04cff", "#d890ff", "#f4d8ff", glow=True)
    # Основание из эндерняка.
    m.box((3, 0, 3), (13, 1.5, 13), endstone)
    m.box((4, 1.5, 4), (12, 2.5, 12), endstone)
    # Обелиск уступами.
    m.box((5, 2.5, 5), (11, 4, 11), obs2)
    m.box((5.5, 4, 5.5), (10.5, 9.5, 10.5), obs)
    m.box((6, 9.5, 6), (10, 11.5, 10), obs2)
    m.box((6.5, 11.5, 6.5), (9.5, 12.5, 9.5), obs)
    m.box((7, 12.5, 7), (9, 14, 9), obs2, rot=("y", 45, (8, 13, 8)))
    # Огромный Глаз Края.
    m.sprite([
        "..oooo..",
        ".oeeeeo.",
        "oeeppeeo",
        "oeeppeeo",
        ".oeeeeo.",
        "..oooo..",
    ], {
        "o": {"mat": rim, "depth": (10.5, 11.1)},
        "e": {"mat": eye, "depth": (10.5, 11.3)},
        "p": {"mat": pupil, "depth": (10.5, 11.4)},
    }, at=(4, 5.5), depth=(10.5, 11.2))
    # Руны на спине.
    m.sprite([
        "r..r",
        "rrrr",
        "r..r",
        "..r.",
        "rr.r",
    ], {"r": rune}, at=(6, 5), depth=(5.2, 5.5))
    # Парящие осколки.
    m.box((1.6, 6, 7), (2.8, 10.5, 8), shard, rot=("z", 22.5, (2.2, 8, 7.5)))
    m.box((13.3, 9, 7), (14.5, 13, 8), shard, rot=("z", -22.5, (13.9, 11, 7.5)))
    m.box((12.3, 3.5, 10.5), (13.3, 6, 11.5), shard, rot=("z", -22.5, (12.8, 4.8, 11)))
    m.box((2.6, 3, 11), (3.6, 5.5, 12), shard, rot=("z", 22.5, (3.1, 4.2, 11.5)))
    m.box((10.5, 11, 3), (11.5, 14, 4), shard, rot=("z", -22.5, (11, 12.5, 3.5)))
    m.box((4, 11.5, 3.5), (5, 14, 4.5), shard, rot=("z", 22.5, (4.5, 12.7, 4)))
    return m


def cat():
    m = Model("totem_cat", "Кот удачи", "totem")
    white = Mat("fur", "#c4c8d4", "#eef0f6", "#ffffff", "#ffffff")
    pink = Mat("flat", "#d06a84", "#f08fa6", "#ffb8c8")
    orange = Mat("fur", "#c8661a", "#ee8a2e", "#ffb060")
    red = Mat("cloth", "#6e0f1a", "#b3202e", "#e0414a", "#ff7b7b", edge="bevel")
    gold = Mat("metal", "#8a5a12", "#d49a2a", "#ffd95e", "#fff6c2", edge="bevel")
    coin = Mat("metal", "#9a6414", "#e0a82a", "#ffd95e", "#fff6b8")
    dark = Mat("flat", "#2a2030", "#3a2c44", "#524058")
    # Красная подушка с золотыми кисточками.
    m.box((3.5, 0, 3.5), (12.5, 1.5, 12.5), red)
    m.box((4, 1.5, 4), (12, 2.5, 12), red)
    m.box((3.2, 0.2, 3.2), (4, 1.2, 4), gold, mirror=True)
    m.box((3.2, 0.2, 12), (4, 1.2, 12.8), gold, mirror=True)
    # Тело, воротник, колокольчик.
    m.box((5, 2.5, 5.5), (11, 7.5, 10.5), white)
    m.box((4.7, 6.6, 5.2), (11.3, 7.8, 10.8), red)
    m.box((7.1, 5.9, 10.8), (8.9, 7.3, 11.5), gold)
    m.box((7.4, 6.3, 11.5), (8.6, 6.5, 11.6), dark)
    # Голова: счастливая мордочка.
    m.box((4.5, 7.5, 5), (11.5, 13, 10.5), white, key={"k": "#3a2c44", "p": "#f08fa6", "c": "#ffb8c8", "o": "#ee8a2e"}, art={"south": [
        "ooooo.........", "oooo..........", "ooo...........", "..............", "..............",
        "...kkk....kkk.", "..k...k..k...k", "..............", "......pp......", "kk.cc.kk.cc.kk", "......kk......"]})
    m.box((4.8, 8.6, 4.7), (11.2, 10.6, 5), orange)
    # Розовые уши.
    for x in (4.5, 8.5):
        m.sprite([
            ".w.",
            "wpw",
        ], {"w": {"mat": white, "depth": (6, 8.5)}, "p": {"mat": pink, "depth": (6, 8.8)}}, at=(x, 13), depth=(6, 8.5))
    # Поднятая лапа и лапа с монетой.
    m.box((11, 4.5, 6.5), (13, 9, 9.5), white)
    m.box((11, 9, 6.5), (13, 11.5, 9.5), white, key={"p": "#f08fa6"}, art={"south": [
        "....", ".pp.", "pppp", ".pp.", "...."]})
    m.sprite([
        ".ooo.",
        "ogdgo",
        ".ooo.",
    ], {
        "o": {"mat": coin, "depth": (10.5, 11.2)},
        "g": {"mat": gold, "depth": (10.5, 11.0)},
        "d": {"mat": dark, "depth": (10.5, 11.1)},
    }, at=(5.5, 2.8), depth=(10.5, 11.2))
    m.box((4, 3.5, 7), (5, 6.5, 9.5), white)
    # Хвост.
    m.box((7, 2.5, 4.2), (9, 4, 5.5), white)
    m.box((7, 2.5, 3.2), (9, 9, 4.2), white)
    m.box((7, 9, 3.2), (9, 10, 4.7), orange)
    return m


def build():
    return [angel(), demon(), frost(), golden(), forest(), ocean(), heart(), skull(), ender(), cat()]
