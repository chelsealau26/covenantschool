---
name: Mascot image transparency
description: Background-removal verification for the newsletter's mixed photo and illustration artwork.
---

For the newsletter's Chef Izzy artwork, verify the resulting image visually and check for an alpha channel instead of trusting a successful background-removal response.

**Why:** The background-removal service returned a successful output while leaving the surrounding newsletter text and background intact.

**How to apply:** Check both the saved asset and the rendered page before delivering transparent artwork. Preserve the original mascot rather than generating a replacement.

Background removal can incorrectly erase enclosed white parts of a graphic logo, even when the background itself is transparent.

**Why:** The removal service left holes in the fundraiser logo's chef hat and eagle feathers.

**How to apply:** Inspect the artwork's white details as well as its alpha channel. For a plain white backdrop, removing only edge-connected white areas preserves enclosed white artwork.

Adding transparent margins through premultiplied RGBA samples can change translucent edge colors during re-encoding.

**Why:** A PyMuPDF pixmap round trip failed a pixel-preservation check when padding the mascot; preserving the original straight-alpha PNG pixels avoided that change.

**How to apply:** When only adding canvas space, keep the original image pixels unchanged. Verify transparent margins and compare the retained pixels, rather than assuming a save/load round trip is lossless.
