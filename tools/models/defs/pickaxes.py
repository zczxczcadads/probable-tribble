"""Облики кирок. Модель стоит вертикально: рукоять внизу (центр хвата около y=1.5), головка вверху."""
from kit import Mat, Model

HEAD_ROWS = 12  # строк головки; ниже идёт рукоять (16 строк), весь рисунок 28 строк от y=-3 до y=25


def _sprite(m, head, shaft, key, depth=(7.2, 8.8)):
    """Левая половина головки зеркалится; рукоять задаётся строками, прижатыми к центру."""
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
        ".....lll",
        "...lllcc",
        "..lssscc",
        ".lssddgg",
        "lsd..ggg",
        "ls...gGG",
        "ld...ggg",
        "d.....gg",
        "......gg",
        ".....GGg",
        ".....ggh",
        "......gh",
    ]
    shaft = ["h", "h", "h", "gg", "h", "h", "h", "h", "h", "h", "h", "h", "h", "h", "gg", "g"]
    _sprite(m, head, shaft, {
        "s": _d(shard, 6.9, 9.1), "l": _d(light, 6.6, 9.4), "d": _d(dark, 7.3, 8.7),
        "c": _d(core, 6.8, 9.2), "g": _d(gold, 6.9, 9.1), "G": _d(gold, 6.7, 9.3),
        "h": _d(wood, 7.3, 8.7),
    })
    return m


def build():
    return [crystal()]
