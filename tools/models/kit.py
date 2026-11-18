"""Конструктор моделей AppleCosmetic.

Модель собирается из коробок и «спрайтов» (пиксельный рисунок, выдавленный в объём),
а на выходе получаются модель предмета Minecraft, её текстура и файл Blockbench.
"""
from __future__ import annotations

import base64
import io
import math
import uuid
import zlib

import numpy as np
from PIL import Image

NAMESPACE = "applecosmetic"
FACES = ("north", "south", "east", "west", "up", "down")
# Ось нормали и её знак для каждой грани.
AXIS = {"north": (2, -1), "south": (2, 1), "east": (0, 1), "west": (0, -1), "up": (1, 1), "down": (1, -1)}
EMPTY = " ."
EPS = 1e-6


def hex_rgb(value):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def make_ramp(colors):
    """Пять оттенков от тёмного к светлому; из одного цвета оттенки строятся сами."""
    pts = np.array([hex_rgb(c) for c in colors], dtype=float)
    if len(pts) == 1:
        base = pts[0]
        pts = np.array([base * 0.42, base * 0.68, base, base + (255 - base) * 0.38, base + (255 - base) * 0.72])
    xs = np.linspace(0, len(pts) - 1, 5)
    out = np.stack([np.interp(xs, np.arange(len(pts)), pts[:, k]) for k in range(3)], axis=1)
    return np.clip(np.rint(out), 0, 255).astype(np.uint8)


