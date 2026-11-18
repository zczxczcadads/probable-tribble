"""Шляпы. Единица = пиксель скина: голова занимает куб от 4 до 12, лицо смотрит на север (−Z)."""
import math

from kit import Mat, Model


def plate(m, cx, cz, r, ys, mat, hole=0.0, half=0.0, cell=1.0):
    """Горизонтальный диск или кольцо; half > 0 вырезает квадрат головы (от 8−half до 8+half)."""
    n = int(math.ceil(r * 2 / cell - 1e-6))
    rows = []
    for j in range(n):
        row = ""
        for i in range(n):
            dx, dz = (i + 0.5) * cell - r, (j + 0.5) * cell - r
            ok = hole - 1e-6 <= math.hypot(dx, dz) <= r + 1e-6
            if half and abs(cx + dx - 8) < half and abs(cz + dz - 8) < half:
                ok = False
            row += "o" if ok else " "
        rows.append(row)
    m.sprite(rows, {"o": mat}, at=(cx - r, cz - r), depth=ys, plane="xz", cell=cell, side=None)


def chain(m, x, y, z, segs, mirror=False):
    """Изогнутый рог из повёрнутых коробок. seg = (угол от оси +X в градусах, длина, ширина, глубина, материал)."""
    for ang, length, w, d, mat in segs:
        rad = math.radians(ang)
        dx, dy = math.cos(rad), math.sin(rad)
        cx, cy = x + dx * length / 2, y + dy * length / 2
        ext = length + 0.3
        if ang <= 45:
            hx, hy, rot = ext / 2, w / 2, ang
        else:
            hx, hy, rot = w / 2, ext / 2, ang - 90
        m.box((cx - hx, cy - hy, z - d / 2), (cx + hx, cy + hy, z + d / 2), mat,
              rot=("z", rot, (cx, cy, z)) if rot else None, mirror=mirror)
        x, y = x + dx * length, y + dy * length


def tri_rows(w, h, apex, inset=0.0, top=0.0, ch="f"):
    rows = []
    for r in range(h):
        t = (r + 0.5) / h
        left, right = apex * (1 - t) + inset, apex * (1 - t) + w * t - inset
        row = ""
        for c in range(w):
            row += ch if left <= c + 0.5 <= right and t >= top else " "
        rows.append(row)
    return rows


def engrave(w, h):
    """Гравировка пояса: цепочка «V» из тёмных и светлых оттенков металла."""
    rows = ["" for _ in range(h)]
    mid = h // 2
    for x in range(w):
        k = x % 4
        for y in range(h):
            ch = "."
            if y == mid - 1 and k in (0, 3):
                ch = "0"
            elif y == mid and k in (1, 2):
                ch = "0"
            elif y == mid + 1 and k in (1, 2):
                ch = "4"
            rows[y] += ch
    return rows


