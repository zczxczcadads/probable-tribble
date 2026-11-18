"""Шляпы. Единица = пиксель скина: голова занимает куб от 4 до 12, лицо смотрит на север (−Z)."""
from kit import Mat, Model


def crown():
    m = Model("hat_crown", "Королевская корона", "hat")
    gold = Mat("metal", "#8a5a12", "#d49a2a", "#ffd95e", "#fff6c2", edge="bevel")
    velvet = Mat("cloth", "#6b0f1f", "#a3182f", "#d43a4f")
    ruby = Mat("gem", "#7a0b1d", "#e0243f", "#ff9aa8", glow=True)
    sapphire = Mat("gem", "#0b2f7a", "#2a6bff", "#a8c8ff", glow=True)
    # Обод вокруг головы.
    m.box((3.5, 11, 3.5), (12.5, 13, 4.5), gold)
    m.box((3.5, 11, 11.5), (12.5, 13, 12.5), gold)
    m.box((3.5, 11, 4.5), (4.5, 13, 11.5), gold)
    m.box((11.5, 11, 4.5), (12.5, 13, 11.5), gold)
    # Зубцы: высокий по центру каждой стороны и по углам.
    for z in (3.5, 11.5):
        m.box((7.25, 13, z), (8.75, 16, z + 1), gold)
        m.box((3.5, 13, z), (4.5, 15, z + 1), gold, mirror=True)
        m.box((5.4, 13, z), (6.4, 14.2, z + 1), gold, mirror=True)
    m.box((3.5, 13, 7.25), (4.5, 16, 8.75), gold, mirror=True)
    m.box((3.5, 13, 5.4), (4.5, 14.2, 6.4), gold, mirror=True)
    m.box((3.5, 13, 9.6), (4.5, 14.2, 10.6), gold, mirror=True)
    # Бархатная подкладка и камни.
    m.box((4.5, 11.5, 4.5), (11.5, 14, 11.5), velvet)
    m.box((7.4, 11.4, 3.2), (8.6, 12.6, 3.5), ruby)
    m.box((7.4, 11.4, 12.5), (8.6, 12.6, 12.8), ruby)
    m.box((3.2, 11.4, 7.4), (3.5, 12.6, 8.6), sapphire, mirror=True)
    m.box((7.5, 16, 3.75), (8.5, 17, 4.25), ruby)
    return m


def build():
    return [crown()]
