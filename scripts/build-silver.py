"""Builds assets/silver.css: a preview-only 'silver' look that swaps every warm tan/beige color in the
site's styles for a bright, cool silver. Rules apply only under html.ccs-silver (?look=silver on a preview link)."""
import re, colorsys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
A = ROOT / "assets"
SOURCES = [A / "site-a11y.css", A / "giving.css", A / "preview.css"]

def warm(r, g, b):
    return r >= g and (r - b > 12 or (r - b > 4 and min(r, g, b) > 225))

def to_silver(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    if 0.55 < l < 0.9: l = l + (0.9 - l) * 0.4      # brighter, metallic
    s = 0.03
    r2, g2, b2 = colorsys.hls_to_rgb(212 / 360, l, s)
    return round(r2 * 255), round(g2 * 255), round(b2 * 255)

HEX = re.compile(r"#([0-9a-fA-F]{6})\b")
RGBA = re.compile(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)(\s*,\s*[\d.]+)?\s*\)")

def swap(text):
    def hx(m):
        v = m.group(1); r, g, b = int(v[0:2], 16), int(v[2:4], 16), int(v[4:6], 16)
        return "#%02x%02x%02x" % to_silver(r, g, b) if warm(r, g, b) else m.group(0)
    def rg(m):
        r, g, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if not warm(r, g, b): return m.group(0)
        r2, g2, b2 = to_silver(r, g, b)
        return f"rgba({r2}, {g2}, {b2}{m.group(4) or ', 1'})"
    return RGBA.sub(rg, HEX.sub(hx, text))

def has_warm(text):
    return swap(text) != text

def prefix(sel):
    out = []
    parts, depth, cur = [], 0, ""
    for ch in sel:
        if ch in "([": depth += 1
        elif ch in ")]": depth -= 1
        if ch == "," and depth == 0: parts.append(cur); cur = ""
        else: cur += ch
    parts.append(cur)
    for s in parts:
        s = s.strip()
        if not s: continue
        if s.startswith(":root"): s = "html.ccs-silver" + s[5:]
        elif s.startswith("html"): s = "html.ccs-silver" + s[4:]
        else: s = "html.ccs-silver " + s
        out.append(s)
    return ", ".join(out)

METAL = "linear-gradient(135deg, #f6f6f7 0%, #cfd0d2 30%, #f2f2f3 48%, #b9bbbe 72%, #e3e4e5 100%)"
COLOR = re.compile(r"#[0-9a-fA-F]{6}\b|rgba?\([^)]*\)|var\(--tan\)|var\(--tan-soft\)|var\(--tan-deep\)")

def _light(tok):
    if tok == "var(--tan)": return 0.77
    if tok == "var(--tan-soft)": return 0.95
    if tok == "var(--tan-deep)": return 0.4
    if tok.startswith("#"):
        r, g, b = int(tok[1:3], 16), int(tok[3:5], 16), int(tok[5:7], 16)
    else:
        n = re.findall(r"[\d.]+", tok); r, g, b = map(float, n[:3])
        if len(n) > 3 and float(n[3]) < .6: return None
    return colorsys.rgb_to_hls(r / 255, g / 255, b / 255)[1]

def metal(decl):
    """A tan fill becomes brushed metal instead of flat grey."""
    if ":" not in decl: return None
    prop, val = decl.split(":", 1)
    if prop.strip() not in ("background", "background-color", "background-image"): return None
    if "url(" in val: return None
    raw = val.replace("!important", "")
    if not (has_warm(raw) or "var(--tan)" in raw): return None
    toks = COLOR.findall(raw)
    if not toks: return None
    ls = [_light(t) for t in toks]
    if any(l is None or l < 0.6 for l in ls) or min(ls) > 0.9: return None
    imp = " !important" if "!important" in val else ""
    return f"background: {METAL}{imp}"

def rules(css):
    css = re.sub(r"/\*[\s\S]*?\*/", "", css)
    i, n, out = 0, len(css), []
    while i < n:
        j = css.find("{", i)
        if j < 0: break
        head = css[i:j].strip()
        if head.startswith("@media") or head.startswith("@supports"):
            depth, k = 1, j + 1
            while k < n and depth:
                depth += {"{": 1, "}": -1}.get(css[k], 0); k += 1
            inner = rules(css[j + 1:k - 1])
            if inner: out.append(f"{head} {{\n{inner}\n}}")
            i = k; continue
        if head.startswith("@"):
            depth, k = 1, j + 1
            while k < n and depth:
                depth += {"{": 1, "}": -1}.get(css[k], 0); k += 1
            i = k; continue
        k = css.find("}", j)
        body = css[j + 1:k]
        decls = []
        for d in (x.strip() for x in body.split(";")):
            if not d: continue
            m = metal(d)
            if m: decls.append(m)
            elif has_warm(d): decls.append(swap(d))
        if decls and head:
            out.append(f"{prefix(head)} {{ " + "; ".join(decls) + "; }")
        i = k + 1
    return "\n".join(out)

def build(page_html_paths):
    parts = []
    for src in SOURCES: parts.append(rules(src.read_text()))
    seen = set()
    for p in page_html_paths:
        for block in re.findall(r"<style[^>]*>([\s\S]*?)</style>", p.read_text()):
            r = rules(block)
            if r and r not in seen: seen.add(r); parts.append(r)
    extra = """
/* review stars stay gold */
html.ccs-silver .hm-stars svg { fill: #e8b33a !important; }
/* metallic sheen on the primary buttons */
html.ccs-silver .gv-btn-gold, html.ccs-silver .gv .gv-btn-gold, html.ccs-silver .ccs-app-btn.is-main {
  background: linear-gradient(135deg, #f7f7f7 0%, #d4d5d6 42%, #f0f0f0 55%, #bdbfc1 100%) !important; border-color: #c8c9cb !important; color: #153553 !important;
  box-shadow: inset 0 1px 0 rgba(255,255,255,.8), 0 8px 20px rgba(13,33,54,.18); }
html.ccs-silver .gv-btn-gold:hover, html.ccs-silver .gv .gv-btn-gold:hover { background: linear-gradient(135deg, #ffffff 0%, #e0e1e2 42%, #f7f7f7 55%, #c9cacc 100%) !important; }
"""
    (A / "silver.css").write_text("/* generated by scripts/build-silver.py, do not edit */\n" + "\n".join(x for x in parts if x) + extra)

if __name__ == "__main__":
    pages = [ROOT / "pages" / "redesign" / "home.html", ROOT / "pages" / "athletics.html"]
    build(pages)
    print("Built silver.css", (A / "silver.css").stat().st_size, "bytes")
