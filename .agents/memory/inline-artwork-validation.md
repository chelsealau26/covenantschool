---
name: Inline artwork validation
description: Avoiding corrupted embedded logos during large HTML edits.
---

Validate embedded artwork from the final HTML, not just the original image files or the number of image tags.

**Why:** Large logo substitutions produced concatenated base64 and excess padding while the surrounding markup still appeared valid. Repeating literal replacements did not reliably repair the artwork.

**How to apply:** Optimize display-sized artwork before embedding. Strictly decode each final data URI and confirm it opens as the declared image type. For public image URLs, verify the actual response and inspect the rendered logo instead of trusting the source file's existence.
