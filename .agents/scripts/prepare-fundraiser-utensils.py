"""Separate supplied doodles and convert brown linework to transparent brand colors."""
from pathlib import Path
from zipfile import ZipFile
import struct
import zlib
import fitz

ARCHIVE = Path("attached_assets/cooking-doodle-icons-kitchen-utensils-line-food-restaurant-log_1791508102309.zip")
MEMBER = "Cooking_doodle_icons_kitchen_utensils_line_food_restaurant_logo.jpg"
OUTPUT = Path("assets/fundraiser-utensils")
# Coordinates on the displayed 1024-pixel-wide reference, selecting one illustration.
CROPS = {
    "whisk": (579, 251, 674, 421),
    "spatula": (638, 90, 711, 235),
    "mixing-bowl": (115, 275, 292, 425),
    "cloche": (342, 285, 530, 410),
    "frying-pan": (760, 259, 944, 422),
}
COLORS = {"navy": (29, 58, 95), "white": (255, 255, 255)}

def save_rgba(path, width, height, pixels):
    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))
    rows = b"".join(b"\0" + pixels[y * width * 4:(y + 1) * width * 4] for y in range(height))
    path.write_bytes(b"\x89PNG\r\n\x1a\n" +
                    chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)) +
                    chunk(b"IDAT", zlib.compress(rows, 9)) + chunk(b"IEND", b""))


def main():
    with ZipFile(ARCHIVE) as archive:
        source = fitz.open(stream=archive.read(MEMBER), filetype="jpeg")
    page = source[0]
    scale = page.rect.width / 1024
    OUTPUT.mkdir(parents=True, exist_ok=True)
    sheet = fitz.open()
    sheet_page = sheet.new_page(width=1200, height=330)
    sheet_page.draw_rect(sheet_page.rect, color=None, fill=(223/255, 244/255, 248/255))
    for index, (name, bounds) in enumerate(CROPS.items()):
        clip = fitz.Rect(*(value * scale for value in bounds))
        ratio = 560 / max(clip.width, clip.height)
        crop = page.get_pixmap(matrix=fitz.Matrix(ratio, ratio), clip=clip, colorspace=fitz.csRGB, alpha=False)
        # Remove white inside and outside the line drawings, retaining antialiasing.
        rgb = crop.samples
        alpha = [round(max(0, min(255, (240 - min(rgb[i:i+3])) * 255 / 218)))
                 for i in range(0, len(rgb), 3)]
        ink_points = [(i % crop.width, i // crop.width) for i, value in enumerate(alpha) if value]
        if not ink_points:
            raise ValueError(f"No artwork found for {name}")
        left = min(x for x, y in ink_points)
        top = min(y for x, y in ink_points)
        right = max(x for x, y in ink_points) + 1
        bottom = max(y for x, y in ink_points) + 1
        width, height = right - left + 16, bottom - top + 16
        for color_name, color in COLORS.items():
            result = bytearray(width * height * 4)
            for y in range(top, bottom):
                for x in range(left, right):
                    opacity = alpha[y * crop.width + x]
                    if opacity:
                        i = ((y - top + 8) * width + x - left + 8) * 4
                        result[i:i+4] = bytes(color + (opacity,))
            path = OUTPUT / f"{name}-{color_name}.png"
            save_rgba(path, width, height, result)
            assert result[3] == 0
            assert all(tuple(result[i:i+3]) == color for i in range(0, len(result), 4) if result[i+3])
            if color_name == "navy":
                size = min(190 / width, 255 / height)
                x = index * 240 + (240 - width * size) / 2
                sheet_page.insert_image(fitz.Rect(x, 20, x + width * size, 20 + height * size), filename=str(path))
                sheet_page.insert_text((index * 240 + 20, 305), name, fontsize=13, color=tuple(value/255 for value in COLORS["navy"]))
        print(f"{name}: isolated, transparent, navy and white; {width}x{height}")
    sheet_page.get_pixmap().save("/tmp/fundraiser-utensil-contact-sheet.png")


if __name__ == "__main__":
    main()
