---
name: Static fundraiser delivery
description: First-paint and static export pitfalls in the imported school website.
---

Render final fundraiser branding and critical layout styles before the first paint, not through end-of-page replacements.

**Why:** Late overrides and replacing the original school header logo after parsing made the old design flash while the large imported document loaded. A settled screenshot alone did not catch this.

**How to apply:** Preserve CSS cascade order when reorganizing styles, render branding in initial HTML, and test the response structure as well as screenshots. Keep the shared footer intact.

Static hosting must include local assets and PDFs, not just HTML.

**Why:** The Python preview serves root-level asset directories separately, while the previous static export served only pages. Images could work in preview but be missing from the deployed bundle.

**How to apply:** Validate the actual built output against the page's image/download URLs. Do not treat successful preview requests as proof that a static deployment contains the files.
