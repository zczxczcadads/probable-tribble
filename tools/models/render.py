"""Простой программный рендер моделей предметов Minecraft для картинок-превью."""
from __future__ import annotations

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from kit import AXIS, rot_axis, rot_xyz

LIGHT = np.array([-0.4, 0.8, 0.45]) / np.linalg.norm([-0.4, 0.8, 0.45])
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def quads(model, texture):
    """Грани модели: (вершины 4×3, UV 4×2, текстура, нормаль, светится ли)."""
    pixels = np.asarray(texture.convert("RGBA"))
    out = []
    for element in model["elements"]:
        (x0, y0, z0), (x1, y1, z1) = element["from"], element["to"]
        # Порядок вершин и привязка UV — как в Minecraft.
        corners = {
            "north": [(x1, y1, z0), (x1, y0, z0), (x0, y0, z0), (x0, y1, z0)],
            "south": [(x0, y1, z1), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1)],
            "west": [(x0, y1, z0), (x0, y0, z0), (x0, y0, z1), (x0, y1, z1)],
            "east": [(x1, y1, z1), (x1, y0, z1), (x1, y0, z0), (x1, y1, z0)],
            "up": [(x0, y1, z0), (x0, y1, z1), (x1, y1, z1), (x1, y1, z0)],
            "down": [(x0, y0, z1), (x0, y0, z0), (x1, y0, z0), (x1, y0, z1)],
        }
        turn, origin = np.eye(3), np.zeros(3)
        if "rotation" in element:
            rotation = element["rotation"]
            turn, origin = rot_axis(rotation["axis"], rotation["angle"]), np.array(rotation["origin"], dtype=float)
        for face, spec in element["faces"].items():
            verts = (np.array(corners[face], dtype=float) - origin) @ turn.T + origin
            u0, v0, u1, v1 = spec["uv"]
            uv = np.array([(u0, v0), (u0, v1), (u1, v1), (u1, v0)], dtype=float)
            axis, sign = AXIS[face]
            normal = np.zeros(3)
            normal[axis] = sign
            out.append((verts, uv, pixels, turn @ normal, element.get("light_emission", 0) > 0))
    return out


