"""Make the reviewed fundraiser HTML independent of local image hosting."""
import base64
from pathlib import Path
import re

page = Path("pages/fall-fundraiser.html")
html = page.read_text()
campaign = re.search(r'<img src="(data:image/jpeg;base64,[^"]+)"', html).group(1)
html = re.sub(r'<template id="legacy-fundraiser">.*?</template>', '', html, flags=re.S)
html = re.sub(r'<script type="text/plain".*?</script>', '', html, flags=re.S)
html = re.sub(
    r'(<img class="recipe-hero-logo" src=")[^"]+(" alt=")[^"]+',
    lambda match: match[1] + campaign + match[2] +
    'Covenant Christian School 2026 Eagles — Recipe for Success, Family Fun Day',
    html,
)
for src, path, kind in [
    ("../assets/fundraiser-chef-izzy.png", "/tmp/fun-chef.jpg", "jpeg"),
    ("../assets/Covenant_School_Logo_Blue2x-9538467.png", "/tmp/school-brand-small.png", "png"),
]:
    encoded = base64.b64encode(Path(path).read_bytes()).decode()
    html = html.replace(src, f"data:image/{kind};base64,{encoded}")
page.write_text(html)
