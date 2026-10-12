---
name: Fundraiser palette maintenance
description: Preserving accessibility behavior during color-only cascade cleanup.
---

Treat high-contrast appearance as a separate baseline when consolidating fundraiser colors. A seemingly redundant normal button rule can also determine contrast-mode colors through specificity.

**Why:** Removing duplicate button colors changed the contrast-mode appearance even though the normal page stayed identical. Preserve the existing accessibility appearance rather than redesigning it during maintenance.

**How to apply:** Compare normal and contrast-mode computed styles, including pseudo-elements and open dialogs, against a pre-change snapshot. Let dialog scroll restoration settle before sampling; capture full-page screenshots after state comparisons so viewport changes do not contaminate layout measurements.

Shared accessibility selectors containing multiple `:not(#id)` terms have ID
specificity even when those IDs are exclusions. Do not assume a fundraiser
color override wins because it comes later.

**Why:** Real-browser checks found white-on-pale fundraiser buttons even though
the local contrast rule explicitly requested dark text.

**How to apply:** Check computed foreground/background contrast with the widget
enabled; keep necessary overrides scoped to fundraiser content, not the footer.

Edit the central definition rule when testing dependent palette tokens, rather
than setting a base token on a descendant.

**Why:** Inherited custom properties containing `var()` have already resolved at
their defining ancestor; a descendant override can misleadingly appear not to
affect a correctly wired derived tint.

**How to apply:** Mutate and restore the definition using CSSOM and assert the
resulting computed component colors. Relative RGB can render with one-channel
rounding differences from legacy RGBA even with equivalent computed values.