def crown():
    m = Model("hat_crown", "Королевская корона", "hat")
    gold = Mat("metal", "#8a5a12", "#d49a2a", "#ffd95e", "#fff6c2", edge="bevel")
    velvet = Mat("cloth", "#6b0f1f", "#a3182f", "#d43a4f")
    ruby = Mat("gem", "#7a0b1d", "#e0243f", "#ff9aa8", glow=True)
    sapphire = Mat("gem", "#0b2f7a", "#2a6bff", "#a8c8ff", glow=True)
    emerald = Mat("gem", "#0b5a2a", "#1fc45a", "#b6ffd0", glow=True)
    # Обод с гравировкой.
    fb = {"north": engrave(18, 5), "south": engrave(18, 5)}
    sb = {"west": engrave(14, 5), "east": engrave(14, 5)}
    m.box((3.5, 10.5, 3.5), (12.5, 13, 4.5), gold, art={"north": fb["north"]})
    m.box((3.5, 10.5, 11.5), (12.5, 13, 12.5), gold, art={"south": fb["south"]})
    m.box((3.5, 10.5, 4.5), (4.5, 13, 11.5), gold, art={"west": sb["west"]})
    m.box((11.5, 10.5, 4.5), (12.5, 13, 11.5), gold, art={"east": sb["east"]})
    # Зубцы-пирамиды: высокий по центру, средние и угловые, на каждом — камень.
    for z in (3.5, 11.5):
        m.box((7, 13, z), (9, 15, z + 1), gold)
        m.box((7.4, 15, z), (8.6, 16.2, z + 1), gold)
        m.box((7.5, 16.2, z + 0.25), (8.5, 17.2, z + 0.75), ruby)
        m.box((3.5, 13, z), (5, 15, z + 1), gold, mirror=True)
        m.box((3.8, 15, z + 0.25), (4.7, 15.9, z + 0.75), sapphire, mirror=True)
        m.box((5.6, 13, z), (6.6, 14.4, z + 1), gold, mirror=True)
    m.box((3.5, 13, 7), (4.5, 15, 9), gold, mirror=True)
    m.box((3.5, 15, 7.4), (4.5, 16.2, 8.6), gold, mirror=True)
    m.box((3.75, 16.2, 7.5), (4.25, 17.2, 8.5), sapphire, mirror=True)
    for z0 in (5.2, 9.8):
        m.box((3.5, 13, z0), (4.5, 14.4, z0 + 1), gold, mirror=True)
    # Бархатная подкладка.
    m.box((4.5, 12, 4.5), (11.5, 14, 11.5), velvet)
    # Камни на ободе: по центру и по бокам, с каждой стороны.
    for z, zz in ((3.2, 3.5), (12.5, 12.8)):
        m.box((7.25, 11, z), (8.75, 12.5, zz), ruby)
        m.box((5.5, 11.35, z), (6.3, 12.15, zz), sapphire, mirror=True)
    m.box((3.2, 11, 7.25), (3.5, 12.5, 8.75), sapphire, mirror=True)
    for z0 in (5.4, 9.8):
        m.box((3.2, 11.35, z0), (3.5, 12.15, z0 + 0.8), emerald, mirror=True)
    return m


def wizard():
    m = Model("hat_wizard", "Шляпа волшебника", "hat")
    indigo = Mat("cloth", "#1b1259", "#3a2a9a", "#6a52d8")
    deep = Mat("cloth", "#240c46", "#4a1d86", "#7d45c8")
    gold = Mat("metal", "#8a5a12", "#d49a2a", "#ffd95e", "#fff6c2", edge="bevel")
    star = Mat("metal", "#b8801a", "#ffcf3a", "#fff0a0", "#ffffff")
    gem = Mat("gem", "#0b5b6e", "#22d3ee", "#d4fbff", glow=True)
    # Поля: широкий диск и приподнятая ступень.
    plate(m, 8, 8, 9, (11, 11.5), deep, half=4)
    plate(m, 8, 8, 7, (11.5, 12), indigo, half=4)
    plate(m, 8, 8, 5.5, (12, 13), gold)
    # Конус с изгибом: центр уходит вбок, к кончику сужается и клонится вниз.
    for y0, y1, r, cx in ((13, 16, 4.5, 8), (16, 18.5, 3.5, 8.5), (18.5, 20.5, 3, 9.5),
                          (20.5, 22.5, 2.5, 10.5), (22.5, 24, 2, 12), (23.5, 25, 1.5, 13.5)):
        plate(m, cx, 8, r, (y0, y1), indigo)
    plate(m, 15.5, 8, 1, (22, 23.5), indigo)
    m.box((15, 21, 7.5), (16, 22, 8.5), gem)
    # Пряжка и камень.
    m.box((6.5, 11.9, 2.1), (9.5, 13.4, 2.5), gold)
    m.box((7.4, 12.2, 1.8), (8.6, 13.1, 2.1), gem)
    # Золотые звёзды.
    big = ["  s  ", " sss ", "sssss", " sss ", " s s "]
    m.sprite(big, {"s": star}, at=(5.75, 13.25), depth=(3.25, 3.5), plane="xy", cell=0.5)
    m.sprite(big, {"s": star}, at=(5.75, 13.25), depth=(12.5, 12.75), plane="xy", cell=0.5)
    m.sprite(big, {"s": star}, at=(6.75, 13.25), depth=(12.5, 12.75), plane="zy", cell=0.5)
    m.sprite(big, {"s": star}, at=(6.75, 13.25), depth=(3.25, 3.5), plane="zy", cell=0.5)
    small = [" s ", "sss", " s "]
    m.sprite(small, {"s": star}, at=(7.75, 16.5), depth=(4.25, 4.5), plane="xy", cell=0.5)
    m.sprite(small, {"s": star}, at=(7.0, 17.0), depth=(12.0, 12.25), plane="zy", cell=0.5)
    return m


