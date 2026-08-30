#!/usr/bin/env python3
"""Regression checks for the bundled rune-stash screenshots."""

from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image

from d2r_runewords import DEFAULT_CFG, RUNES, analyze_image


def scan(path):
    return analyze_image(path, dict(DEFAULT_CFG))


def expected_more_runes():
    values = {}
    for line in Path("d2rmorerunes.txt").read_text().splitlines():
        fields = line.split()
        if len(fields) == 2 and fields[1].isdigit():
            rune = next(r for r in RUNES if r.casefold() == fields[0].casefold())
            values[rune] = int(fields[1])
    return {r: n for r in RUNES if (n := values.get(r, 0))}


if __name__ == "__main__":
    result = scan("d2rmorerunes.png")
    assert result["owned"] == expected_more_runes()
    assert [(s["rune"], s["x0"], s["y0"]) for s in result["stats"][-6:]] == [
        ("Lo", 177, 396), ("Sur", 229, 396),
        ("Ber", 541, 396), ("Jah", 593, 396),
        ("Cham", 177, 448), ("Zod", 593, 448),
    ]
    with TemporaryDirectory() as tmp:
        high_rune = Path(tmp) / "ber.png"
        image = Image.open("d2rmorerunes.png")
        image.paste(image.crop((177, 240, 223, 285)), (541, 396))
        image.save(high_rune)
        assert scan(high_rune)["owned"]["Ber"] == 5

    nine = scan("testing9.png")["owned"]
    assert (nine["Tir"], nine["Ith"]) == (9, 9)

    assert scan("d2screenshot.png")["owned"] == {
        "El": 2, "Eld": 1, "Nef": 1, "Eth": 3, "Ith": 1, "Ral": 2,
        "Ort": 2, "Thul": 2, "Amn": 1, "Sol": 1, "Shael": 1,
        "Dol": 1, "Fal": 1,
    }
    print("rune detection OK")
