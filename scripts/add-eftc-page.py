"""One-time builder for the Education Freedom Tax Credit page and its links.

Creates pages/federal-tax-credit.html from the Scholarship Opportunities page
(same header, hero style and footer), then adds links to it in the nav, footer,
Ways to Give, Scholarship Opportunities and the sitemap. Safe to re-run.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "pages"
SLUG = "federal-tax-credit"
URL = f"https://covenantschool.com/{SLUG}"
CSS = '<link rel="stylesheet" href="/assets/eftc.css"><script src="/assets/eftc.js" defer></script>'

TITLE = "Education Freedom Tax Credit | Covenant Christian School"
DESC = ("Redirect up to $1,700 of your federal taxes ($3,400 for couples filing jointly) "
        "to scholarships for Covenant Christian School students through the new Education "
        "Freedom Tax Credit, starting January 2027.")

WIDGET = """<div id="theodore-giving-embed"></div>
<script src="https://aosf.theolearning.com/embed.js"
        data-base-url="https://aosf.theolearning.com"
        data-public-key="JGBH9Zv13Fsr6hKWbMGDrydX"
        data-primary-color="#f5c842"
        data-secondary-color="#1a2744"></script>"""

MAIN_SECTION = f"""
  <section class="eftc eftc-main" aria-labelledby="eftc-how">
    <div class="eftc-grid">
      <div class="eftc-intro">
        <span class="eftc-badge">New in 2027</span>
        <h2 id="eftc-how">Your Taxes Can Help a Covenant Student</h2>
        <p class="eftc-lead">The federal Education Freedom Tax Credit gives you a dollar-for-dollar credit on your federal income taxes when you give to a scholarship-granting organization. Covenant Christian School has partnered with the Alabama Opportunity Scholarship Fund (AOSF) so your gift supports scholarships for Covenant families.</p>

        <div class="eftc-amounts">
          <div class="eftc-amount"><span class="eftc-amount-label">Individuals</span><strong>$1,700</strong><span>credit per taxpayer</span></div>
          <div class="eftc-amount"><span class="eftc-amount-label">Married filing jointly</span><strong>$3,400</strong><span>credit per couple</span></div>
        </div>

        <ul class="eftc-checks">
          <li>Dollar-for-dollar credit on your federal income taxes</li>
          <li>Open to taxpayers in every state</li>
          <li>No payment today, just your pledge</li>
        </ul>
      </div>

      <div class="eftc-pledge" id="pledge" aria-labelledby="eftc-pledge-title">
        <div class="eftc-pledge-head">
          <h3 id="eftc-pledge-title">Make Your Pledge</h3>
          <p>No payment is due today.</p>
        </div>
        {WIDGET}
        <noscript><p class="eftc-fallback">This form needs JavaScript. Please <a href="/contact">contact our office</a> to pledge.</p></noscript>
      </div>
    </div>
  </section>

  <section class="eftc eftc-how" aria-labelledby="eftc-steps-title">
    <div class="eftc-wrap">
      <h2 id="eftc-steps-title">How It Works</h2>
      <ol class="eftc-steps">
        <li><h4>Pledge today</h4><p>Use the form to let us know you plan to give. Pledging now helps us plan scholarships for next year.</p></li>
        <li><h4>Give through AOSF in 2027</h4><p>When the program opens in January 2027, your gift goes to AOSF with Covenant Christian School selected as your school.</p></li>
        <li><h4>Claim your credit</h4><p>Claim the credit on your 2027 federal tax return. Your tax professional can confirm how it applies to you.</p></li>
      </ol>
    </div>
  </section>

  <section class="eftc eftc-know" aria-labelledby="eftc-know-title">
    <div class="eftc-wrap">
      <h2 id="eftc-know-title">Good to Know</h2>
      <div class="eftc-tiles">
        <div class="eftc-tile"><h4>Any state can give</h4><p>Grandparents, alumni and friends anywhere in the country can take part, not just Alabama residents.</p></div>
        <div class="eftc-tile"><h4>First come, first served</h4><p>Credits are limited by a national cap, so pledging early helps make sure your gift counts.</p></div>
        <div class="eftc-tile"><h4>For Covenant families</h4><p>Scholarships support K–12 students in households earning up to 300% of their area's median income. See <a href="/scholarship-opportunities">Scholarship Opportunities</a>.</p></div>
      </div>
      <p class="eftc-note">Covenant Christian School does not provide tax advice. Please consult a tax professional about your situation.</p>
    </div>
  </section>

  <section class="eftc eftc-help">
    <h2>Questions?</h2>
    <p>We're happy to walk you through it, or you can learn more from the <a href="https://www.alabamascholarshipfund.org/" target="_blank" rel="noopener">Alabama Opportunity Scholarship Fund</a>.</p>
    <div class="eftc-help-actions">
      <a class="eftc-btn eftc-btn-gold" href="#pledge">Make Your Pledge</a>
      <a class="eftc-btn eftc-btn-outline" href="/contact">Contact Our Office</a>
    </div>
  </section>
