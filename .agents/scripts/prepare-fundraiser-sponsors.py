"""Prepare display-sized copies of supplied sponsor logos without changing artwork."""
from pathlib import Path
import json
import pymupdf

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / ".agents/outputs/fundraiser-sponsors"
OUT.mkdir(parents=True, exist_ok=True)
ASSETS = ROOT / "attached_assets"


def prepare(pixmap, identifier):
    if pixmap.colorspace.n != 3:
        pixmap = pymupdf.Pixmap(pymupdf.csRGB, pixmap)
    samples = pixmap.samples
    channels = pixmap.n
    xmin, ymin, xmax, ymax = pixmap.width, pixmap.height, -1, -1
    for y in range(pixmap.height):
        for x in range(pixmap.width):
            offset = (y * pixmap.width + x) * channels
            r, g, b = samples[offset:offset + 3]
            alpha = samples[offset + 3] if pixmap.alpha else 255
            if alpha > 12 and not (r >= 248 and g >= 248 and b >= 248):
                xmin, ymin = min(xmin, x), min(ymin, y)
                xmax, ymax = max(xmax, x), max(ymax, y)
    if xmax < xmin:
        raise ValueError(f"No visible artwork in {identifier}")
    rect = pymupdf.IRect(
        max(0, xmin - 5), max(0, ymin - 5),
        min(pixmap.width, xmax + 6), min(pixmap.height, ymax + 6),
    )
    cropped = pymupdf.Pixmap(pymupdf.csRGB, rect, pixmap.alpha)
    cropped.clear_with(0)
    cropped.copy(pixmap, rect)
    scale = min(1, 400 / max(cropped.width, cropped.height))
    if scale < 1:
        cropped = pymupdf.Pixmap(
            cropped, max(1, round(cropped.width * scale)),
            max(1, round(cropped.height * scale)),
        )
    opaque = not cropped.alpha or all(a == 255 for a in cropped.samples[3::4])
    if opaque:
        if cropped.alpha:
            cropped = pymupdf.Pixmap(cropped, 0)
        path = OUT / f"{identifier}.jpg"
        path.write_bytes(cropped.tobytes("jpeg", jpg_quality=90))
    else:
        path = OUT / f"{identifier}.png"
        cropped.save(path)
    return {
        "id": identifier, "logoPath": str(path.relative_to(ROOT)),
        "width": cropped.width, "height": cropped.height,
    }


pdf = pymupdf.open(ASSETS / "CJ_Machine_Logo_Smaller_1791504525762.pdf")
pdf[0].get_pixmap(matrix=pymupdf.Matrix(1.5, 1.5)).save(OUT / "cj-pdf-preview.png")
images = pdf[0].get_images(full=True)
if len(images) != 1:
    raise ValueError("Expected one supplied C & J Machine logo in the PDF.")
specs = [
    ("cj-machine", "C & J Machine", pymupdf.Pixmap(pdf, images[0][0])),
    ("facts", "FACTS", pymupdf.Pixmap(str(ASSETS / "FACTS_Logo_1791504525762.png"))),
    ("joe-cowart", "Joe Cowart, Inc.", pymupdf.Pixmap(str(ASSETS / "Joe_Cowart_Inc._1791504525762.png"))),
    ("little-monkey-toes", "Little Monkey Toes", pymupdf.Pixmap(str(ASSETS / "Little_Monkey_Toes_1791504525763.png"))),
    ("mw-counseling", "MW Counseling, LLC", pymupdf.Pixmap(str(ASSETS / "Unknown_1791504525763.png"))),
]
manifest = []
for identifier, name, pixmap in specs:
    entry = prepare(pixmap, identifier)
    entry["name"] = name
    manifest.append(entry)
    print(name, entry["width"], entry["height"], entry["logoPath"])
(OUT / "manifest.json").write_text(json.dumps(manifest, indent=2))
