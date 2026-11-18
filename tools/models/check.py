"""Проверяет собранный набор: модели укладываются в ограничения Minecraft, текстуры на месте."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "src/main/resources/pack"
ITEMS_ADDER = PACK / "itemsadder/contents/applecosmetic"
BETTER_MODEL = PACK / "bettermodel/models"
CONTEXTS = {"thirdperson_righthand", "thirdperson_lefthand", "firstperson_righthand", "firstperson_lefthand",
            "gui", "head", "ground", "fixed"}


def check_model(path, problems):
    data = json.loads(path.read_text(encoding="utf-8"))
    name = path.stem

    def bad(text):
        problems.append(f"{name}: {text}")

    texture = data["textures"]["0"]
    namespace, rel = texture.split(":")
    image_path = ITEMS_ADDER / "textures" / f"{rel}.png"
    if namespace != "applecosmetic" or not image_path.is_file():
        bad(f"нет текстуры {texture}")
        return
    with Image.open(image_path) as image:
        if image.size[0] != image.size[1] or image.size[0] & (image.size[0] - 1) or image.size[0] > 256:
            bad(f"размер текстуры {image.size}")
    if not data["elements"]:
        bad("нет коробок")
    for element in data["elements"]:
        if min(element["from"]) < -16 or max(element["to"]) > 32:
            bad(f"коробка вне пределов: {element['from']}–{element['to']}")
        if any(a > b for a, b in zip(element["from"], element["to"])):
            bad("перепутаны углы коробки")
        rotation = element.get("rotation")
        if rotation and (rotation["angle"] not in (-45, -22.5, 22.5, 45) or rotation["axis"] not in "xyz"):
            bad(f"поворот {rotation}")
        if not 0 <= element.get("light_emission", 0) <= 15:
            bad("light_emission")
        if not element["faces"]:
            bad("коробка без граней")
        for face, spec in element["faces"].items():
            if face not in ("north", "south", "east", "west", "up", "down") or spec["texture"] != "#0":
                bad(f"грань {face}")
            if len(spec["uv"]) != 4 or min(spec["uv"]) < 0 or max(spec["uv"]) > 16:
                bad(f"UV {spec['uv']}")
    for context, transform in data["display"].items():
        if context not in CONTEXTS:
            bad(f"неизвестное положение {context}")
        if max(map(abs, transform.get("translation", [0]))) > 80 or max(map(abs, transform.get("scale", [1]))) > 4:
            bad(f"{context}: сдвиг или масштаб вне пределов")


def main():
    problems = []
    models = sorted((ITEMS_ADDER / "models/item").glob("*.json"))
    for path in models:
        check_model(path, problems)
    listed = set()
    for config in sorted((ITEMS_ADDER / "configs").glob("*.yml")):
        lines = config.read_text(encoding="utf-8").splitlines()
        for index, line in enumerate(lines):
            if line.strip().startswith("model: item/"):
                listed.add(line.split("item/")[1].strip())
    names = {path.stem for path in models}
    if listed != names:
        problems.append(f"конфиги и модели расходятся: {sorted(listed ^ names)}")
    hats = {path.stem.removeprefix("ac_") for path in BETTER_MODEL.glob("ac_*.bbmodel")}
    if hats != {name for name in names if name.startswith("hat_")}:
        problems.append(f"модели BetterModel расходятся со шляпами: {sorted(hats)}")
    for path in BETTER_MODEL.glob("*.bbmodel"):
        data = json.loads(path.read_text(encoding="utf-8"))
        if any(face["texture"] is None for cube in data["elements"] for face in cube["faces"].values()):
            problems.append(f"{path.stem}: в модели есть плоская коробка без текстуры на грани")
    for problem in problems:
        print("ОШИБКА:", problem)
    print(f"Проверено моделей: {len(models)}, шляп для BetterModel: {len(hats)}, ошибок: {len(problems)}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
