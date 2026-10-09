"""Apply the fundraiser's retirement rule without requiring a scheduled deploy."""
from datetime import datetime, timezone
from pathlib import Path
import re

_source = (Path(__file__).parent / "assets/fundraiser-lifecycle.mjs").read_text()
END_TIME = datetime.fromisoformat(re.search(r'END_TIME = "([^"]+)"', _source)[1].replace("Z", "+00:00"))
SCRIPT = '<script type="module" src="/assets/fundraiser-lifecycle.mjs"></script>'

def has_ended(now=None):
    return (now or datetime.now(timezone.utc)) >= END_TIME

def retire_content(text):
    text = re.sub(r'<p class="fundraiser-footer-link"[^>]*>[\s\S]*?</p>', '', text)
    text = re.sub(r'<aside\b[^>]*class="fundraiser-announcement"[\s\S]*?</aside>', '', text)
    return re.sub(r'<url>\s*<loc>https://covenantschool\.com/fall-fundraiser</loc>[\s\S]*?</url>', '', text)

def prepare_html(text):
    return text if SCRIPT in text else text.replace("</head>", SCRIPT + "</head>", 1)
