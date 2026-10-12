---
name: Browser scroll restoration checks
description: Browser tests must preserve real scroll and navigation signals.
---

Center an event trigger first, let scrolling settle, then use pointer coordinates
when comparing pre-open and post-close scroll positions.

**Why:** Playwright locator clicks can scroll again before dispatching the click,
so the app saves a different position from the test's earlier snapshot. This
produced false restoration failures on desktop and phone.

**How to apply:** Do not loosen restoration assertions to hide the mismatch.
Avoid automation-driven scroll between the snapshot and the opening click;
keep full-page screenshots after geometry measurements.

Use a Date-only test clock when asserting navigation-dependent behavior.

**Why:** In this environment, Playwright clock mocking exposed no native
Performance navigation entries, causing actual refreshes to be classified as
ordinary visits. The popup itself worked with real browser navigation timing.

**How to apply:** Preserve the real Performance API in reload/back-navigation
tests; freeze Date separately to keep fundraiser tests before the deadline.
