"""Assemble the complete static site, including local images and downloads."""
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from fundraiser_lifecycle import prepare_html
OUTPUT = ROOT / "dist"
if OUTPUT.is_symlink():
    raise RuntimeError("Refusing to replace a symlink at the build destination.")
OUTPUT.mkdir(exist_ok=True)
shutil.copytree(ROOT / "pages", OUTPUT, dirs_exist_ok=True)
for folder in ("assets", "pdfs"):
    shutil.copytree(ROOT / folder, OUTPUT / folder, dirs_exist_ok=True)
for page in OUTPUT.glob("*.html"):
    page.write_text(prepare_html(page.read_text()))
print("Built dist/ with all pages, images and PDF downloads.")
