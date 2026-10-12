---
name: Browser scroll restoration checks
description: Avoid testing automation scrolling instead of the dialog's saved scroll position.
---

Center an event trigger first, let scrolling settle, then use pointer coordinates
when comparing pre-open and post-close scroll positions.

**Why:** Playwright locator clicks can scroll again before dispatching the click,
so the app saves a different position from the test's earlier snapshot. This
produced false restoration failures on desktop and phone.

**How to apply:** Do not loosen restoration assertions to hide the mismatch.
Avoid automation-driven scroll between the snapshot and the opening click;
keep full-page screenshots after geometry measurements.
