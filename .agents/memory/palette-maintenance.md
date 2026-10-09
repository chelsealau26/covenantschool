---
name: Fundraiser palette maintenance
description: Preserving accessibility behavior during color-only cascade cleanup.
---

Treat high-contrast appearance as a separate baseline when consolidating fundraiser colors. A seemingly redundant normal button rule can also determine contrast-mode colors through specificity.

**Why:** Removing duplicate button colors changed the contrast-mode appearance even though the normal page stayed identical. Preserve the existing accessibility appearance rather than redesigning it during maintenance.

**How to apply:** Compare normal and contrast-mode computed styles, including pseudo-elements and open dialogs, against a pre-change snapshot. Let dialog scroll restoration settle before sampling; capture full-page screenshots after state comparisons so viewport changes do not contaminate layout measurements.
