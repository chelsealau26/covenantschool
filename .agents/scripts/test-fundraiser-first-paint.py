"""Check that the finished design does not depend on post-load replacements."""
from html.parser import HTMLParser
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
html = (ROOT / "pages/fall-fundraiser.html").read_text()

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_head = False
        self.in_footer = False
        self.before_main = True
        self.logos = []
        self.hero = []
        self.styles = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "head": self.in_head = True
        if tag == "footer": self.in_footer = True
        if tag == "main": self.before_main = False
        if tag == "body": assert "fundraiser-route" in attrs["class"].split()
        if tag == "style":
            assert self.in_head or self.in_footer, "Final styles must precede first paint."
            self.styles.append(attrs.get("id"))
        if tag == "img":
            if self.before_main: self.logos.append(attrs.get("src", ""))
            if "recipe-hero-izzy" in attrs.get("class", "").split(): self.hero.append(attrs)
    def handle_endtag(self, tag):
        if tag == "head": self.in_head = False
        if tag == "footer": self.in_footer = False

page = Page()
page.feed(html)
assert len(page.logos) == 3
assert all(src == "/assets/fundraiser-header-logo-transparent.png" for src in page.logos)
assert len(page.hero) == 1
assert page.hero[0]["width"] == "324" and page.hero[0]["height"] == "411"
assert "fundraiser-sticky-header" in page.styles
assert "fundraiser-newsletter-palette" in page.styles
assert "img.setAttribute('src','/assets/fundraiser-header-logo-transparent.png')" not in html
assert "Inactive previous inline encoding" not in html
assets = set(re.findall(r'/assets/[^"\s)<]+', html))
for asset in assets:
    source = ROOT / asset.lstrip("/")
    exported = ROOT / "dist" / asset.lstrip("/")
    assert source.is_file(), asset
    assert exported.is_file(), f"Missing from static deployment: {asset}"
    assert source.read_bytes() == exported.read_bytes(), f"Stale build asset: {asset}"
for name in ("cj-machine.jpg", "facts.png", "joe-cowart.png", "little-monkey-toes.png", "mw-counseling.jpg"):
    assert f"/assets/fundraiser-sponsors/{name}" in assets
print("PASS: initial header/hero markup, early final styles, and complete static sponsor/image assets.")
