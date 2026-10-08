"""Reduce oversized embedded images without removing text or links."""
from pathlib import Path
import fitz

source = Path("attached_assets/2026LaunchNewsletter_TheRecipeReport_1791493786053.pdf")
target = Path("pdfs/fall-fundraiser-parent-newsletter-2026.pdf")
document = fitz.open(source)
processed = set()
for page in document:
    for image in page.get_images(full=True):
        xref, width, height = image[0], image[2], image[3]
        if xref in processed or max(width, height) < 2000:
            continue
        processed.add(xref)
        pixmap = fitz.Pixmap(document, xref)
        if pixmap.colorspace and pixmap.colorspace.n != 3:
            pixmap = fitz.Pixmap(fitz.csRGB, pixmap)
        while max(pixmap.width, pixmap.height) > 1800:
            pixmap.shrink(1)
        if pixmap.alpha:
            pixmap = fitz.Pixmap(pixmap, 0)
        page.replace_image(xref, stream=pixmap.tobytes("jpeg", jpg_quality=85))
document.save(target, garbage=4, deflate=True)
document.close()
print(f"Prepared newsletter: {target.stat().st_size:,} bytes")
