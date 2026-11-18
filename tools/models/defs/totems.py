"""Облики тотемов: фигурки в кубе 16×16×16, лицом на юг (+Z)."""
from kit import Mat, Model


def angel():
    m = Model("totem_angel", "Ангел-хранитель", "totem")
    gold = Mat("metal", "#8a5a12", "#d49a2a", "#ffd95e", "#fff6c2", edge="bevel")
    robe = Mat("band", "#b9c4dc", "#e6ecf7", "#ffffff")
    skin = Mat("flat", "#d9a583", "#f2cfae", "#ffe6cf")
    hair = Mat("fur", "#b8791c", "#f0c14a", "#ffe89a")
    feather = Mat("flat", "#aab8d6", "#e9f0ff", "#ffffff")
    halo = Mat("glow", "#e0a81e", "#ffe168", "#fffbd6", glow=True)
    # Постамент, туловище и руки.
    m.box((5, 0, 5), (11, 1.5, 11), gold)
    m.box((5.5, 1.5, 6), (10.5, 8, 10), robe, art={"south": [
        "..........", "..........", "....22....", "...2112...", "....22....",
        "..........", "..........", "..........", "..........", "..........", "..........", "..........", ".........."]})
    m.box((4.5, 4, 7), (5.5, 7.5, 9), robe, mirror=True)
    # Голова с лицом и волосы.
    m.box((5.5, 8, 5.5), (10.5, 13, 10.5), skin, key={"e": "#3a2a55", "m": "#c9736a", "w": "#ffffff"}, art={"south": [
        "..........", "..........", "..........", "..........",
        ".we....ew.", ".ee....ee.", "..........", "....mm....", "..........", ".........."]})
    m.box((5.2, 11.6, 5.2), (10.8, 13.4, 10.8), hair)
    m.box((5.2, 9, 5.2), (10.8, 11.6, 6.5), hair)
    # Нимб и крылья за спиной.
    m.disc(8, 8, 3, (14.4, 15), halo, hole=1.9)
    m.sprite([
        " ww        ww ",
        "wwww      wwww",
        "wwwww    wwwww",
        "wwwwww  wwwwww",
        " wwwww  wwwww ",
        " wwwww  wwwww ",
        "  wwww  wwww  ",
        "   www  www   ",
        "    ww  ww    ",
    ], {"w": feather}, at=(1, 3), depth=(5, 6), side=2)
    return m


def build():
    return [angel()]