"""

def callout(heading, body, label):
    return f"""<section class="eftc eftc-callout" aria-label="Education Freedom Tax Credit">
    <div class="eftc-callout-inner">
      <div class="eftc-callout-copy">
        <div class="eftc-eyebrow-row"><span class="eftc-eyebrow">Education Freedom Tax Credit</span><span class="eftc-badge">New in 2027</span></div>
        <h2>{heading}</h2>
        <p>{body}</p>
      </div>
      <a class="eftc-btn" href="/{SLUG}">{label}</a>
    </div>
  </section>
  """

def add_css(html):
    if CSS in html:
        return html
    html = html.replace('<link rel="stylesheet" href="/assets/eftc.css">', '')
    return html.replace("</head>", CSS + "</head>", 1)

def build_page():
    src = (PAGES / "scholarship-opportunities.html").read_text()
    src = re.sub(r'<section class="eftc eftc-callout"[\s\S]*?</section>\s*', '', src)
    # Head metadata
    src = src.replace("Scholarship Opportunities | Covenant Christian School", TITLE)
    src = src.replace("https://covenantschool.com/scholarship-opportunities", URL)
    old_desc = re.search(r'<meta name="description" content="([^"]*)"', src)[1]
    src = src.replace(old_desc, DESC)
    src = src.replace('"name": "Scholarship Opportunities",', '"name": "Education Freedom Tax Credit",')

    # Hero text + button
    src = src.replace(">SCHOLARSHIP OPPORTUNITIES</span></h5>", ">EDUCATION FREEDOM TAX CREDIT</span></h5>", 1)
    src = src.replace(">Every Child Deserves Access To A Quality Education</span></h1>",
                      ">Turn Your Federal Taxes Into Scholarships for Covenant Students</span></h1>", 1)
    src = src.replace(
        "We’re here to help make quality education accessible through exceptional scholarship opportunities. "
        "Explore two external programs designed to support and enrich your child’s educational journey.",
        "Starting January 2027, you can redirect up to $1,700 of your federal income taxes "
        "($3,400 for married couples filing jointly) to scholarships for Covenant Christian School families.", 1)
    src = src.replace('href="/scholarship-opportunities#options" \n             target="_self" class="theme-button', 'href="#pledge" \n             target="_self" class="eftc-hero-btn theme-button', 1)
    src = re.sub(r"\n\s*EXPLORE THE OPPORTUNITES</span>", "\n                    MAKE YOUR PLEDGE</span>", src, count=1)

    # Keep the hero (first container), replace the rest of the page body.
    start = src.index('<main id="main-content"')
    second = src.index('id="container-widget-1734627093594"')
    cut = src.rindex("<div", start, second)
    end = src.index("</main>")
    # Two wrapper divs (content-wrapper, content) are still open at `cut`.
    src = src[:cut] + MAIN_SECTION + "\n      </div>\n  </div>\n  " + src[end:]
    # Use a hero photo different from the Scholarship page.
    src = src.replace("covenant-126-9598381.jpg", "covenant-104-9578593.jpg")
    src = src.replace('<link rel="stylesheet" href="/assets/ccs-tables.css">', '')
    (PAGES / f"{SLUG}.html").write_text(add_css(src))

NAV_ANCHOR = '<a class="website-nav-link" rel="tab" href="/ways-to-give" >Ways to Give</a>\n                          </li>'
NAV_ITEM = NAV_ANCHOR + f"""

                          <li>


                            <a class="website-nav-link" rel="tab" href="/{SLUG}" >Federal Tax Credit</a>
                          </li>"""
FOOT_ANCHOR = '<a href="/ways-to-give">Ways to Give</a></span></p>'
FOOT_ITEM = FOOT_ANCHOR + f'<p style="line-height: 2;"><span style="color: rgba(255, 255, 255, 0.7); font-size: 15px;"><a href="/{SLUG}">Federal Tax Credit</a></span></p>'

def link_everywhere():
    for page in PAGES.glob("*.html"):
        html = page.read_text()
        if f'href="/{SLUG}" >Federal Tax Credit' not in html:
            html = html.replace(NAV_ANCHOR, NAV_ITEM)
        if f'<a href="/{SLUG}">Federal Tax Credit</a>' not in html:
            html = html.replace(FOOT_ANCHOR, FOOT_ITEM)
        page.write_text(html)

def add_callouts():
    targets = {
        "ways-to-give.html": callout(
            "Give With Your Federal Taxes",
            "Redirect up to $1,700 of your federal income taxes ($3,400 for couples filing jointly) "
            "to scholarships for Covenant students. Pledge now for January 2027.",
            "Pledge Now"),
        "scholarship-opportunities.html": callout(
            "A New Way Friends and Family Can Help",
            "Grandparents, relatives and supporters in any state can redirect part of their federal taxes "
            "to AOSF scholarships for Covenant families starting in 2027. Share this page with them!",
            "Learn More"),
    }
    for name, block in targets.items():
        page = PAGES / name
        html = page.read_text()
        html = re.sub(r'<section class="eftc eftc-callout"[\s\S]*?</section>\s*', '', html)
        start = html.index('<main id="main-content"')
        # Insert right after the page's hero container (the second top-level container).
        containers = [m.start() for m in re.finditer(r'id="container-widget-\d+"', html[start:])]
        second = start + containers[1]
        cut = html.rindex("<div", start, second)
        html = html[:cut] + block + html[cut:]
        page.write_text(add_css(html))

def add_sitemap():
    sm = PAGES / "sitemap.xml"
    xml = sm.read_text()
    if URL not in xml:
        line = "  <url><loc>https://covenantschool.com/scholarship-opportunities</loc>"
        i = xml.index(line); j = xml.index("\n", i) + 1
        xml = xml[:j] + f"  <url><loc>{URL}</loc><lastmod>2026-12-01</lastmod></url>\n" + xml[j:]
        sm.write_text(xml)

if __name__ == "__main__":
    if not (PAGES / f"{SLUG}.html").exists():
        build_page()
    link_everywhere()
    add_callouts()
    add_sitemap()
    print("EFTC page and links added.")
