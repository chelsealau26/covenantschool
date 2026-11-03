"""Preview-only brand guide for the refreshed Covenant Christian School design.
Served at /brand-guide?preview=KEY (404 for everyone else)."""

SW = [  # name, hex, use
    ("Navy", "#153553", "Primary brand color. Headings on light backgrounds, outline buttons, footer."),
    ("Navy 2", "#224361", "Hover state for navy buttons; top of the footer gradient."),
    ("Deep navy", "#0d2136", "Dark bands, photo overlays (72%), bottom of the footer gradient."),
    ("Ink", "#131c24", "Large Anton headings on light backgrounds."),
    ("Silver", "#c4c5c7", "Accents: rules, icon outlines, frames. Filled shapes and buttons use the Metallic finish below (navy text only)."),
    ("Light silver", "#dddedf", "Small text on dark or photo backgrounds (taglines, subtitles)."),
    ("Deep silver", "#636669", "Small text and accents on light backgrounds: eyebrow labels, arrows, link hover text. Not a button color."),
    ("Star gold", "#e8b33a", "Review stars only. The one place gold appears."),
    ("Mist", "#eeeeef", "Soft section background (e.g. CCS Resources)."),
    ("Paper", "#f7f7f7", "Alternate light section background."),
    ("White", "#ffffff", "Default section background; text on navy."),
]

def swatch(name, hexv, use):
    dark = hexv in ("#153553", "#224361", "#0d2136", "#131c24", "#636669")
    return (f'<li class="bgd-sw"><span class="bgd-chip" style="background:{hexv}"><span style="color:{"#fff" if dark else "#153553"}">{hexv}</span></span>'
            f'<strong>{name}</strong><span>{use}</span></li>')

def rule_list(items):
    return "<ul class=\"bgd-rules\">" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"

def section(id_, title, intro, body, tone="gv-white"):
    return f'''
  <section class="gv gv-section {tone}" id="{id_}" aria-labelledby="bgd-{id_}">
    <div class="gv-wrap">
      <div class="bgd-head"><h2 id="bgd-{id_}">{title}</h2><p>{intro}</p></div>
      {body}
    </div>
  </section>'''

STYLE = """<style>
.bgd-head { max-width: 760px; margin-bottom: 30px; }
.bgd-head p { margin-top: 10px !important; color: var(--muted); font-size: 17px; }
.bgd-sws { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 22px; }
.bgd-sw { display: flex; flex-direction: column; gap: 6px; font-size: 15px; color: var(--muted); }
.bgd-sw strong { color: var(--navy); font-size: 16px; }
.bgd-chip { display: flex; align-items: flex-end; height: 96px; padding: 10px 12px; border-radius: 4px; border: 1px solid #e3d6c6; font: 700 13px/1 "Open Sans", Arial, sans-serif; letter-spacing: .04em; }
.bgd-rules { margin: 0; padding-left: 20px; display: grid; gap: 10px; max-width: 860px; font-size: 17px; line-height: 1.6; color: var(--ink); }
.bgd-rules li::marker { color: var(--tan-deep); }
.bgd-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 32px; align-items: start; }
.bgd-card { background: #fff; border: 1px solid #e6dacb; border-radius: 4px; padding: 26px; }
.bgd-card.is-dark { background: var(--navy); border-color: var(--navy); color: #fff; }
.bgd-card h3 { margin-bottom: 12px !important; }
.bgd-card.is-dark h3 { color: #fff; }
.bgd-label { display: block; margin-bottom: 8px; font: 700 12px/1.2 "Open Sans", Arial, sans-serif; letter-spacing: .12em; text-transform: uppercase; color: var(--tan-deep); }
.bgd-card.is-dark .bgd-label { color: var(--tan); }
.bgd-type > * + * { margin-top: 18px !important; }
.bgd-demo-anton { font: 400 52px/1.05 Anton, "Open Sans", Arial, sans-serif; color: var(--ink); }
.bgd-demo-tahoma { font: 700 21px/1.35 Tahoma, "Open Sans", Arial, sans-serif; color: var(--navy); }
.bgd-demo-body { font: 400 17px/1.65 "Open Sans", Arial, sans-serif; color: var(--muted); }
.bgd-demo-tag { font: 400 16px/1.4 "Open Sans", Arial, sans-serif; letter-spacing: .14em; text-transform: uppercase; color: #dddedf; }
.bgd-row { display: flex; flex-wrap: wrap; gap: 14px; align-items: center; margin-top: 14px; }
.bgd-corner { width: 84px; height: 64px; background: var(--tan-soft); border: 2px solid var(--navy); display: grid; place-items: center; font: 700 12px "Open Sans", Arial, sans-serif; color: var(--navy); }
.bgd-table { width: 100%; border-collapse: collapse; font-size: 16px; }
.bgd-table th, .bgd-table td { text-align: left; padding: 12px 10px; border-bottom: 1px solid #e6dacb; vertical-align: top; }
.bgd-table th { font: 700 13px/1.2 "Open Sans", Arial, sans-serif; letter-spacing: .08em; text-transform: uppercase; color: var(--navy); }
.bgd-note { margin-top: 18px !important; font-size: 15px; color: var(--muted); }
.bgd-grad { height: 130px; align-items: flex-end; font: 400 22px/1 Anton, "Open Sans", Arial, sans-serif; letter-spacing: .02em; border: 0; }
.gv .bgd-grad { color: #fff !important; } .gv .bgd-grad.is-light { color: #153553 !important; }
.bgd-grads { grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); margin-bottom: 30px; }
.bgd-sw code { font-size: 12px; color: var(--muted); word-break: break-word; }
.bgd-toc { display: flex; flex-wrap: wrap; gap: 10px 22px; margin-top: 26px; }
.bgd-toc a { color: #fff !important; text-decoration: none !important; font-weight: 600; transition: color .2s; }
.bgd-toc a:hover, .bgd-toc a:focus-visible { color: #dddedf !important; }
@media (max-width: 860px) { .bgd-grid { grid-template-columns: 1fr; } .bgd-demo-anton { font-size: 40px; } }
</style>"""

