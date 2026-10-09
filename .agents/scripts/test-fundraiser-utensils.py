"""Verify the supplied doodles have real alpha and only approved ink colors."""
from pathlib import Path
import struct
import zlib

root = Path("assets/fundraiser-utensils")
colors = {"navy": (29, 58, 95), "white": (255, 255, 255)}
for name in ("whisk", "spatula", "mixing-bowl", "cloche", "frying-pan"):
    for variant, color in colors.items():
        path = root / f"{name}-{variant}.png"
        data = path.read_bytes()
        assert data[:8] == b"\x89PNG\r\n\x1a\n", path
        position = 8
        compressed = bytearray()
        while position < len(data):
            length = struct.unpack(">I", data[position:position+4])[0]
            kind = data[position+4:position+8]
            content = data[position+8:position+8+length]
            if kind == b"IHDR":
                width, height, depth, mode, _, _, _ = struct.unpack(">IIBBBBB", content)
                assert (depth, mode) == (8, 6), f"{path}: requires RGBA"
            if kind == b"IDAT":
                compressed.extend(content)
            position += length + 12
        raw = zlib.decompress(compressed)
        stride = width * 4 + 1
        assert len(raw) == stride * height
        visible = 0
        for y in range(height):
            row = raw[y * stride:(y + 1) * stride]
            assert row[0] == 0
            for x in range(width):
                i = 1 + x * 4
                red, green, blue, alpha = row[i:i+4]
                if alpha:
                    visible += 1
                    assert (red, green, blue) == color, f"{path}: unexpected ink color"
                    assert 8 <= x < width - 8 and 8 <= y < height - 8, f"{path}: missing transparent padding"
        assert 0 < visible < width * height * 0.5, f"{path}: background must be transparent"
print("PASS: ten separate doodles, exact navy/white ink, real transparent backgrounds/interiors and uncropped transparent margins.")
