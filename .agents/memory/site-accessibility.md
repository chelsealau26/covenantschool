---
name: Site accessibility and SEO conventions
description: Shared landmarks, contrast overrides and image descriptions across all pages.
---

Load `assets/site-a11y.css` last on every page and keep its rules scoped away from the fundraiser page's own tested styles (`body:not(.fundraiser-route)`, `:not(.fundraiser-register)`).

**Why:** Site-wide contrast/focus fixes must not change the approved fundraiser design; a computed-style comparison of every fundraiser element showed zero differences with this file loaded.

**How to apply:** Put shared accessibility CSS in that file, not inline `<style>` blocks; the fundraiser palette guard rejects new color literals in page style blocks.

The header parts are wrapped in `<header class="ccs-site-header">`, so `.page-layout > .mobile-menu` style selectors no longer match.

**Why:** Wrapping broke the right-side mobile menu slide until `assets/mobile-header.css` gained `.page-layout.open > .ccs-site-header > ...` selectors.

**How to apply:** When adding header rules with `>`, include the wrapper; verify the phone menu opens with the page, menu and sticky header all at left -240px.

Describe only what is visible in photos; never invent names, events or awards.

**Why:** The user explicitly said: “JUST DESCRIBE WHAT YOU SEE HERE, DONT MAKE SOMETHING UP.”

**How to apply:** Write alt text from the image itself. Use `alt=""` for decorative stock photos beside a heading that already conveys the same meaning.

The privacy policy covers only the website. Keep it accurate to what the site actually does (no own cookies; Cloudflare Web Analytics; platform page views; Google Maps, Calendly, job application form via Resend + Cloudflare Turnstile, Google Fonts, jsDelivr).

**Why:** The user said it is “JUST FOR THE WEBSITE USE.”

**How to apply:** Update the policy when adding forms, trackers or embeds.