GRADS = [  # name, css, text color, use
    ("Navy depth", "linear-gradient(165deg, #224361 0%, #153553 42%, #0d2136 100%)", "#fff",
     "The main dark gradient: footer, dark sections, the Mission panel, this guide's header. Light from the top left, deepening to the bottom right."),
    ("Navy tile", "linear-gradient(180deg, #1a4168 0%, #153553 55%, #102b45 100%)", "#fff",
     "Vertical version for tiles and cards that sit on top of photos or white (the quick links under the hero)."),
    ("Photo shade", "linear-gradient(90deg, rgba(13,33,54,.9) 0%, rgba(13,33,54,.78) 55%, rgba(13,33,54,.45) 100%), url(/assets/covenant-92-9517625.jpg) center 8% / cover", "#fff",
     "Over photos when the text sits on the left: dark behind the words, letting faces show on the right."),
    ("Metallic", "linear-gradient(135deg, #f6f6f7 0%, #cfd0d2 30%, #f2f2f3 48%, #b9bbbe 72%, #e3e4e5 100%)", "#153553",
     "Hover fill that rises from the bottom of navy tiles. Text on it turns navy."),
    ("Mist fade", "linear-gradient(180deg, #ffffff 0%, #f7f7f7 100%)", "#153553",
     "Soft light sections (CCS Resources). Paper fade (white → paper) is the lighter alternative."),
]

def grad(name, css, fg, use):
    return (f'<li class="bgd-sw"><span class="bgd-chip bgd-grad{' is-light' if fg != '#fff' else ''}" style="background:{css}">{name}</span>'
            f'<strong>{name}</strong><span>{use}</span><code>{css.split(", url(")[0]}</code></li>')

