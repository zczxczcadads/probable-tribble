"""Облики мечей. Модель стоит вертикально: рукоять внизу (центр хвата около y=1.5), клинок вверх."""
from kit import Mat, Model


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


def build():
    return [frost()]