def tophat():
    m = Model("hat_tophat", "Цилиндр", "hat")
    silk = Mat("flat", "#16161f", "#282838", "#40405a", "#6a6a90")
    red = Mat("cloth", "#5a0b16", "#9b1224", "#d6283f")
    gold = Mat("metal", "#8a5a12", "#d49a2a", "#ffd95e", "#fff6c2", edge="bevel")
    card = Mat("cloth", "#c9c2b0", "#f2eee2", "#ffffff")
    heart = Mat("flat", "#9b1224", "#e0243f", "#ff6a7a")
    # Поля с загнутым краем.
    plate(m, 8, 8, 9, (11, 11.5), silk, half=4)
    plate(m, 8, 8, 9, (11.5, 12), silk, hole=8, half=4)
    # Красная лента и цилиндр, расширяющийся кверху.
    plate(m, 8, 8, 5.5, (12, 14), red)
    plate(m, 8, 8, 5, (14, 18), silk)
    plate(m, 8, 8, 5.5, (18, 20), silk)
    plate(m, 8, 8, 6, (20, 21), silk)
    plate(m, 8, 8, 5.5, (21, 21.5), silk, hole=4.5)
    # Золотая пряжка.
    m.box((6.25, 12.2, 2.0), (9.75, 13.8, 2.5), gold)
    m.box((7.1, 12.7, 1.75), (8.9, 13.3, 2.0), red)
    m.box((7.7, 12.45, 1.5), (8.3, 13.55, 1.75), gold)
    # Карта за лентой.
    m.sprite(["ccccc", "crcrc", "crrrc", "ccrcc", "ccccc", "ccccc", "ccccc"],
             {"c": card, "r": heart}, at=(5.75, 13), depth=(13.25, 13.75), plane="zy", cell=0.5)
    return m


def halo():
    m = Model("hat_halo", "Нимб", "hat")
    glow = Mat("glow", "#9a6a00", "#ffcf3a", "#fff3a0", glow=True)
    pale = Mat("glow", "#d8b030", "#fff0a0", "#ffffff", glow=True)
    gold = Mat("metal", "#8a5a12", "#d49a2a", "#ffd95e", "#fff6c2", edge="bevel")
    white = Mat("cloth", "#c0cdec", "#eef3ff", "#ffffff")
    spark = Mat("glow", "#ffe9a0", "#ffffff", "#ffffff", glow=True)
    plate(m, 8, 8, 5, (14.5, 15.5), glow, hole=3.8, cell=0.5)
    # Крылья по бокам головы: веер перьев, сверху мелкое оперение; золотая застёжка у виска.
    wing = ["...wwww",
            "..wwwww",
            ".wmwwmw",
            "wwwmwwm",
            "wmwwmw.",
            ".w.wm.."]
    cover = ["..ww.",
             ".wmwm",
             "wmw.."]
    shade = Mat("cloth", "#7b8cb8", "#b7c5e6", "#dfe8fb")
    key = {"w": white, "m": shade}
    m.box((12, 8.4, 7.5), (12.6, 9.6, 8.5), gold, mirror=True)
    m.sprite(wing, key, at=(12.6, 7), depth=(7.25, 8.75), plane="xy", cell=1.0)
    m.sprite([r[::-1] for r in wing], key, at=(3.4 - 7, 7), depth=(7.25, 8.75), plane="xy", cell=1.0)
    m.sprite(cover, key, at=(12.6, 8), depth=(8.75, 9.25), plane="xy", cell=1.0)
    m.sprite([r[::-1] for r in cover], key, at=(3.4 - 5, 8), depth=(8.75, 9.25), plane="xy", cell=1.0)
    # Искры.
    star = [" s ", "sss", " s "]
    m.sprite(star, {"s": spark}, at=(3.5, 17.5), depth=(7.75, 8.25), plane="xy", cell=0.5)
    m.sprite(star, {"s": spark}, at=(11.0, 18.5), depth=(7.75, 8.25), plane="xy", cell=0.5)
    m.sprite(star, {"s": spark}, at=(7.2, 19.0), depth=(4.5, 5.0), plane="zy", cell=0.5)
    for p in ((5.5, 20.5, 6.0), (12.5, 16.5, 10.5), (3.2, 15.5, 10.5), (13.5, 14.5, 5.8), (8.5, 17.5, 11.0)):
        m.box((p[0], p[1], p[2]), (p[0] + 0.5, p[1] + 0.5, p[2] + 0.5), spark)
    return m