def brand_guide(ICON):
    sws = '<ul class="bgd-sws">' + "".join(swatch(*s) for s in SW) + "</ul>"
    colors = sws + rule_list([
        "Yellow is reserved for the Fall Fundraiser and never appears anywhere else.",
        "Text must be at least 4.5:1 against its background (3:1 for text 24px+ or 19px+ bold). Navy on silver passes (7.3:1); white on silver does not (1.7:1), so silver buttons always use navy text.",
        "On navy backgrounds, link hover is light silver (#dddedf), never blue.",
        "Small silver text on light backgrounds uses Deep silver (#636669, 5.8:1 on white). Regular Silver is for lines, outlines, icons and large shapes.",
    ])
    grads = '<ul class="bgd-sws bgd-grads">' + "".join(grad(*g) for g in GRADS) + "</ul>" + rule_list([
        "Lean on gradients for every dark or tinted surface; flat navy should be the exception. They give depth and keep the site feeling current.",
        "Gradients stay within one family: navy to deeper navy, white to mist, and the Metallic silver sheen. Never mix navy and silver in one gradient, and never use rainbow or neon blends. Silver is never flat grey on a fill: buttons, tiles and filled shapes always use the Metallic finish.",
        "Dark gradients run at 165° (light top-left to dark bottom-right); light and tile gradients run straight down (180°).",
        "Every gradient also sets a solid fallback color (e.g. Navy) so text stays readable while it paints and accessibility checkers read the right background.",
        "Text on a gradient must pass contrast against its lightest point.",
    ])
    type_ = f'''<div class="bgd-grid">
      <div class="bgd-card bgd-type">
        <span class="bgd-label">Section headings (h1, h2) · Anton</span><p class="bgd-demo-anton">Experience the Covenant Difference</p>
        <span class="bgd-label">Sub-headings (h3, card and column titles) · Tahoma bold</span><p class="bgd-demo-tahoma">Join the Family Teacher Partnership</p>
        <span class="bgd-label">Body · Open Sans 17–19px</span><p class="bgd-demo-body">Get involved and make a difference in our school community. Together, we can support our students and enrich their educational experience.</p>
      </div>
      <div class="bgd-card is-dark bgd-type">
        <span class="bgd-label">Tagline / subtitle on dark · Open Sans, regular, spaced capitals</span><p class="bgd-demo-tag">Supporting the family with Christian education</p>
      </div>
    </div>''' + rule_list([
        "One h1 per page (the hero). Every section gets an h2; cards and columns inside it use h3. Never skip a level (h2 → h4) and never use a heading just for size.",
        "Anton headings: hero 44–92px, sections 40–46px, bands 46–48px. Title Case in sections; ALL CAPS only in heroes and photo bands.",
        "Taglines and subtitles stay regular weight and under 20px so they read as text, not as headings.",
        "Keep the client's wording. Tidy spacing and punctuation only; no rewrites without approval.",
    ])
    buttons = f'''<div class="bgd-grid">
      <div class="bgd-card">
        <span class="bgd-label">On light backgrounds</span>
        <div class="bgd-row"><a class="gv-btn gv-btn-gold" href="/schedule-tour">Schedule a Tour</a><a class="gv-btn gv-btn-line" href="#buttons">Learn More</a></div>
      </div>
      <div class="bgd-card is-dark">
        <span class="bgd-label">On navy or photo backgrounds</span>
        <div class="bgd-row"><a class="gv-btn gv-btn-gold" href="/schedule-tour">Schedule a Tour</a><a class="gv-btn gv-btn-ghost" href="#buttons">More Details</a></div>
      </div>
    </div>
    <table class="bgd-table" style="margin-top:28px">
      <thead><tr><th scope="col">Style</th><th scope="col">Means</th><th scope="col">Used for</th></tr></thead>
      <tbody>
        <tr><td>Metallic silver, navy text</td><td>The one action we most want a new family to take on that page</td><td>Schedule a Tour; Apply Now on the New Student Application page; Pledge Now / Donate on giving pages</td></tr>
        <tr><td>Navy outline (light bg)</td><td>Go somewhere / learn more</td><td>Learn More, Apply Today, Directions, Download the App, Explore Scholarships</td></tr>
        <tr><td>White outline (dark bg)</td><td>Same as navy outline, on navy or photos</td><td>Visit the Family Portal, More Details</td></tr>
        <tr><td>Text link + arrow</td><td>List of destinations</td><td>CCS Resources; arrows are drawn by CSS so they are not read aloud</td></tr>
      </tbody>
    </table>''' + rule_list([
        "At most one silver button per section. If two actions compete, the tour wins the silver.",
        "Labels are short, uppercase verbs: SCHEDULE A TOUR, LEARN MORE, APPLY TODAY.",
        "No underlines, on headings or on links. Links show they are links with color, an arrow, or a hover change (light silver on navy, deep silver on light).",
        "Buttons are at least 52px tall; side-by-side buttons in a row share the same width and line up at the bottom.",
        "Links that leave the site open in a new tab and say so to screen readers. Square donations open in an on-page window; PDFs open in an on-page window on computers only.",
    ])
    shape = f'''<div class="bgd-row" style="margin-bottom:22px">
        <span class="bgd-corner" style="border-radius:4px">4px</span>
        <span class="bgd-corner" style="border-radius:6px">6px</span>
        <span class="bgd-corner" style="border-radius:999px;width:120px">pill</span>
        <span class="bgd-corner" style="border-radius:50%;width:64px">circle</span>
      </div>''' + rule_list([
        "4px corners on surfaces: cards, photos, panels, inputs. Echoes the straight lines of the logo.",
        "6px corners on buttons and other controls.",
        "Pills only for small badges (e.g. NEW IN 2027). Circles only for round icon buttons (social, back to top).",
        "Icons: simple line icons (1.8 stroke) in a 52px square with a 2px silver outline. On hover the square fills navy and the icon turns silver.",
        "Thin rules: 1px #d6d7d9 between items; 2px silver or navy for the top of a list; 3px silver along the top of the footer.",
    ])
    brand = rule_list([
        "The eagle from the logo is the signature detail. Use it large and quiet: white at about 22% on mist, or 7–8% on navy, bleeding off the edge of the section. Never small, never as clip art.",
        "Photos must show faces. Position crops so faces are fully visible on desktop and phones.",
        "Heroes: the homepage and About Us are centered (brand statements over a full-width photo). Every other page is left-aligned: big Anton headline on navy at the left, the photo shown clearly on the right and fading into the navy, with a gentle parallax. On phones the photo sits behind the text under a navy overlay.",
        "Photos with text on them get an even navy overlay (rgba(13,33,54,.72)) when the text is centered, or a left-to-right navy gradient when the text sits on the left. The section also gets a solid dark background color so text stays readable while the photo loads.",
        "The silver frame: a featured photo can carry a 2px silver outline offset 22px down and right, drawn in as it scrolls into view.",
        "Sections alternate White, Paper and Mist, broken up by full-width navy photo bands. Two adjacent sections never share the same background unless they are one group.",
        "Footer: navy gradient (Navy 2 → Navy → Deep navy) with a 3px silver line on top; social icons are round outlines that fill metallic silver on hover.",
    ])
    motion = rule_list([
        "Motion should feel purposeful, never cute: fade-and-rise as sections enter, numbers that count up, the hero photos crossfading every 6 seconds, photo bands drifting at about a quarter of the scroll speed, the silver frame drawing itself in.",
        "Quick-link tiles: a metallic silver wash rises from the bottom and the eagle glides in on hover.",
        "Nothing moves for visitors who turn on “reduce motion”; everything simply appears.",
        "Avoid collages, floating badges, bouncing and other decoration that competes with the content.",
    ])
    a11y = rule_list([
        "Every image has alt text. Photos of people get a short description (under 100 characters); decorative images and the eagle watermark use empty alt.",
        "Headings in order, one h1, no empty headings, no text styled to look like a heading that isn't one.",
        "Contrast 4.5:1 for body text, checked against the darkest and lightest parts of any photo behind it.",
        "Keyboard focus is always visible; round controls get round focus rings.",
        "Check every page with WAVE and fix all errors and contrast errors before publishing.",
    ])
    hero = f'''
  <section class="gv gv-section gv-dark" aria-labelledby="bgd-title" style="background: linear-gradient(165deg, #224361 0%, #153553 42%, #0d2136 100%) #153553">
    <div class="gv-wrap">
      <p class="gv-eyebrow" style="color:#dddedf">Internal · preview only</p>
      <h1 id="bgd-title" style="color:#fff">Covenant Brand Guide</h1>
      <p class="gv-lead" style="color:#fff;max-width:720px;margin-top:14px">The rules behind the refreshed homepage, so every page of the website can follow the same design.</p>
      <nav class="bgd-toc" aria-label="Brand guide sections"><a href="#colors">Color</a><a href="#gradients">Gradients</a><a href="#type">Type</a><a href="#buttons">Buttons</a><a href="#shape">Corners &amp; icons</a><a href="#brand">Eagle, photos &amp; layout</a><a href="#motion">Motion</a><a href="#a11y">Accessibility</a></nav>
    </div>
  </section>'''
    return STYLE + hero + "".join([
        section("colors", "Color", "Navy and silver, the school colors, on crisp cool neutrals. Silver always reads metallic, never flat grey.", colors),
        section("gradients", "Gradients", "Depth instead of flat color: the modern finish across the site.", grads, "gv-paper"),
        section("type", "Type", "Three typefaces, each with one job.", type_),
        section("buttons", "Buttons", "A button's style tells visitors what it does. Metallic silver always means the same thing.", buttons, "gv-paper"),
        section("shape", "Corners &amp; icons", "Mostly straight, like the logo, with just enough softness.", shape, "gv-soft"),
        section("brand", "Eagle, photos &amp; layout", "What makes a page feel like Covenant.", brand),
        section("motion", "Motion", "Small, deliberate movement that helps people notice what matters.", motion, "gv-paper"),
        section("a11y", "Accessibility", "Every page should pass WAVE with no errors.", a11y),
    ])