def draw(parts, rotation, scale, translation, size=256, supersample=3, light="side"):
    """Рисует грани в ортогональной проекции, как в ячейке инвентаря (16 единиц на всю ширину)."""
    n = size * supersample
    color = np.zeros((n, n, 4), dtype=np.float32)
    depth = np.full((n, n), -np.inf, dtype=np.float32)
    turn = rot_xyz(*rotation)
    for verts, uv, pixels, normal, emissive in parts:
        view = (verts - 8.0) @ turn.T * scale + np.array(translation, dtype=float)
        facing = turn @ normal
        if facing[2] <= 1e-6:
            continue
        shade = 1.0 if (light == "front" or emissive) else min(1.0, 0.66 + 0.42 * max(0.0, float(facing @ LIGHT)))
        sx = (view[:, 0] / 16 + 0.5) * n
        sy = (0.5 - view[:, 1] / 16) * n
        th, tw = pixels.shape[:2]
        for i, j, k in ((0, 1, 2), (0, 2, 3)):
            xs, ys = sx[[i, j, k]], sy[[i, j, k]]
            lo_x, hi_x = max(int(np.floor(xs.min())), 0), min(int(np.ceil(xs.max())), n - 1)
            lo_y, hi_y = max(int(np.floor(ys.min())), 0), min(int(np.ceil(ys.max())), n - 1)
            if lo_x > hi_x or lo_y > hi_y:
                continue
            area = (xs[1] - xs[0]) * (ys[2] - ys[0]) - (xs[2] - xs[0]) * (ys[1] - ys[0])
            if abs(area) < 1e-9:
                continue
            py, px = np.mgrid[lo_y:hi_y + 1, lo_x:hi_x + 1]
            px, py = px + 0.5, py + 0.5
            w0 = ((xs[1] - px) * (ys[2] - py) - (xs[2] - px) * (ys[1] - py)) / area
            w1 = ((xs[2] - px) * (ys[0] - py) - (xs[0] - px) * (ys[2] - py)) / area
            w2 = 1 - w0 - w1
            inside = (w0 >= -1e-6) & (w1 >= -1e-6) & (w2 >= -1e-6)
            z = w0 * view[i, 2] + w1 * view[j, 2] + w2 * view[k, 2]
            tu = w0 * uv[i, 0] + w1 * uv[j, 0] + w2 * uv[k, 0]
            tv = w0 * uv[i, 1] + w1 * uv[j, 1] + w2 * uv[k, 1]
            # Небольшой отступ от края прямоугольника, чтобы не захватить соседний тексель.
            u_lo, u_hi = uv[:, 0].min(), uv[:, 0].max()
            v_lo, v_hi = uv[:, 1].min(), uv[:, 1].max()
            tx = np.clip(np.floor(np.clip(tu, u_lo + 1e-4, u_hi - 1e-4) / 16 * tw).astype(int), 0, tw - 1)
            ty = np.clip(np.floor(np.clip(tv, v_lo + 1e-4, v_hi - 1e-4) / 16 * th).astype(int), 0, th - 1)
            sample = pixels[ty, tx].astype(np.float32) / 255
            block_depth = depth[lo_y:hi_y + 1, lo_x:hi_x + 1]
            block_color = color[lo_y:hi_y + 1, lo_x:hi_x + 1]
            visible = inside & (z > block_depth) & (sample[..., 3] > 0.5)
            block_depth[visible] = z[visible]
            lit = sample.copy()
            lit[..., :3] *= shade
            block_color[visible] = lit[visible]
    premultiplied = color.copy()
    premultiplied[..., :3] *= color[..., 3:4]
    small = premultiplied.reshape(size, supersample, size, supersample, 4).mean(axis=(1, 3))
    alpha = small[..., 3:4]
    small[..., :3] = np.where(alpha > 0, small[..., :3] / np.maximum(alpha, 1e-6), 0)
    return Image.fromarray(np.clip(small * 255, 0, 255).astype(np.uint8), "RGBA")


def fit(parts, rotation, pad=1.2):
    """Масштаб и сдвиг, при которых все грани помещаются в кадр."""
    turn = rot_xyz(*rotation)
    pts = np.concatenate([(verts - 8.0) @ turn.T for verts, *_ in parts])
    lo, hi = pts.min(axis=0), pts.max(axis=0)
    scale = (16 - 2 * pad) / max(hi[0] - lo[0], hi[1] - lo[1])
    center = (lo + hi) / 2
    return scale, [-center[0] * scale, -center[1] * scale, 0]


def sheet(title, tiles, columns=5, cell=256, path=None):
    """Лист превью: плитки (картинка, подпись) в сетке с заголовком."""
    gap, label, head = 14, 40, 64
    rows = (len(tiles) + columns - 1) // columns
    width = gap + columns * (cell + gap)
    height = head + rows * (cell + label + gap) + gap
    canvas = Image.new("RGBA", (width, height), (24, 26, 34, 255))
    pen = ImageDraw.Draw(canvas)
    pen.text((gap + 4, 16), title, font=ImageFont.truetype(FONT_BOLD, 30), fill=(240, 240, 245))
    font = ImageFont.truetype(FONT, 17)
    for index, (image, text) in enumerate(tiles):
        x = gap + (index % columns) * (cell + gap)
        y = head + (index // columns) * (cell + label + gap)
        pen.rounded_rectangle((x, y, x + cell, y + cell + label), radius=12, fill=(40, 44, 58), outline=(70, 76, 96))
        canvas.alpha_composite(image.resize((cell, cell), Image.LANCZOS) if image.size != (cell, cell) else image, (x, y))
        box = pen.textbbox((0, 0), text, font=font)
        pen.text((x + (cell - (box[2] - box[0])) / 2, y + cell + 9), text, font=font, fill=(225, 228, 238))
    if path:
        canvas.convert("RGB").save(path)
    return canvas