def horns():
    m = Model("hat_horns", "Рога демона", "hat")
    iron = Mat("metal", "#0f0710", "#241430", "#4a2a52", "#7a4a80", edge="bevel")
    black = Mat("wrap", "#0a0507", "#1d0b10", "#3a1219")
    d1 = Mat("wrap", "#1d0509", "#4a0b14", "#7d1a24")
    d2 = Mat("wrap", "#3a0710", "#7a1020", "#b82233")
    d3 = Mat("wrap", "#5a0b18", "#a3162c", "#e0384a")
    ember = Mat("glow", "#a82a00", "#ff6a1a", "#ffd27a", glow=True)
    ruby = Mat("gem", "#7a0b1d", "#e0243f", "#ff9aa8", glow=True)
    # Чёрный обод с шипами.
    m.box((3.5, 10.5, 3.5), (12.5, 12, 4.5), iron)
    m.box((3.5, 10.5, 11.5), (12.5, 12, 12.5), iron)
    m.box((3.5, 10.5, 4.5), (4.5, 12, 11.5), iron)
    m.box((11.5, 10.5, 4.5), (12.5, 12, 11.5), iron)
    for z in (3.5, 11.5):
        m.box((7, 12, z), (9, 13.2, z + 1), iron)
        m.box((7.4, 13.2, z + 0.1), (8.6, 14.4, z + 0.9), iron)
        m.box((7.7, 14.4, z + 0.3), (8.3, 16, z + 0.7), ember)
        m.box((4.9, 12, z), (6.2, 12.9, z + 1), iron, mirror=True)
        m.box((5.2, 12.9, z + 0.2), (5.9, 14.3, z + 0.8), iron, mirror=True)
    for z0 in (5.3, 9.7):
        m.box((3.5, 12, z0), (4.5, 12.9, z0 + 1), iron, mirror=True)
        m.box((3.7, 12.9, z0 + 0.2), (4.3, 14.2, z0 + 0.8), iron, mirror=True)
    m.box((3.5, 12, 7), (4.5, 13.2, 9), iron, mirror=True)
    m.box((3.7, 13.2, 7.4), (4.3, 14.4, 8.6), iron, mirror=True)
    m.box((3.85, 14.4, 7.7), (4.15, 15.8, 8.3), ember, mirror=True)
    m.box((7.3, 10.8, 3.2), (8.7, 11.8, 3.5), ruby)
    # Рога: загнутые вверх и внутрь, от чёрного основания к раскалённому кончику.
    m.box((9.25, 12, 6.5), (12.25, 13, 9.5), black, mirror=True)
    chain(m, 10.75, 13, 8, [
        (67.5, 2.5, 3.0, 3.0, black), (67.5, 2.2, 2.6, 2.6, d1), (90, 2.0, 2.2, 2.2, d1),
        (112.5, 2.0, 1.8, 1.8, d2), (112.5, 1.8, 1.4, 1.4, d3), (135, 1.5, 1.0, 1.0, ember)], mirror=True)
    return m


