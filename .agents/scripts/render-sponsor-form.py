from pathlib import Path
import fitz

source = Path("attached_assets/Covenant_Corporate_Sponsor_Form_-2026REVISED_1791493623697.pdf")
output = Path(".agents/outputs")
output.mkdir(parents=True, exist_ok=True)
with fitz.open(source) as document:
    document[0].get_pixmap(matrix=fitz.Matrix(1.5, 1.5)).save(output / "sponsor-form.png")