class Mat:
    """Материал: стиль рисунка и палитра от тёмного к светлому.

    Стили: flat, metal, gem, glow, band, wood, wrap, stone, cloth, check, fur, bone, crystal.
    edge: 'bevel' — светлый верх и левый край, тёмный низ и правый; 'dark' — тёмная рамка.
    glow=True — деталь светится в темноте.
    """

    def __init__(self, style, *colors, glow=False, edge=None):
        self.style = style
        self.ramp = make_ramp(colors)
        self.glow = glow
        self.edge = edge
        self.key = f"{style}:{','.join(colors)}:{edge}"

    def _rng(self, *parts):
        return np.random.default_rng(zlib.crc32(":".join(map(str, (self.key,) + parts)).encode()))

    def field(self, w, h, salt=""):
        """Узор материала без учёта формы грани: индексы оттенков 0..4."""
        rng = self._rng("field", w, h, salt)
        idx = np.full((h, w), 2, dtype=np.int16)
        ys, xs = np.mgrid[0:h, 0:w]
        style = self.style
        if style in ("flat", "cloth"):
            noise = rng.random((h, w))
            idx[noise < 0.05] = 1
            idx[noise > 0.95] = 3
        elif style == "stone":
            noise = rng.random((h, w))
            idx[noise < 0.22] = 1
            idx[noise > 0.80] = 3
        elif style == "wood":
            idx[:, (np.arange(w) % 3) == 1] = 1
            idx[rng.random((h, w)) > 0.93] = 3
        elif style == "wrap":
            idx[((xs + ys) // 2) % 2 == 0] = 1
        elif style == "check":
            idx[((xs // 2 + ys // 2) % 2) == 0] = 3
        elif style == "fur":
            idx += (rng.random((1, w)) > 0.5).astype(np.int16) - (rng.random((h, w)) > 0.85).astype(np.int16)
        elif style == "bone":
            idx[:] = 3
            idx[rng.random((h, w)) < 0.08] = 2
        elif style == "crystal":
            band = (xs * 2 + ys) % 7
            idx[:] = np.where(band < 1, 4, np.where(band < 4, 3, 2))
        elif style in ("gem", "glow"):
            idx[:] = 3
        return idx

    def paint(self, w, h, face):
        """Рисунок грани коробки размером w×h текселей."""
        idx = self.field(w, h, face)
        style = self.style
        if style == "metal":
            if face == "up":
                idx += 1
            elif face == "down":
                idx -= 1
            else:
                if w >= 2:
                    idx[:, 0] += 2
                    idx[:, -1] -= 1
                if w >= 5:
                    idx[:, 1] += 1
        elif style == "band":
            if h >= 2:
                idx[0, :] += 1
                idx[-1, :] -= 1
        elif style == "gem":
            ys, xs = np.mgrid[0:h, 0:w]
            cy, cx = (h - 1) / 2, (w - 1) / 2
            dist = np.maximum(np.abs(ys - cy) / max(cy, 0.5), np.abs(xs - cx) / max(cx, 0.5))
            idx[:] = np.where(dist > 0.8, 1, np.where(dist > 0.45, 2, 3))
            idx[min(1, h - 1), min(1, w - 1)] = 4
        elif style == "glow":
            if w >= 3 and h >= 3:
                idx[1:-1, 1:-1] = 4
        if self.edge == "bevel" and w >= 3 and h >= 3:
            idx[0, :-1] += 1
            idx[1:, 0] += 1
            idx[-1, 1:] -= 1
            idx[:-1, -1] -= 1
        elif self.edge == "dark" and w >= 3 and h >= 3:
            idx[0, :] -= 1
            idx[-1, :] -= 1
            idx[1:-1, 0] -= 1
            idx[1:-1, -1] -= 1
        return self.colors(idx)

    def colors(self, idx):
        rgb = self.ramp[np.clip(idx, 0, 4)]
        return np.dstack([rgb, np.full(idx.shape, 255, dtype=np.uint8)])

    def solid(self, w, h, index=2):
        return self.colors(np.full((h, w), index, dtype=np.int16))


def rot_axis(axis, degrees):
    c, s = math.cos(math.radians(degrees)), math.sin(math.radians(degrees))
    if axis == "x":
        return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    if axis == "y":
        return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def rot_xyz(rx, ry, rz):
    """Поворот как в Minecraft: сначала вокруг Z, затем Y, затем X."""
    return rot_axis("x", rx) @ rot_axis("y", ry) @ rot_axis("z", rz)


class Element:
    def __init__(self, a, b, mat, faces, rot=None, glow=False):
        self.a, self.b, self.mat, self.faces, self.rot, self.glow = a, b, mat, faces, rot, glow
        self.hidden = set()

    def corners(self):
        pts = np.array([[x, y, z] for x in (self.a[0], self.b[0]) for y in (self.a[1], self.b[1])
                        for z in (self.a[2], self.b[2])], dtype=float)
        if self.rot:
            axis, angle, origin = self.rot
            origin = np.array(origin, dtype=float)
            pts = (pts - origin) @ rot_axis(axis, angle).T + origin
        return pts


class Model:
    """Модель одного предмета.

    kind: 'sword' и 'pickaxe' — предмет в руке (модель стоит вертикально, рукоять внизу,
    центр хвата около y=1.5); 'totem' — фигурка в кубе 16×16×16, лицом на юг (+Z);
    'hat' — шляпа: единица = пиксель скина, голова занимает куб от 4 до 12, лицо смотрит на север (−Z).
    """

    def __init__(self, ident, name, kind, density=2):
        self.id, self.name, self.kind, self.density = ident, name, kind, density
        self.elements = []
        self.gui_rot = None
        self.grip = (8.0, 1.6, 8.0)
        self.center_x = 8.0

    # ── Построение ─────────────────────────────────────────────────────────

    def _face_size(self, a, b, face):
        dx, dy, dz = (b[i] - a[i] for i in range(3))
        w, h = {"north": (dx, dy), "south": (dx, dy), "east": (dz, dy), "west": (dz, dy),
                "up": (dx, dz), "down": (dx, dz)}[face]
        if w <= EPS or h <= EPS:
            return None
        return max(1, int(round(w * self.density))), max(1, int(round(h * self.density)))

    def _apply_art(self, image, rows, key, mat):
        rows = [r for r in rows]
        h, w = image.shape[:2]
        ah, aw = len(rows), max(len(r) for r in rows)
        if h % ah or w % aw or h // ah != w // aw:
            raise ValueError(f"{self.id}: рисунок {aw}×{ah} не подходит к грани {w}×{h} текселей")
        k = h // ah
        for y, row in enumerate(rows):
            for x, ch in enumerate(row.ljust(aw)):
                if ch in EMPTY:
                    continue
                if ch in "01234":
                    color = tuple(mat.ramp[int(ch)])
                else:
                    color = hex_rgb((key or {})[ch])
                image[y * k:(y + 1) * k, x * k:(x + 1) * k, :3] = color

    def box(self, a, b, mat, art=None, key=None, rot=None, mirror=False, glow=None, images=None, side=None):
        """Коробка от угла a до угла b.

        art — рисунки поверх граней: {'north': ["..11..", ...]}; строки идут сверху вниз, как грань
        видна снаружи. Цифры 0–4 — оттенки материала, остальные символы берутся из key ('#rrggbb').
        rot — поворот (ось, угол, центр); угол кратен 22.5 и не больше 45 по модулю.
        mirror=True добавляет зеркальную копию относительно x=8.
        """
        a, b = tuple(map(float, a)), tuple(map(float, b))
        if any(a[i] > b[i] for i in range(3)):
            raise ValueError(f"{self.id}: у коробки {a}–{b} перепутаны углы")
        if min(a) < -16 or max(b) > 32:
            raise ValueError(f"{self.id}: коробка {a}–{b} выходит за пределы от −16 до 32")
        if rot and not rot[1]:
            rot = None
        if rot and (abs(rot[1]) > 45 or (rot[1] / 22.5) % 1):
            raise ValueError(f"{self.id}: угол {rot[1]} недопустим")
        faces = {}
        for face in FACES:
            size = self._face_size(a, b, face)
            if size is None:
                continue
            if images and face in images:
                image = images[face].copy()
            elif side is not None:
                image = mat.solid(size[0], size[1], side)
            else:
                image = mat.paint(size[0], size[1], face)
            if art and face in art:
                self._apply_art(image, art[face], key, mat)
            faces[face] = image
        element = Element(a, b, mat, faces, rot, mat.glow if glow is None else glow)
        self.elements.append(element)
        if mirror:
            cx = self.center_x
            flipped = None
            if art:
                swap = {"east": "west", "west": "east"}
                flipped = {swap.get(f, f): [row[::-1] for row in rows] for f, rows in art.items()}
            mrot = None
            if rot:
                axis, angle, origin = rot
                mrot = (axis, angle if axis == "x" else -angle, (2 * cx - origin[0], origin[1], origin[2]))
            self.box((2 * cx - b[0], a[1], a[2]), (2 * cx - a[0], b[1], b[2]), mat, art=flipped, key=key,
                     rot=mrot, glow=glow, side=side)
        return element

    def sprite(self, rows, key, at, depth, plane="xy", cell=1.0, side=1):
        """Пиксельный рисунок, выдавленный в объём.

        rows — строки рисунка сверху вниз; пробел и точка — пусто. key: символ → Mat или
        {'mat': Mat, 'depth': (от, до)} для деталей другой толщины.
        plane='xy': рисунок смотрит на юг и север, at=(x, y) — левый нижний угол, depth — по Z.
        plane='xz': рисунок лежит горизонтально, at=(x, z) — угол верхней строки, depth — по Y.
        plane='zy': рисунок смотрит на запад и восток, at=(z, y), depth — по X.
        cell — размер клетки. side — оттенок торцов (0–4) или None, чтобы рисовать их материалом.
        Края каждой области получают свет сверху-слева и тень снизу-справа.
        """
        width = max(len(r) for r in rows)
        grid = [r.ljust(width) for r in rows]
        tpc = cell * self.density
        if tpc < 1 or abs(tpc - round(tpc)) > EPS:
            raise ValueError(f"{self.id}: клетка {cell} не кратна текселю")
        tpc = int(round(tpc))
        art = self._sprite_art(grid, key, tpc)
        height = len(grid)
        for ch, col, row, w, h in _greedy(grid):
            spec = key[ch]
            mat = spec["mat"] if isinstance(spec, dict) else spec
            d0, d1 = spec.get("depth", depth) if isinstance(spec, dict) else depth
            piece = art[row * tpc:(row + h) * tpc, col * tpc:(col + w) * tpc]
            u0, u1 = at[0] + col * cell, at[0] + (col + w) * cell
            if plane == "xy":
                v0, v1 = at[1] + (height - row - h) * cell, at[1] + (height - row) * cell
                a, b = (u0, v0, d0), (u1, v1, d1)
                images = {"south": piece, "north": piece[:, ::-1]}
            elif plane == "xz":
                z0, z1 = at[1] + row * cell, at[1] + (row + h) * cell
                a, b = (u0, d0, z0), (u1, d1, z1)
                images = {"up": piece, "down": piece[::-1]}
            elif plane == "zy":
                v0, v1 = at[1] + (height - row - h) * cell, at[1] + (height - row) * cell
                a, b = (d0, v0, u0), (d1, v1, u1)
                images = {"west": piece, "east": piece[:, ::-1]}
            else:
                raise ValueError(plane)
            self.box(a, b, mat, images=images, side=side)

    def _sprite_art(self, grid, key, tpc):
        height, width = len(grid) * tpc, len(grid[0]) * tpc
        chars = np.array([[grid[y // tpc][x // tpc] for x in range(width)] for y in range(height)])
        padded = np.pad(chars, 1, constant_values=" ")
        image = np.zeros((height, width, 4), dtype=np.uint8)
        for ch in set(chars.flatten()):
            if ch in EMPTY:
                continue
            spec = key[ch]
            mat = spec["mat"] if isinstance(spec, dict) else spec
            idx = mat.field(width, height, "sprite")
            inner = padded[1:-1, 1:-1]
            light = (padded[:-2, 1:-1] != inner) | (padded[1:-1, :-2] != inner)
            dark = (padded[2:, 1:-1] != inner) | (padded[1:-1, 2:] != inner)
            idx = idx + (light & ~dark).astype(np.int16) - (dark & ~light).astype(np.int16)
            mask = chars == ch
            image[mask] = mat.colors(idx)[mask]
        return image

    def disc(self, cx, cz, radius, y, mat, hole=0.0, cell=1.0, side=None):
        """Горизонтальный диск или кольцо (hole — внутренний радиус); y=(низ, верх)."""
        n = int(math.ceil(radius * 2 / cell - EPS))
        rows = []
        for j in range(n):
            row = ""
            for i in range(n):
                dist = math.hypot((i + 0.5) * cell - radius, (j + 0.5) * cell - radius)
                row += "o" if hole - EPS <= dist <= radius + EPS else " "
            rows.append(row)
        self.sprite(rows, {"o": mat}, at=(cx - radius, cz - radius), depth=y, plane="xz", cell=cell, side=side)

    # ── Проверки ───────────────────────────────────────────────────────────

    def finish(self):
        """Убирает грани, целиком закрытые соседней коробкой, и ищет наложения граней."""
        plain = [e for e in self.elements if e.rot is None]
        for e in plain:
            for face in e.faces:
                axis, sign = AXIS[face]
                plane = e.b[axis] if sign > 0 else e.a[axis]
                rest = [i for i in range(3) if i != axis]
                for o in plain:
                    if o is e:
                        continue
                    outside = (o.a[axis] <= plane + EPS < o.b[axis]) if sign > 0 else (o.a[axis] < plane - EPS <= o.b[axis])
                    if outside and all(o.a[i] <= e.a[i] + EPS and o.b[i] >= e.b[i] - EPS for i in rest):
                        e.hidden.add(face)
                        e.faces[face] = e.mat.solid(1, 1)
                        break
        warnings = []
        seen = []
        for e in plain:
            for face in e.faces:
                if face in e.hidden:
                    continue
                axis, sign = AXIS[face]
                plane = e.b[axis] if sign > 0 else e.a[axis]
                rest = [i for i in range(3) if i != axis]
                rect = tuple((e.a[i], e.b[i]) for i in rest)
                for other_face, other_plane, other_rect in seen:
                    if other_face == face and abs(other_plane - plane) < EPS and all(
                            min(rect[k][1], other_rect[k][1]) - max(rect[k][0], other_rect[k][0]) > EPS for k in (0, 1)):
                        warnings.append(f"{self.id}: грани «{face}» накладываются в плоскости {plane:g} "
                                        f"({rect} и {other_rect}) — сдвиньте одну из коробок")
                seen.append((face, plane, rect))
        return warnings

    def corners(self):
        return np.concatenate([e.corners() for e in self.elements])

    # ── Экспорт ────────────────────────────────────────────────────────────

    def atlas(self):
        """Собирает грани в одну текстуру: (размер, картинка, положение каждой грани)."""
        unique, lookup = [], {}
        for e in self.elements:
            for face, image in e.faces.items():
                token = (image.shape, image.tobytes())
                if token not in lookup:
                    lookup[token] = len(unique)
                    unique.append(image)
        order = sorted(range(len(unique)), key=lambda i: (-unique[i].shape[0], -unique[i].shape[1]))
        for size in (16, 32, 64, 128, 256, 512):
            x = y = shelf = 0
            pos = {}
            for i in order:
                h, w = unique[i].shape[:2]
                if x + w + 2 > size:
                    x, y, shelf = 0, y + shelf, 0
                if w + 2 > size or y + h + 2 > size:
                    pos = None
                    break
                pos[i] = (x + 1, y + 1)
                x += w + 2
                shelf = max(shelf, h + 2)
            if pos is not None:
                break
        else:
            raise ValueError(f"{self.id}: текстура не помещается в 512×512")
        canvas = np.zeros((size, size, 4), dtype=np.uint8)
        for i, (x, y) in pos.items():
            image = unique[i]
            h, w = image.shape[:2]
            # Поля в один тексель повторяют край, чтобы на стыках не проступал соседний рисунок.
            canvas[y - 1:y + h + 1, x - 1:x + w + 1] = np.pad(image, ((1, 1), (1, 1), (0, 0)), mode="edge")
        rects = {}
        for index, e in enumerate(self.elements):
            for face, image in e.faces.items():
                x, y = pos[lookup[(image.shape, image.tobytes())]]
                rects[(index, face)] = (x, y, x + image.shape[1], y + image.shape[0])
        return size, Image.fromarray(canvas, "RGBA"), rects

    def fit(self, rot, pad=1.0, max_scale=4.0):
        """Преобразование, при котором модель целиком помещается в ячейку 16×16."""
        pts = (self.corners() - 8.0) @ rot_xyz(*rot).T
        lo, hi = pts.min(axis=0), pts.max(axis=0)
        scale = min(max_scale, (16 - 2 * pad) / max(hi[0] - lo[0], hi[1] - lo[1]))
        center = (lo + hi) / 2
        return {"rotation": list(rot), "translation": [_num(-center[0] * scale), _num(-center[1] * scale), 0],
                "scale": [_num(scale)] * 3}

    def _held(self, rot, translation, scale):
        """Положение в руке как у обычного меча, с поправкой на место хвата модели."""
        shift = rot_xyz(*rot) @ (np.array([8.0, 1.6, 8.0]) - np.array(self.grip)) * scale
        return {"rotation": list(rot), "translation": [_num(translation[i] + shift[i]) for i in range(3)],
                "scale": [scale] * 3}

    def gui_rotation(self):
        if self.gui_rot:
            return self.gui_rot
        return {"sword": [0, 0, -45], "pickaxe": [0, 0, -45], "totem": [15, 25, 0], "hat": [20, 205, 0]}[self.kind]

    def display(self):
        gui = self.fit(self.gui_rotation())
        if self.kind in ("sword", "pickaxe"):
            # Углы стандартной модели item/handheld, пересчитанные для вертикально стоящей модели.
            return {
                "thirdperson_righthand": self._held([0, -90, 10], [0, 4, 0.5], 0.85),
                "firstperson_righthand": self._held([0, -90, -20], [1.13, 3.2, 1.13], 0.68),
                "ground": {"rotation": [0, 0, 0], "translation": [0, 2, 0], "scale": [0.5] * 3},
                "gui": gui,
                "fixed": self.fit([0, 180, -45], pad=0.5, max_scale=1.0),
            }
        display = {
            "thirdperson_righthand": {"rotation": [0, 0, 0], "translation": [0, 3, 1], "scale": [0.55] * 3},
            "firstperson_righthand": {"rotation": [0, -90, 25], "translation": [1.13, 3.2, 1.13], "scale": [0.68] * 3},
            "ground": {"rotation": [0, 0, 0], "translation": [0, 2, 0], "scale": [0.5] * 3},
            "gui": gui,
            "fixed": self.fit([0, 0, 0], pad=1.0, max_scale=1.0),
        }
        if self.kind == "hat":
            # Предмет на голове рисуется в масштабе 0.625; 1.6 возвращает «единица = пиксель скина».
            display["head"] = {"rotation": [0, 0, 0], "translation": [0, 0, 0], "scale": [1.6] * 3}
            display["thirdperson_righthand"]["scale"] = [0.4] * 3
            display["firstperson_righthand"]["scale"] = [0.4] * 3
        return display

    def java(self):
        """Модель предмета Minecraft и её текстура."""
        size, texture, rects = self.atlas()
        elements = []
        for index, e in enumerate(self.elements):
            faces = {}
            for face in e.faces:
                if face in e.hidden:
                    continue
                x0, y0, x1, y1 = rects[(index, face)]
                faces[face] = {"uv": [_num(v * 16 / size) for v in (x0, y0, x1, y1)], "texture": "#0"}
            if not faces:
                continue
            item = {"from": [_num(v) for v in e.a], "to": [_num(v) for v in e.b]}
            if e.rot:
                axis, angle, origin = e.rot
                item["rotation"] = {"angle": angle, "axis": axis, "origin": [_num(v) for v in origin]}
            if e.glow:
                item["light_emission"] = 15
                item["shade"] = False
            item["faces"] = faces
            elements.append(item)
        reference = f"{NAMESPACE}:item/{self.id}"
        model = {
            "credit": "AppleCosmetic",
            "texture_size": [size, size],
            "textures": {"0": reference, "particle": reference},
            "gui_light": "front" if self.kind in ("sword", "pickaxe") else "side",
            "elements": elements,
            "display": self.display(),
        }
        return model, texture

    def bbmodel(self, bone="h_head"):
        """Файл Blockbench для BetterModel: шляпа на кости, которая поворачивается вместе с головой."""
        size, texture, rects = self.atlas()
        scale = 0.9375  # модель игрока рисуется в масштабе 15/16

        def point(p):
            # Низ головы (y=4 в модели шляпы) находится на высоте 22.5 от ног игрока.
            return [_num((p[0] - 8) * scale), _num((p[1] - 4) * scale + 22.5), _num((p[2] - 8) * scale)]

        def ident(*parts):
            return str(uuid.uuid5(uuid.NAMESPACE_URL, "/".join(map(str, (NAMESPACE, self.id) + parts))))

        cubes = []
        for index, e in enumerate(self.elements):
            faces = {}
            for face in FACES:
                if face in e.faces:
                    faces[face] = {"uv": list(rects[(index, face)]), "texture": 0}
                else:
                    faces[face] = {"uv": [0, 0, 0, 0], "texture": None}
            center = [(e.a[i] + e.b[i]) / 2 for i in range(3)]
            cube = {
                "name": "cube", "box_uv": False, "render_order": "default", "locked": False,
                "allow_mirror_modeling": True, "from": point(e.a), "to": point(e.b), "autouv": 0, "color": 0,
                "origin": point(e.rot[2] if e.rot else center), "faces": faces, "type": "cube",
                "uuid": ident("cube", index),
            }
            if e.rot:
                cube["rotation"] = [e.rot[1] if e.rot[0] == axis else 0 for axis in "xyz"]
            cubes.append(cube)
        buffer = io.BytesIO()
        texture.save(buffer, "PNG")
        group = ident("bone")
        return {
            "meta": {"format_version": "5.0", "model_format": "free", "box_uv": False},
            "name": self.id,
            "model_identifier": "",
            "visible_box": [1, 1, 0],
            "variable_placeholders": "",
            "variable_placeholder_buttons": [],
            "timeline_setups": [],
            "unhandled_root_fields": {},
            "resolution": {"width": size, "height": size},
            "elements": cubes,
            "groups": [{
                "uuid": group, "export": True, "locked": False, "origin": [0, 22.5, 0], "rotation": [0, 0, 0],
                "color": 0, "name": bone, "children": [], "reset": False, "shade": True, "mirror_uv": False,
                "selected": False, "visibility": True, "autouv": 0, "isOpen": True, "primary_selected": False,
            }],
            "outliner": [{"uuid": group, "isOpen": True, "children": [c["uuid"] for c in cubes]}],
            "textures": [{
                "name": f"{self.id}.png", "path": "", "folder": "", "namespace": "", "id": "0", "group": "",
                "width": size, "height": size, "uv_width": size, "uv_height": size, "particle": False,
                "use_as_default": False, "layers_enabled": False, "sync_to_project": "", "render_mode": "default",
                "render_sides": "auto", "pbr_channel": "color", "frame_time": 1, "frame_order_type": "loop",
                "frame_order": "", "frame_interpolate": False, "visible": True, "internal": True, "saved": False,
                "uuid": ident("texture"),
                "source": "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode(),
            }],
            "animations": [],
        }


def _num(value):
    value = round(float(value), 4)
    return int(value) if value == int(value) else value


def _greedy(grid):
    """Разбивает рисунок на прямоугольники из одинаковых символов: (символ, столбец, строка, ширина, высота)."""
    height, width = len(grid), len(grid[0])
    used = [[False] * width for _ in range(height)]
    out = []
    for r in range(height):
        for c in range(width):
            ch = grid[r][c]
            if ch in EMPTY or used[r][c]:
                continue
            w = 1
            while c + w < width and grid[r][c + w] == ch and not used[r][c + w]:
                w += 1
            h = 1
            while r + h < height and all(grid[r + h][c + i] == ch and not used[r + h][c + i] for i in range(w)):
                h += 1
            for i in range(h):
                for j in range(w):
                    used[r + i][c + j] = True
            out.append((ch, c, r, w, h))
    return out
