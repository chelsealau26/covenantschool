"""One school-confirmed source for preview and exported campaign progress."""
import json
import math
import re
from datetime import date
from pathlib import Path

SOURCE = Path(__file__).parent / "assets/fundraiser-progress.json"
STAT_KEYS = ("studentsRegisteredPercent", "participantsDonatingPercent")


def prepare_progress(text):
    if 'id="fundraiser-school-progress"' not in text:
        return text
    data = json.loads(SOURCE.read_text())
    goal, raised = data["goal"], data["raised"]
    if not all(isinstance(n, (int, float)) and not isinstance(n, bool)
               and math.isfinite(n) for n in (goal, raised)) or goal <= 0 or raised < 0:
        raise ValueError("Campaign progress requires a positive goal and nonnegative confirmed total.")
    for key in STAT_KEYS:
        value = data.get(key)
        if value is not None and (isinstance(value, bool) or not isinstance(value, (int, float))
                                  or not math.isfinite(value) or not 0 <= value <= 100):
            raise ValueError(f"{key} must be a percentage from 0 to 100.")
    updated = data.get("updatedAt")
    updated_text = ""
    if updated:
        day = date.fromisoformat(updated)
        updated_text = f"Updated {day:%B} {day.day}, {day.year}"
    money = lambda n: "$" + f"{n:,.2f}".rstrip("0").rstrip(".")
    pct = f"{raised / goal * 100:.1f}".rstrip("0").rstrip(".")
    text = re.sub(r'(<script type="application/json" id="fundraiser-school-progress">).*?(</script>)',
                  lambda m: m[1] + json.dumps(data).replace("<", "\\u003c") + m[2], text)
    text = re.sub(r'(<strong class="goal-amount"[^>]*>)[^<]*',
                  lambda m: m[1] + money(goal), text)
    text = re.sub(r'(<p[^>]+data-school-goal-total[^>]*>)[^<]*',
                  lambda m: m[1] + f"{money(raised)} raised · {pct}% of our goal", text)
    text = re.sub(r'(<div class="measuring-levels"[^>]*>)([\s\S]*?)(</div>\s*<svg)',
                  lambda m: m[1] + "".join(
                      f'<div class="measuring-level"><span>{money(goal * ratio)}</span><i></i></div>'
                      for ratio in (1, .75, .5, .25, 0)) + m[3], text)
    def update_line(match):
        tag = match[1].replace(" hidden", "") if updated_text else (
            match[1] if " hidden" in match[1] else match[1][:-1] + " hidden>")
        return tag + updated_text
    text = re.sub(r'(<p[^>]+data-school-goal-date[^>]*>)[^<]*', update_line, text)
    for key in STAT_KEYS:
        if data.get(key) is not None:
            value = f"{data[key]:.1f}".rstrip("0").rstrip(".") + "%"
            text = re.sub(fr'(<strong data-stat="{key}">)[^<]*', lambda m: m[1] + value, text)
    def jug(match):
        tag = match[0]
        for name, value in (("aria-valuemax", goal), ("aria-valuenow", raised),
                            ("aria-label", f"{money(raised)} raised toward our {money(goal)} school-wide goal; {pct}%."
                                          + (f" {updated_text}." if updated_text else ""))):
            tag = re.sub(fr'{name}="[^"]*"', lambda _: f'{name}="{value}"', tag)
        return tag
    return re.sub(r'<[^>]+data-measuring-glass[^>]*>', jug, text)