def cat_ears():
    m = Model("hat_cat_ears", "Кошачьи ушки", "hat")
    band = Mat("flat", "#c2306a", "#ff5c98", "#ffb3cd", edge="bevel")
    fur = Mat("fur", "#6f6a8c", "#a29cc8", "#d8d3f0")
    pink = Mat("fur", "#d4527f", "#ff8fb7", "#ffd0e0")
    cream = Mat("cloth", "#e8c8d4", "#fff0f5", "#ffffff")
    gold = Mat("metal", "#8a5a12", "#d49a2a", "#ffd95e", "#fff6c2", edge="bevel")
    # Ободок: перекладина сверху и стойки у висков.
    m.box((3.5, 12, 7.5), (12.5, 12.75, 9), band)
    m.box((3.5, 8, 7.5), (4, 12, 9), band, mirror=True)
    # Уши: ступенчатые треугольники, внутри розовые.
    w, h = 8, 12
    east = tri_rows(w, h, 6)
    inner = tri_rows(w, h, 6, inset=1.6, top=0.3, ch="p")
    m.sprite(east, {"f": fur}, at=(8.5, 12), depth=(5, 7.5), plane="xy", cell=0.5)
    m.sprite(inner, {"p": pink}, at=(8.5, 12), depth=(4.75, 5), plane="xy", cell=0.5)
    m.sprite([r[::-1] for r in east], {"f": fur}, at=(3.5, 12), depth=(5, 7.5), plane="xy", cell=0.5)
    m.sprite([r[::-1] for r in inner], {"p": pink}, at=(3.5, 12), depth=(4.75, 5), plane="xy", cell=0.5)
    # Бант и бубенчик у правого виска.
    m.sprite(["cc...cc", "ccc.ccc", "cccpccc", "ccc.ccc", "cc...cc"],
             {"c": cream, "p": pink}, at=(6.25, 9.5), depth=(12.5, 13), plane="zy", cell=0.5)
    m.box((12.5, 7.6, 7.5), (13.5, 8.6, 8.5), gold)
    return m


def viking():
    m = Model("hat_viking", "Шлем викинга", "hat")
    iron = Mat("metal", "#2d3138", "#5a6270", "#9aa3b2", "#d4dae3", edge="bevel")
    brass = Mat("metal", "#6a4510", "#b07a1e", "#f2c24a", "#fff0a8", edge="bevel")
    ivory = Mat("bone", "#8a7a52", "#cdbd90", "#f4ead0")
    # Медный обод.
    m.box((3.5, 10.5, 3.5), (12.5, 12, 4.5), brass)
    m.box((3.5, 10.5, 11.5), (12.5, 12, 12.5), brass)
    m.box((3.5, 10.5, 4.5), (4.5, 12, 11.5), brass)
    m.box((11.5, 10.5, 4.5), (12.5, 12, 11.5), brass)
    # Заклёпки.
    for x in (5, 7.5, 10):
        m.box((x, 10.9, 3.25), (x + 0.5, 11.4, 3.5), iron)
        m.box((x, 10.9, 12.5), (x + 0.5, 11.4, 12.75), iron)
    for z in (5.5, 8, 10.5):
        m.box((3.25, 10.9, z - 0.25), (3.5, 11.4, z + 0.25), iron)
        m.box((12.5, 10.9, z - 0.25), (12.75, 11.4, z + 0.25), iron)
    # Купол из ступеней и медная полоса поверх.
    layers = ((12, 13.5, 4.5), (13.5, 15, 4), (15, 16.5, 3.5), (16.5, 17.5, 2.5), (17.5, 18.25, 1.5))
    for y0, y1, r in layers:
        plate(m, 8, 8, r, (y0, y1), iron)
        m.box((7.25, y0 + 0.25, 8 - r - 0.25), (8.75, y1 + 0.25, 8 + r + 0.25), brass)
    m.box((7.5, 18.5, 7.5), (8.5, 20.5, 8.5), brass)
    # Наносник.
    m.box((7.1, 8.2, 3.0), (8.9, 10.5, 3.5), iron)
    m.box((7.4, 5.8, 3.0), (8.6, 8.2, 3.5), iron)
    m.box((7.6, 5.3, 3.0), (8.4, 5.8, 3.5), brass)
    # Рога из слоновой кости.
    m.box((12.5, 10.25, 6.5), (13.25, 12.5, 9.5), brass, mirror=True)
    chain(m, 13.25, 11.4, 8, [
        (0, 1.5, 2.6, 2.6, ivory), (22.5, 2, 2.4, 2.4, ivory), (45, 2, 2.2, 2.2, ivory),
        (67.5, 2, 2.0, 2.0, ivory), (90, 2, 1.6, 1.6, ivory), (90, 1.6, 1.1, 1.1, ivory),
        (112.5, 1.2, 0.8, 0.8, ivory)], mirror=True)
    return m


