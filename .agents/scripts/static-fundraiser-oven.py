"""Keep the decorative oven visible without JavaScript; JS only animates it."""
import re
from pathlib import Path

page = Path("pages/fall-fundraiser.html")
source = page.read_text()
assignment = re.search(r"^  card\.innerHTML='(.*)';$", source, re.M)
assert assignment, "Oven markup assignment not found"
markup = '<div class="recipe-photo-card recipe-oven-card">' + assignment[1] + "</div>"
pattern = r'(<section class="recipe-section paper" id="the-need"><div class="recipe-wrap recipe-story">)<div class="recipe-photo-card">.*?(?=<div class="recipe-story-copy">)'
source, count = re.subn(pattern, lambda match: match[1] + markup, source, count=1, flags=re.S)
assert count == 1, "Expected one mascot card to replace"
source = source.replace(assignment[0] + "\n", "").replace(
    "  card.className='recipe-photo-card recipe-oven-card';\n", ""
)
page.write_text(source)
print("Decorative oven markup is now static; animation remains progressive enhancement.")
