---
name: Inline artwork validation
description: Avoiding corrupted embedded logos during large HTML edits.
---

Validate embedded artwork from the final HTML, not just the original image files or the number of image tags.

**Why:** Large logo substitutions produced concatenated base64 and excess padding while the surrounding markup still appeared valid. Repeating literal replacements did not reliably repair the artwork.

**How to apply:** Optimize display-sized artwork before embedding. Strictly decode each final data URI and confirm it opens as the declared image type. For public image URLs, verify the actual response and inspect the rendered logo instead of trusting the source file's existence.

Map crop coordinates to the dimensions of the image actually viewed, not merely the saved preview's dimensions.

**Why:** The image viewer resized a preview, so coordinates estimated from the displayed image clipped the supplied utensil drawings despite producing valid transparent PNGs.

**How to apply:** Account for preview scaling, then inspect every isolated drawing on a contrasting contact sheet. Transparent corners and valid encoding do not prove that an entire handle or outline survived cropping.
