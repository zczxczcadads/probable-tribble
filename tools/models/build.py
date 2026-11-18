"""Собирает модели: набор для ItemsAdder, файлы для BetterModel и листы превью.

    python3 tools/models/build.py                 — все категории
    python3 tools/models/build.py swords hats     — только указанные
    python3 tools/models/build.py --view hat_crown — крупно одну модель с четырёх сторон (в /tmp/ac_preview)
"""
from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

import render  # noqa: E402
from kit import NAMESPACE, Mat, Model  # noqa: E402
from PIL import Image  # noqa: E402

PACK = ROOT / "src/main/resources/pack"
ITEMS_ADDER = PACK / "itemsadder/contents" / NAMESPACE
BETTER_MODEL = PACK / "bettermodel/models"
PREVIEW = ROOT / "docs/preview"
SCRATCH = Path("/tmp/ac_preview")

# категория → (заголовок, предмет-основа в ItemsAdder)
CATEGORIES = {
    "swords": ("Мечи", "DIAMOND_SWORD"),
    "pickaxes": ("Кирки", "DIAMOND_PICKAXE"),
    "totems": ("Тотемы", "TOTEM_OF_UNDYING"),
    "hats": ("Шляпы", "PAPER"),
}


def head_parts():
    """Голова игрока для превью шляп."""
    head = Model("_head", "", "hat", density=1)
    key = {"h": "#3b2a1e", "s": "#c69c7b", "w": "#f4f4f4", "b": "#3f4fb5", "n": "#a87856", "m": "#7d4f3c"}
    side = ["hhhhhhhh", "hhhhhhhh", "hhhhssss", "hhhsssss", "hhssssss", "hsssssss", "ssssssss", "ssssssss"]
    head.box((4, 4, 4), (12, 12, 12), Mat("flat", "#c69c7b"), key=key, art={
        "north": ["hhhhhhhh", "hhhhhhhh", "hssssssh", "ssssssss", "swbssbws", "sssnnsss", "ssmmmmss", "ssssssss"],
        "south": ["hhhhhhhh"] * 6 + ["ssssssss"] * 2,
        "west": [row[::-1] for row in side],
        "east": side,
        "up": ["hhhhhhhh"] * 8,
        "down": ["ssssssss"] * 8,
    })
    model, texture = head.java()
    return render.quads(model, texture)


def picture(model, data, texture, rotation=None, size=256):
    """Картинка модели: значок как в инвентаре, шляпа — на голове."""
    parts = render.quads(data, texture)
    light = data.get("gui_light", "side")
    if model.kind == "hat":
        rotation = rotation or model.gui_rotation()
        parts = head_parts() + parts
        scale, shift = render.fit(parts, rotation)
        return render.draw(parts, rotation, scale, shift, size=size, light="side")
    if rotation is None:
        gui = data["display"]["gui"]
        return render.draw(parts, gui["rotation"], gui["scale"][0], gui["translation"], size=size, light=light)
    scale, shift = render.fit(parts, rotation)
    return render.draw(parts, rotation, scale, shift, size=size, light="side")


def load(category):
    module = importlib.import_module(f"defs.{category}")
    return module.build()


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")


def build(category):
    title, material = CATEGORIES[category]
    models = load(category)
    # Файлы моделей, которых больше нет в описании, удаляются.
    prefix = models[0].id.split("_")[0] + "_"
    for folder, pattern in ((ITEMS_ADDER / "models/item", f"{prefix}*.json"),
                            (ITEMS_ADDER / "textures/item", f"{prefix}*.png"),
                            (BETTER_MODEL, f"ac_{prefix}*.bbmodel")):
        for stale in folder.glob(pattern):
            stale.unlink()
    tiles, problems = [], []
    lines = [
        f"# Модели AppleCosmetic: {title.lower()}.",
        "# Файл создан tools/models/build.py вместе с моделями и текстурами этого набора.",
        "info:",
        f"  namespace: {NAMESPACE}",
        "items:",
    ]
    for model in models:
        problems += model.finish()
        data, texture = model.java()
        write_json(ITEMS_ADDER / "models/item" / f"{model.id}.json", data)
        (ITEMS_ADDER / "textures/item").mkdir(parents=True, exist_ok=True)
        texture.save(ITEMS_ADDER / "textures/item" / f"{model.id}.png")
        lines += [f"  {model.id}:", f"    name: \"{model.name}\"", f"    material: {material}",
                  "    graphics:", f"      model: item/{model.id}"]
        if model.kind == "hat":
            write_json(BETTER_MODEL / f"ac_{model.id}.bbmodel", model.bbmodel())
        tiles.append((picture(model, data, texture), model.name))
        print(f"  {model.id}: коробок {len(data['elements'])}, текстура {texture.size[0]}×{texture.size[1]}")
    (ITEMS_ADDER / "configs").mkdir(parents=True, exist_ok=True)
    (ITEMS_ADDER / "configs" / f"{category}.yml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    PREVIEW.mkdir(parents=True, exist_ok=True)
    render.sheet(title, tiles, path=PREVIEW / f"{category}.png")
    for problem in problems:
        print("  ВНИМАНИЕ:", problem)
    return len(models), problems


def view(ident):
    """Одна модель крупно: значок, вид спереди, сбоку и сзади-сверху."""
    # Категория определяется по началу имени: sword_ → swords, hat_ → hats.
    category = ident.split("_")[0] + "s"
    if category not in CATEGORIES:
        raise SystemExit(f"Модель «{ident}» не найдена")
    for category in (category,):
        for model in load(category):
            if model.id != ident:
                continue
            for problem in model.finish():
                print("ВНИМАНИЕ:", problem)
            data, texture = model.java()
            front = [0, 180, 0] if model.kind == "hat" else [0, 0, 0]
            views = [None, front, [0, front[1] + 90, 0], [25, front[1] + 215, 0]]
            canvas = Image.new("RGBA", (768, 768), (32, 35, 46, 255))
            for index, rotation in enumerate(views):
                canvas.alpha_composite(picture(model, data, texture, rotation, size=384),
                                       ((index % 2) * 384, (index // 2) * 384))
            SCRATCH.mkdir(parents=True, exist_ok=True)
            canvas.convert("RGB").save(SCRATCH / f"{ident}.png")
            texture.resize((texture.size[0] * 4, texture.size[1] * 4), Image.NEAREST).save(SCRATCH / f"{ident}_texture.png")
            print(f"{SCRATCH / (ident + '.png')}: коробок {len(data['elements'])}, текстура {texture.size[0]}px")
            return
    raise SystemExit(f"Модель «{ident}» не найдена")


def main(argv):
    if argv[:1] == ["--view"]:
        for ident in argv[1:]:
            view(ident)
        return
    chosen = argv or list(CATEGORIES)
    total, problems = 0, []
    for category in chosen:
        print(f"{CATEGORIES[category][0]}:")
        count, found = build(category)
        total += count
        problems += found
    print(f"Готово: моделей {total}, замечаний {len(problems)}")
    if problems:
        raise SystemExit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
