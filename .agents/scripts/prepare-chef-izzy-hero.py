"""Give the original transparent Chef Izzy breathing room without cropping his hat."""
from pathlib import Path
import struct
import zlib

import pymupdf


def png_pixels(data):
    """Decode straight RGBA pixels without a premultiplied-alpha round trip."""
    width, height, depth, kind, compression, filtering, interlace = struct.unpack(
        ">IIBBBBB", data[16:29]
    )
    assert (depth, kind, compression, filtering, interlace) == (8, 6, 0, 0, 0)
    compressed = bytearray()
    metadata = []
    offset = 8
    while offset < len(data):
        length = struct.unpack(">I", data[offset:offset + 4])[0]
        name = data[offset + 4:offset + 8]
        payload = data[offset + 8:offset + 8 + length]
        if name == b"IDAT":
            compressed.extend(payload)
        elif name in (b"cHRM", b"gAMA", b"iCCP", b"sRGB", b"pHYs"):
            metadata.append((name, payload))
        offset += length + 12
    filtered = zlib.decompress(compressed)
    stride = width * 4
    decoded = bytearray()
    previous = bytearray(stride)
    for y in range(height):
        start = y * (stride + 1)
        mode = filtered[start]
        assert mode in range(5)
        row = bytearray(filtered[start + 1:start + 1 + stride])
        for x in range(stride):
            left = row[x - 4] if x >= 4 else 0
            above = previous[x]
            diagonal = previous[x - 4] if x >= 4 else 0
            predicted = left + above - diagonal
            distances = [abs(predicted - value) for value in (left, above, diagonal)]
            paeth = (left, above, diagonal)[distances.index(min(distances))]
            adjustment = (0, left, above, (left + above) // 2, paeth)[mode]
            row[x] = (row[x] + adjustment) & 255
        decoded.extend(row)
        previous = row
    return width, height, bytes(decoded), metadata


def chunk(name, payload):
    return struct.pack(">I", len(payload)) + name + payload + struct.pack(
        ">I", zlib.crc32(name + payload) & 0xFFFFFFFF
    )


source = Path("assets/fundraiser-chef-izzy-transparent.png")
output = Path("assets/fundraiser-chef-izzy-hero.png")
padding = 12
mascot = pymupdf.Pixmap(str(source))
assert mascot.n == 4 and mascot.alpha, "Use the original transparent mascot."
width, height = mascot.width + padding * 2, mascot.height + padding * 2
samples = bytearray(width * height * 4)
source_width, source_height, original, metadata = png_pixels(source.read_bytes())
assert (source_width, source_height) == (mascot.width, mascot.height)
for row in range(mascot.height):
    start = ((row + padding) * width + padding) * 4
    source_start = row * mascot.width * 4
    samples[start:start + mascot.width * 4] = original[
        source_start:source_start + mascot.width * 4
    ]
rows = b"".join(
    b"\0" + samples[row * width * 4:(row + 1) * width * 4]
    for row in range(height)
)
output.write_bytes(
    b"\x89PNG\r\n\x1a\n"
    + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
    + b"".join(chunk(name, payload) for name, payload in metadata)
    + chunk(b"IDAT", zlib.compress(rows, 9))
    + chunk(b"IEND", b"")
)
check = pymupdf.Pixmap(str(output))
assert check.alpha and (check.width, check.height) == (width, height)
_, _, checked_pixels, _ = png_pixels(output.read_bytes())
assert checked_pixels[:padding * width * 4] == bytes(padding * width * 4)
for row in range(mascot.height):
    start = ((row + padding) * width + padding) * 4
    source_start = row * mascot.width * 4
    assert checked_pixels[start:start + mascot.width * 4] == original[
        source_start:source_start + mascot.width * 4
    ], "The mascot artwork must remain pixel-for-pixel unchanged."

# Render the actual newsletter as a visual reference for the complete original hat.
newsletter = pymupdf.open(
    "attached_assets/2026LaunchNewsletter_TheRecipeReport_1791493786053.pdf"
)
reference = Path(".agents/outputs/chef-izzy-newsletter-reference.png")
reference.parent.mkdir(parents=True, exist_ok=True)
newsletter[0].get_pixmap(matrix=pymupdf.Matrix(1.5, 1.5)).save(str(reference))
print(f"Saved {output}: {width}×{height}, genuine alpha and 12px transparent margins.")
