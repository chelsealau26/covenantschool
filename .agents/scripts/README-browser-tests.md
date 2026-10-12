# Fundraiser browser regression checks

Start the existing **Start application** workflow (`python server.py`), then run:

```sh
python .agents/scripts/test-fundraiser-browser.py
```

The Python Playwright dependency is locked in `uv.lock`. The runner uses system
Chromium (`chromium` on PATH); set `CHROMIUM_PATH` to use another Chromium binary.
It targets `https://$REPLIT_DEV_DOMAIN`; `BASE_URL` can point to another running
development server. It does not start a second server, publish, submit forms, or
change fundraising totals.

The live fundraiser must still be active. A retired page correctly fails these
checks rather than silently passing or bypassing retirement.

Coverage:

- 1440×1000 desktop, 390×844 phone, and 320×740 narrow phone.
- Initial and scrolled header logos; decoded, proportional, unclipped Chef Izzy;
  text-range overlap; decoded individual utensil backgrounds behind copy;
  document overflow and exactly two mobile season-date lines.
- Normal and the actual accessibility widget's high-contrast mode, including
  computed text/background contrast in every open event dialog.
- All six native modal dialogs, each closed via X, Escape, and real backdrop
  clicks (108 open/close cycles); title, viewport containment, internal overflow,
  sticky close control, background scroll lock, restored focus/scroll/overflow.
- Actual intersection-triggered jug fill, waiting just outside/inside the bottom
  threshold, final decorative fill, hidden raised total, and reduced-motion
  desktop/phone behavior.

Successful full-page screenshots, failure screenshots, and action traces are
written to `/tmp/fundraiser-browser`. These are diagnostic artifacts, not
pixel-perfect approved baselines. The geometry checks cannot detect edits to
the artwork's pixels; keep the existing asset checks as well. This suite uses
Chromium, not Safari or Firefox.

Pointer clicks deliberately use the already-centered event button coordinates:
Playwright locator clicks may auto-scroll between the saved position and the
click, invalidating the comparison with the position restored by the app.
