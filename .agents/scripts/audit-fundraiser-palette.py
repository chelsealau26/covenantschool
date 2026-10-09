"""Render supplied brand references and report their frequent color values."""
from pathlib import Path
from collections import Counter
import fitz

out = Path("/tmp/fundraiser-brand-reference")
out.mkdir(exist_ok=True)
newsletter = fitz.open("attached_assets/2026LaunchNewsletter_TheRecipeReport_1791493786053.pdf")
colors = Counter()
for index, page in enumerate(newsletter):
    for drawing in page.get_drawings():
        for key in ("fill", "color"):
            rgb = drawing.get(key)
            if rgb and len(rgb) == 3:
                colors["#" + "".join(f"{round(v * 255):02x}" for v in rgb)] += 1
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                colors[f"#{span['color']:06x}"] += len(span["text"])
    if index < 2:
        page.get_pixmap(matrix=fitz.Matrix(1100 / page.rect.width, 1100 / page.rect.width)).save(out / f"newsletter-{index + 1}.png")
print("Newsletter pages:", len(newsletter))
print("Frequent source vector/text colors:", colors.most_common(16))
logo = fitz.open("attached_assets/Recipe_for_Success_overalllogo_1791493623697.jpg")
page = logo[0]
pix = page.get_pixmap(matrix=fitz.Matrix(600 / page.rect.width, 600 / page.rect.width), alpha=False)
pix.save(out / "logo.png")
rgb = pix.samples
bins = Counter(tuple(min(255, round(value / 8) * 8) for value in rgb[i:i+3]) for i in range(0, len(rgb), 3))
print("Logo frequent RGB buckets:", bins.most_common(12))
