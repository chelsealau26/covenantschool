"""Assemble the complete static site, including local images and downloads."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "dist"
if OUTPUT.is_symlink():
    raise RuntimeError("Refusing to replace a symlink at the build destination.")
OUTPUT.mkdir(exist_ok=True)
shutil.copytree(ROOT / "pages", OUTPUT, dirs_exist_ok=True)
for folder in ("assets", "pdfs"):
    shutil.copytree(ROOT / folder, OUTPUT / folder, dirs_exist_ok=True)
print("Built dist/ with all pages, images and PDF downloads.")
