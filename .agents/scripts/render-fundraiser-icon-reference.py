"""Render the supplied newsletter for reviewing its kitchen illustration style."""
from pathlib import Path

import fitz


source = Path("attached_assets/2026LaunchNewsletter_TheRecipeReport_1791493786053.pdf")
output = Path("/tmp/fundraiser-icon-reference.png")
with fitz.open(source) as document:
    document[0].get_pixmap(matrix=fitz.Matrix(1.3, 1.3)).save(output)
print(output)
