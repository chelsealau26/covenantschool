"""Remove only the connected white backdrop, preserving enclosed white artwork."""
from collections import deque
from pathlib import Path

import pymupdf

original = pymupdf.Pixmap(
    "attached_assets/Recipe_for_Success_overalllogo_1791493623697.jpg"
)
if original.colorspace.n != 3:
    original = pymupdf.Pixmap(pymupdf.csRGB, original)
image = pymupdf.Pixmap(original, 600, 650)
assert image.n == 3 and not image.alpha
width, height = image.width, image.height
rgb = image.samples
near_white = bytearray(width * height)
for index in range(width * height):
    r, g, b = rgb[index * 3:index * 3 + 3]
    near_white[index] = min(r, g, b) >= 244 and max(r, g, b) - min(r, g, b) <= 12
outside = bytearray(width * height)
queue = deque()


def visit(index):
    if near_white[index] and not outside[index]:
        outside[index] = 1
        queue.append(index)


for x in range(width):
    visit(x)
    visit((height - 1) * width + x)
for y in range(height):
    visit(y * width)
    visit(y * width + width - 1)
while queue:
    index = queue.popleft()
    x, y = index % width, index // width
    if x:
        visit(index - 1)
    if x < width - 1:
        visit(index + 1)
    if y:
        visit(index - width)
    if y < height - 1:
        visit(index + width)

# Keep breathing room around the lettering, without a large invisible image box.
foreground = [i for i in range(width * height) if not outside[i]]
left = max(0, min(i % width for i in foreground) - 5)
right = min(width, max(i % width for i in foreground) + 6)
top = max(0, min(i // width for i in foreground) - 5)
bottom = min(height, max(i // width for i in foreground) + 6)
new_width, new_height = right - left, bottom - top
rgba = bytearray(new_width * new_height * 4)
for y in range(top, bottom):
    for x in range(left, right):
        index = y * width + x
        if not outside[index]:
            target = ((y - top) * new_width + x - left) * 4
            rgba[target:target + 3] = rgb[index * 3:index * 3 + 3]
            rgba[target + 3] = 255
assert sum(outside) > width * height // 3
protected_white = sum(
    near_white[i] and not outside[i] for i in range(width * height)
)
assert protected_white > 1000, "Preserve the white hat and eagle details."
output = Path("assets/fundraiser-header-logo-transparent.png")
pymupdf.Pixmap(pymupdf.csRGB, new_width, new_height, bytes(rgba), True).save(str(output))
check = pymupdf.Pixmap(str(output))
assert check.alpha and check.n == 4
assert all(
    check.samples[index * 4 + 3] == 0
    for index in [0, new_width - 1, (new_height - 1) * new_width, new_width * new_height - 1]
)
print(
    f"Saved {output}: {new_width}×{new_height}; "
    f"{protected_white} enclosed white pixels preserved."
)
