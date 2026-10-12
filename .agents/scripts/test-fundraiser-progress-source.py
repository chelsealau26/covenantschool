"""Both pages receive one confirmed source; expiry removes the welcome markup."""
import json
from pathlib import Path
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from fundraiser_lifecycle import prepare_html, retire_content
from fundraiser_progress import SOURCE

def config(text):
    import re
    return json.loads(re.search(r'id="fundraiser-school-progress">(.*?)</script>', text)[1])

home = (ROOT / "pages/index.html").read_text()
fundraiser = (ROOT / "pages/fall-fundraiser.html").read_text()
assert config(prepare_html(home)) == config(prepare_html(fundraiser)) == json.loads(SOURCE.read_text())
assert 'id="fundraiser-welcome"' not in retire_content(prepare_html(home))
with patch("fundraiser_progress.SOURCE") as source:
    source.read_text.return_value = '{"goal":60000,"raised":15000,"updatedAt":null}'
    rendered = prepare_html(fundraiser)
    assert config(prepare_html(home)) == config(rendered)
    assert 'class="goal-amount">$60,000' in rendered
    assert '$15,000 raised · 25%' in rendered
    assert 'aria-valuemax="60000"' in rendered
    assert '<span>$45,000</span>' in rendered
print("PASS shared progress, updated initial jug text/ticks/ARIA, and server popup removal")
