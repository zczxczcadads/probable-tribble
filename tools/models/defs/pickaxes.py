"""Облики кирок. Модель стоит вертикально: рукоять внизу (центр хвата около y=1.5), головка вверху."""
from kit import Mat, Model


def crystal():
    m = Model("pickaxe_crystal", "Кристальная кирка", "pickaxe")
    shard = Mat("crystal", "#0f6e7a", "#25b7c4", "#8ff0f0", "#effffd")
    core = Mat("flat", "#b6fff6", "#ffffff", glow=True)
    wood = Mat("wood", "#3a2618", "#5c3d26", "#7d5636")
    band = Mat("metal", "#6b4a12", "#b8862b", "#f0c95a", "#fff3b8")
    m.sprite([
        "    sssssss    ",
        "  sscccccccss  ",
        " sss  bbb  sss ",
        " ss   bhb   ss ",
        "ss     h     ss",
        "s      h      s",
        "s      h      s",
        "       h       ",
        "       h       ",
        "       h       ",
        "       h       ",
        "       h       ",
        "       h       ",
        "       h       ",
        "       h       ",
        "       h       ",
        "       h       ",
        "       h       ",
        "       h       ",
        "       h       ",
        "       h       ",
        "      bhb      ",
        "       h       ",
        "       h       ",
        "       h       ",
        "       b       ",
    ], {
        "s": shard,
        "c": {"mat": core, "depth": (7.1, 8.9)},
        "h": {"mat": wood, "depth": (7.3, 8.7)},
        "b": {"mat": band, "depth": (7.0, 9.0)},
    }, at=(0.5, -3), depth=(7.4, 8.6))
    return m


def build():
    return [crystal()]
