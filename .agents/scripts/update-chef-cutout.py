"""Embed the clean mascot PNG in both fundraiser image locations."""
import base64
import re
from pathlib import Path

page = Path("pages/fall-fundraiser.html")
image = Path("assets/fundraiser-chef-izzy-transparent.png")
data_url = "data:image/png;base64," + base64.b64encode(image.read_bytes()).decode()
count = 0


def replace_image(match):
    global count
    tag = match.group()
    if 'alt="Chef Izzy' not in tag:
        return tag
    count += 1
    return re.sub(r'src="[^"]*"', lambda _: f'src="{data_url}"', tag)


updated = re.sub(r"<img\b[^>]*>", replace_image, page.read_text())
assert count == 2, f"Expected two mascot images, found {count}"
page.write_text(updated)
print("Updated both Chef Izzy images.")