def straw():
    m = Model("hat_straw", "Соломенная шляпа", "hat")
    weave = Mat("check", "#9c7420", "#cf9f3a", "#ecc968", "#f8e39a")
    lip = Mat("wrap", "#8a6418", "#c8982f", "#e8c460")
    ribbon = Mat("cloth", "#0b2f7a", "#1f55c8", "#5c8cf0")
    white = Mat("flat", "#d8d4c4", "#f4f0e0", "#ffffff")
    sun = Mat("glow", "#d48a00", "#ffc21a", "#fff0a0")
    green = Mat("cloth", "#1d5a22", "#2f9a38", "#6fd070")
    wheat = Mat("flat", "#a87a1a", "#e6b440", "#ffe08a")
    plate(m, 8, 8, 10, (11.5, 12), weave, half=4)
    plate(m, 8, 8, 10, (12, 12.5), lip, hole=9, half=4)
    plate(m, 8, 8, 5, (12, 12.5), weave)
    plate(m, 8, 8, 5.5, (12.5, 13.5), ribbon)
    plate(m, 8, 8, 4.5, (13.5, 15), weave)
    plate(m, 8, 8, 3.5, (15, 15.5), lip)
    # Бант с хвостиками на правой стороне.
    m.sprite(["bb...bb", "bbb.bbb", "bbbkbbb", "bbb.bbb", ".b...b."],
             {"b": ribbon, "k": lip}, at=(5.75, 12.75), depth=(13, 13.75), plane="zy", cell=0.5)
    # Ромашка спереди и колосок сзади.
    m.sprite(["..www..", ".wwwww.", "wwsssww", "wwsssww", "wwsssww", ".wwwww.", "..www.."],
             {"w": white, "s": sun}, at=(7.25, 12.6), depth=(2.1, 3.5), plane="xy", cell=0.5)
    m.sprite(["g..", "gg.", ".gg"], {"g": green}, at=(10.75, 12.6), depth=(2.1, 2.5), plane="xy", cell=0.5)
    m.sprite(["..w..", ".w.w.", "..w..", ".w.w.", "..w..", ".w.w.", "..w..", "..k..", "..k..", "..k.."],
             {"w": wheat, "k": green}, at=(8.75, 12.8), depth=(12.5, 13.0), plane="xy", cell=0.5)
    return m


def mushroom():
    m = Model("hat_mushroom", "Шляпка мухомора", "hat")
    cap = Mat("cloth", "#6d0a14", "#b01524", "#e0283a", "#ff6a72")
    gill = Mat("wood", "#c8b890", "#e8dcb8", "#f8f0d8")
    spot = Mat("flat", "#cfc7b3", "#f3efe0", "#ffffff")
    skirt = Mat("wrap", "#c8b890", "#e8dcb8", "#f8f0d8")
    # Пластинки под шляпкой и юбочка-кольцо на «ножке».
    plate(m, 8, 8, 7, (11, 12), gill, half=4)
    m.box((3.5, 10, 3.5), (12.5, 11, 4.5), skirt)
    m.box((3.5, 10, 11.5), (12.5, 11, 12.5), skirt)
    m.box((3.5, 10, 4.5), (4.5, 11, 11.5), skirt)
    m.box((11.5, 10, 4.5), (12.5, 11, 11.5), skirt)
    layers = ((12, 13, 8), (13, 14, 7.5), (14, 15, 7), (15, 16, 6), (16, 17, 5), (17, 17.75, 3.5))
    for y0, y1, r in layers:
        plate(m, 8, 8, r, (y0, y1), cap)
    # Белые бугорки: по бокам (по два на нижнем уступе, по одному выше) и сверху.
    for x in (6.5, 9.5):
        for z0, z1 in ((-0.4, 0), (16, 16.4)):
            m.box((x - 0.75, 12.2, z0), (x + 0.75, 12.8, z1), spot)
        for x0, x1 in ((-0.4, 0), (16, 16.4)):
            m.box((x0, 12.2, x - 0.75), (x1, 12.8, x + 0.75), spot)
    for z0, z1 in ((1.0 - 0.4, 1.0), (15 - 0.0, 15.4)):
        m.box((7.25, 14.2, z0), (8.75, 14.8, z1), spot)
    for x0, x1 in ((1.0 - 0.4, 1.0), (15.0, 15.4)):
        m.box((x0, 14.2, 7.25), (x1, 14.8, 8.75), spot)
    for ang, rho, y in ((20, 6.5, 15), (110, 6.5, 15), (200, 6.5, 15), (290, 6.5, 15),
                        (60, 5.5, 16), (160, 5.5, 16), (250, 5.5, 16), (340, 5.5, 16)):
        x, z = 8 + rho * math.cos(math.radians(ang)), 8 + rho * math.sin(math.radians(ang))
        m.box((x - 0.5, y, z - 0.5), (x + 0.5, y + 0.4, z + 0.5), spot)
    for x, z, s in ((6.5, 6.5, 1.5), (9.5, 8.5, 1.0)):
        m.box((x, 17.75, z), (x + s, 18.15, z + s), spot)
    return m


def headphones():
    m = Model("hat_headphones", "Наушники", "hat")
    shell = Mat("metal", "#1b1d26", "#2c3040", "#454b60", "#6a7290", edge="bevel")
    pad = Mat("cloth", "#0d0e14", "#1a1c26", "#2c3040")
    neon = Mat("glow", "#0a8ab0", "#35e0ff", "#c7f8ff", glow=True)
    # Дуга оголовья: ступенчатая арка над головой.
    m.box((12.5, 10.5, 7), (13.5, 12.25, 9), shell, mirror=True)
    m.box((11.25, 12.25, 7), (13.5, 13.5, 9), shell, mirror=True)
    m.box((4.75, 12.25, 7), (11.25, 13.5, 9), shell)
    m.box((5, 12, 6.75), (11, 12.25, 9.25), pad)
    m.box((5.5, 13.5, 7.5), (10.5, 13.75, 8.5), neon)
    # Чашки: мягкий амбушюр, корпус и светящееся кольцо.
    m.box((12, 5.5, 5.5), (13, 10.5, 10.5), pad, mirror=True)
    m.box((13, 5.25, 5.25), (14.5, 10.75, 10.75), shell, mirror=True)
    m.box((14.5, 5.75, 5.75), (14.9, 6.5, 10.25), neon, mirror=True)
    m.box((14.5, 9.5, 5.75), (14.9, 10.25, 10.25), neon, mirror=True)
    m.box((14.5, 6.5, 5.75), (14.9, 9.5, 6.5), neon, mirror=True)
    m.box((14.5, 6.5, 9.5), (14.9, 9.5, 10.25), neon, mirror=True)
    m.box((14.5, 6.75, 6.75), (15.0, 9.25, 9.25), shell, mirror=True)
    # Микрофон на штанге у левой чашки.
    m.box((1.9, 3.8, 5.0), (2.6, 5.5, 5.75), shell)
    m.box((1.9, 3.8, 3.25), (2.6, 4.5, 5.0), shell)
    m.box((2.6, 3.8, 3.25), (4.6, 4.5, 4.0), shell)
    m.box((4.6, 3.6, 3.0), (5.8, 4.9, 4.0), pad)
    m.box((4.9, 3.9, 2.75), (5.5, 4.5, 3.0), neon)
    return m


def build():
    return [crown(), wizard(), tophat(), halo(), horns(), cat_ears(), viking(), straw(), mushroom(), headphones()]
