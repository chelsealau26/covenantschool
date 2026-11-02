"""Builds the redesigned giving pages from the site's shared header/footer.

Outputs
  pages/redesign/ways-to-give.html              (preview only until published)
  pages/redesign/scholarship-opportunities.html (preview only until published)
  pages/federal-tax-credit.html                 (hidden until the Dec 1 launch)

The worker serves the redesigns at /ways-to-give and /scholarship-opportunities
only when ?preview=<PREVIEW_KEY> is present. Tax-credit blocks have a
"coming soon" version and a "live" version; the worker keeps the right one.
Run:  python3 scripts/build-giving-pages.py
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "pages"
OUT = PAGES  # redesigns approved and published 2026-11-02
import hashlib
def _v(name):
    return hashlib.sha1((ROOT / "assets" / name).read_bytes()).hexdigest()[:8]
HEAD_EXTRA = f'<link rel="stylesheet" href="/assets/giving.css?v={_v("giving.css")}"><script src="/assets/giving.js?v={_v("giving.js")}" defer></script>'
IMG = "/assets/"

ICON = {
    "hand": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11 14h2a2 2 0 0 0 0-4h-3c-.6 0-1.1.2-1.4.6L3 16"/><path d="m7 20 1.6-1.4c.3-.4.8-.6 1.4-.6h4c1.1 0 2.1-.4 2.8-1.2l4.6-4.4a2 2 0 0 0-2.75-2.91l-4.2 3.9"/><path d="m2 15 6 6"/><path d="M19.5 8.5c.7-.7 1.5-1.6 1.5-2.7A2.73 2.73 0 0 0 16 4a2.78 2.78 0 0 0-5 1.8c0 1.2.8 2 1.5 2.8L16 12Z"/></svg>',
    "handshake": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m11 17 2 2a1 1 0 1 0 3-3"/><path d="m14 14 2.5 2.5a1 1 0 1 0 3-3l-3.88-3.88a3 3 0 0 0-4.24 0l-.88.88a1 1 0 1 1-3-3l2.81-2.81a5.79 5.79 0 0 1 7.06-.87l.47.28a2 2 0 0 0 1.42.25L21 4"/><path d="m21 3 1 11h-2"/><path d="M3 3 2 14l6.5 6.5a1 1 0 1 0 3-3"/><path d="M3 4h8"/></svg>',
    "heart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>',
    "pen": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>',
    "gift": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13"/><path d="M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7"/><path d="M7.5 8a2.5 2.5 0 0 1 0-5C10 3 12 8 12 8s2-5 4.5-5a2.5 2.5 0 0 1 0 5"/></svg>',
    "receipt": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 2v20l2-1 2 1 2-1 2 1 2-1 2 1 2-1 2 1V2l-2 1-2-1-2 1-2-1-2 1-2-1-2 1Z"/><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"/><path d="M12 17.5v-11"/></svg>',
    "map": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10Z"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>',
    "users": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/></svg>',
    "info": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>',
    "file": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5Z"/><path d="M14 2v6h6"/><path d="M16 13H8"/><path d="M16 17H8"/></svg>',
    "play": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m10 8 6 4-6 4Z"/></svg>',
    "external": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/></svg>',
    "lock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>',
    "calendar": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4"/><path d="M8 2v4"/><path d="M3 10h18"/></svg>',
    "school": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 10 12 5 2 10l10 5 10-5Z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>',
}
NEW_TAB = ' target="_blank" rel="noopener"'
SQUARE = "https://checkout.square.site/merchant/904MH0TAGK07M/checkout/XBAPCE4C2MVPSZMTCZOLJ4OE"


def credit_block(heading, body, photo, anchor="tax-credit"):
    """Tax credit feature: a 'coming soon' version and a 'live' version (worker keeps one)."""
    amounts = ('<div class="gv-credit-amounts"><div><strong>$1,700</strong><span>per individual</span></div>'
               '<div><strong>$3,400</strong><span>married filing jointly</span></div></div>')
    return f'''
  <section class="gv-section gv-white" id="{anchor}" aria-labelledby="gv-credit-title">
    <div class="gv-wrap">
      <div class="gv-credit" data-reveal="zoom" style="--credit-img: url('{IMG}{photo}')">
        <div class="gv-credit-copy">
<!--eftc:soon-->
          <span class="gv-badge gv-badge-tan gv-badge-soon">Coming December 1</span>
<!--/eftc:soon-->
<!--eftc:live-->
          <span class="gv-badge gv-badge-tan">New in 2027</span>
<!--/eftc:live-->
          <h2 id="gv-credit-title">{heading}</h2>
          <p>{body}</p>
          {amounts}
<!--eftc:soon-->
          <p class="gv-credit-soon">{ICON["calendar"]}<span>Pledges open December 1 for the Education Freedom Tax Credit. Check back soon!</span></p>
<!--/eftc:soon-->
<!--eftc:live-->
          <div class="gv-actions"><a class="gv-btn gv-btn-gold" href="/federal-tax-credit">Pledge Now</a><a class="gv-btn gv-btn-ghost" href="/federal-tax-credit#how">How It Works</a></div>
<!--/eftc:live-->
        </div>
        <div class="gv-credit-photo" aria-hidden="true"></div>
      </div>
    </div>
  </section>'''


def help_strip(text):
    return f'''
  <section class="gv-section gv-dark">
    <div class="gv-wrap gv-help" data-reveal>
      <div>
        <h2>We're Here to Help</h2>
        <p>{text}</p>
      </div>
      <div class="gv-actions"><a class="gv-btn gv-btn-gold" href="/contact">Contact Our Office</a></div>
    </div>
  </section>'''


# ---------------------------------------------------------------- Ways to Give
SPONSORS = [
    ("Anchor Point Therapy", "https://www.google.com/search?q=anchor+point+therapy+mobile+al", "anchor-point-therapy.jpg"),
    ("Belzona", "https://belzonaalabama.com/en/", "belzona.png"),
    ("C & J Machine", "https://www.google.com/search?q=c+%26+j+machine+%26+welding+inc", "cj-machine.jpg"),
    ("Christian Warehouse Store", "https://www.google.com/search?q=christian+warehouse+store+mobile+al", "christian-warehouse-store.png"),
    ("Covenant Church", "https://covenantmobile.com/", "covenant-church.png"),
    ("Eivar Ofelia Designs", "https://eivarofeliadesigns.com/", "eivar-ofelia-designs.png"),
    ("FACTS", "https://factsmgt.com/", "facts.png"),
    ("Joe Cowart, Inc.", "https://www.google.com/search?q=joe+cowart+inc+theodore", "joe-cowart.png"),
    ("L&E Yataco Services, LLC", "https://www.leyatacoservicesllc.com/", "le-yataco-services.jpg"),
    ("Little Monkey Toes", "https://littlemonkeytoes.com/", "little-monkey-toes.png"),
    ("Mobile Appliance", "https://mobileappliance.net/", "mobile-appliance.png"),
    ("Moe's Southwest Grill", "https://locations.moes.com/al/mobile/390-schillinger-rd-s", "moes-southwest-grill.png"),
    ("MW Counseling, LLC", "https://www.morganwalkercounseling.com/", "mw-counseling.jpg"),
    ("Pitts Properties LLC", "https://pittsconstruction.net/", "pitts-properties.png"),
    ("SAAD Healthcare", "https://saadhealthcare.com/", "saad-healthcare.png"),
    ("Vandals", "https://www.google.com/search?q=vandals+street+kitchen+mobile+al", "vandals.jpg"),
    ("Zoghby's", "https://zoghbyuniforms.com/", "zoghbys.png"),
]


def ways_to_give():
    logos = "\n".join(
        f'        <li data-reveal="zoom"><a href="{url}"{NEW_TAB} aria-label="{name} (opens in a new tab)">'
        f'<img src="/assets/fundraiser-sponsors/{img}" alt="{name}" loading="lazy"></a></li>'
        for name, url, img in SPONSORS)
    return f'''
  <section class="gv gv-hero gv-hero-split">
    <div class="gv-hero-photo" style="background-image: url('{IMG}covenant-104-9578593.jpg')" aria-hidden="true"></div>
    <div class="gv-wrap">
      <div class="gv-hero-copy">
        <span class="gv-eyebrow">Ways to Give</span>
        <h1>Join Us in Making a Difference</h1>
        <p class="gv-lead">We can't do it without amazing supporters like you! Whether you volunteer your time, partner with us through your business, or donate financially, together we can create a brighter future for our school family.</p>
        <div class="gv-actions">
          <a class="gv-btn gv-btn-gold" href="{SQUARE}"{NEW_TAB}>{ICON["heart"]}Make a Donation</a>
          <a class="gv-btn gv-btn-ghost" href="#ways">See All Ways to Give</a>
        </div>
      </div>
    </div>
  </section>

  <section class="gv gv-section gv-paper" id="ways" aria-labelledby="gv-ways-title">
    <div class="gv-wrap">
      <div class="gv-head" data-reveal>
        <span class="gv-eyebrow">Get involved</span>
        <h2 id="gv-ways-title">Four Ways to Give</h2>
        <p>Every gift of money, time or partnership makes a meaningful difference for our students. Choose the way that fits you best.</p>
      </div>
      <div class="gv-cards gv-cards-4">
        <article class="gv-card" data-reveal>
          <div class="gv-card-img"><span class="gv-card-clip"><img src="{IMG}covenant-59-9551512.jpg" alt="" loading="lazy"></span><span class="gv-card-icon">{ICON["heart"]}</span></div>
          <div class="gv-card-body">
            <h3>Donate</h3>
            <p>Your donations provide essential resources and enriching educational experiences for our students. Give securely online.</p>
            <div class="gv-actions"><a class="gv-btn gv-btn-gold" href="{SQUARE}"{NEW_TAB}>Make a Donation</a></div>
          </div>
        </article>
        <article class="gv-card" data-reveal>
          <div class="gv-card-img"><span class="gv-card-clip"><img src="{IMG}covenant-64-9598590.jpg" alt="" loading="lazy"></span><span class="gv-card-icon">{ICON["receipt"]}</span>
<!--eftc:soon-->
            <span class="gv-badge gv-badge-tan gv-badge-soon gv-card-badge">Coming Dec 1</span>
<!--/eftc:soon-->
<!--eftc:live-->
            <span class="gv-badge gv-badge-tan gv-card-badge">New</span>
<!--/eftc:live-->
          </div>
          <div class="gv-card-body">
            <h3>Give With Your Taxes</h3>
            <p>Redirect up to $1,700 of your federal income taxes ($3,400 for couples filing jointly) to scholarships for Covenant students through a new federal tax credit.</p>
<!--eftc:soon-->
            <div class="gv-actions"><a class="gv-btn" href="#tax-credit">Learn More</a></div>
<!--/eftc:soon-->
<!--eftc:live-->
            <div class="gv-actions"><a class="gv-btn" href="/federal-tax-credit">Pledge Now</a></div>
<!--/eftc:live-->
          </div>
        </article>
        <article class="gv-card" data-reveal>
          <div class="gv-card-img"><span class="gv-card-clip"><img src="{IMG}covenant-10-9527833.jpg" alt="" loading="lazy"></span><span class="gv-card-icon">{ICON["handshake"]}</span></div>
          <div class="gv-card-body">
            <h3>Sponsor</h3>
            <p>Partner with us through your business and invest in the resources and opportunities that help our students thrive academically, socially, and personally.</p>
            <div class="gv-actions"><a class="gv-btn" href="#sponsors">See Our Sponsors</a><a class="gv-link" href="/contact">Become a sponsor</a></div>
          </div>
        </article>
        <article class="gv-card" data-reveal>
          <div class="gv-card-img"><span class="gv-card-clip"><img src="{IMG}covenant-108-9584556.jpg" alt="" loading="lazy"></span><span class="gv-card-icon">{ICON["hand"]}</span></div>
          <div class="gv-card-body">
            <h3>Volunteer</h3>
            <p>Become a substitute teacher, or join the FTP (Family Teacher Partnership) to help in meaningful ways across our campus.</p>
            <div class="gv-actions"><a class="gv-btn" href="/contact">Get in Touch</a></div>
          </div>
        </article>
      </div>
    </div>
  </section>
{credit_block("Give With Your Federal Taxes", "A new federal tax credit lets you redirect part of your federal income taxes to scholarships for Covenant students through the Alabama Opportunity Scholarship Fund. Supporters in any state can take part.", "covenant-142-9598319.jpg").replace('class="gv-section', 'class="gv gv-section')}

  <section class="gv gv-band" style="--band-img: url('{IMG}covenant-2-9598822.jpg')">
    <div class="gv-wrap" data-reveal>
      <h2>Your Contribution Makes a Difference!</h2>
      <p>Every donation helps provide resources and enriching experiences for Covenant students.</p>
      <div class="gv-actions"><a class="gv-btn gv-btn-gold" href="{SQUARE}"{NEW_TAB}>{ICON["heart"]}Make a Donation</a></div>
      <p class="gv-note">{ICON["lock"]}Secure checkout through Square</p>
    </div>
  </section>

  <section class="gv gv-section gv-paper" id="sponsors" aria-labelledby="gv-sponsors-title">
    <div class="gv-wrap">
      <div class="gv-head" data-reveal>
        <span class="gv-eyebrow">Thank you</span>
        <h2 id="gv-sponsors-title">Our Sponsors</h2>
        <p>We're grateful to these businesses and organizations for investing in our students.</p>
      </div>
      <ul class="gv-logos">
{logos}
      </ul>
      <div class="gv-center" data-reveal>
        <div class="gv-actions"><a class="gv-btn gv-btn-line" href="/contact">Become a Sponsor</a></div>
      </div>
    </div>
  </section>
'''


# ---------------------------------------------------------------- Scholarships
INCOME = [(1, "46,950"), (2, "63,450"), (3, "79,950"), (4, "96,450"), (5, "112,950"), (6, "129,450"), (7, "145,950"), (8, "162,450")]


def scholarships():
    rows = "".join(f'<tr><th scope="row">{n} {"person" if n == 1 else "people"}</th><td>${v}</td></tr>' for n, v in INCOME)
    return f'''
  <section class="gv gv-hero gv-hero-img-anim" style="--hero-img: url('{IMG}covenant-126-9598381.jpg')">
    <div class="gv-wrap">
      <div class="gv-hero-copy">
        <span class="gv-eyebrow">Scholarship Opportunities</span>
        <h1>Every Child Deserves Access to a Quality Education</h1>
        <p class="gv-lead">We're here to help make quality education accessible through exceptional scholarship opportunities. Explore two external programs designed to support and enrich your child's educational journey.</p>
        <div class="gv-actions">
          <a class="gv-btn gv-btn-gold" href="#options">Explore Your Options</a>
          <a class="gv-btn gv-btn-ghost" href="/new-student-application">Apply to Covenant</a>
        </div>
      </div>
    </div>
  </section>

  <nav class="gv gv-jump" aria-label="On this page">
    <div class="gv-wrap">
      <span class="gv-jump-label">On this page <span class="gv-jump-hint" aria-hidden="true">Swipe for more &rarr;</span></span>
      <div class="gv-jump-links">
        <a href="#aosf"><span class="gv-num">1</span>AOSF Scholarship</a>
        <a href="#choose"><span class="gv-num">2</span>CHOOSE Act ESA</a>
        <a href="#compare">Compare</a>
        <a href="#tax-credit">For friends &amp; family</a>
        <a href="#notes">Things to note</a>
      </div>
    </div>
  </nav>

  <section class="gv gv-section gv-paper" id="options" aria-labelledby="gv-options-title">
    <div class="gv-wrap">
      <div class="gv-head" data-reveal>
        <span class="gv-eyebrow">You have options</span>
        <h2 id="gv-options-title">Two Separate Programs for Covenant Families</h2>
        <p>Covenant Christian School families can use two different programs to make a quality Christian education more affordable: an AOSF scholarship and the CHOOSE Act Education Savings Account (ESA). Each has its own application, deadlines, and requirements, so be sure to look at both.</p>
      </div>
      <div class="gv-cards gv-cards-2">
        <article class="gv-card" data-reveal>
          <div class="gv-card-img"><span class="gv-card-clip"><img src="{IMG}covenant-121-9598740.jpg" alt="" loading="lazy"></span><span class="gv-card-icon">{ICON["school"]}</span></div>
          <div class="gv-card-body">
            <span class="gv-card-kicker"><span class="gv-num">1</span>Program 1 &middot; Scholarship</span>
            <h3>Alabama Opportunity Scholarship <span class="gv-nowrap">Fund <small class="gv-abbr">(AOSF)</small></span></h3>
            <p class="gv-card-stat">Need-based scholarships</p>
            <ul class="gv-checks">
              <li>For K5–12 students</li>
              <li>Covers some or all tuition costs</li>
              <li>Applications typically open in March</li>
            </ul>
            <p class="gv-status">{ICON["clock"]}<span><strong>Not open yet.</strong> 2027–2028 applications typically open in March. Check back then!</span></p>
            <div class="gv-actions"><a class="gv-btn" href="#aosf">Learn About AOSF</a></div>
          </div>
        </article>
        <article class="gv-card" data-reveal>
          <div class="gv-card-img"><span class="gv-card-clip"><img src="{IMG}covenant-82-9584556.jpg" alt="" loading="lazy"></span><span class="gv-card-icon">{ICON["receipt"]}</span></div>
          <div class="gv-card-body">
            <span class="gv-card-kicker"><span class="gv-num">2</span>Program 2 &middot; Education Savings Account</span>
            <h3>CHOOSE Act Alabama Scholarship</h3>
            <p class="gv-card-stat">Up to <span data-count="7000" data-prefix="$">$7,000</span> per student</p>
            <ul class="gv-checks">
              <li>For K5–12 Alabama residents</li>
              <li>Tuition and other qualifying expenses</li>
              <li>Household income up to 300% of the Federal Poverty Level</li>
            </ul>
            <p class="gv-status">{ICON["clock"]}<span><strong>Not open yet.</strong> 2027–2028 dates haven't been announced. Check back for updates!</span></p>
            <div class="gv-actions"><a class="gv-btn" href="#choose">Learn About the CHOOSE Act</a></div>
          </div>
        </article>
      </div>

      <div class="gv-compare-wrap" id="compare" data-reveal>
        <h3>At a Glance</h3>
        <div class="gv-compare-scroll">
        <table class="gv-compare">
          <caption class="sr-only">Comparison of the AOSF scholarship and the CHOOSE Act Education Savings Account</caption>
          <thead><tr><th scope="col"><span class="sr-only">Detail</span></th><th scope="col"><span class="gv-num">1</span>AOSF Scholarship</th><th scope="col"><span class="gv-num">2</span>CHOOSE Act ESA</th></tr></thead>
          <tbody>
            <tr><th scope="row">What it is</th><td data-label="AOSF Scholarship">Need-based scholarship from a scholarship-granting organization</td><td data-label="CHOOSE Act ESA">State Education Savings Account (ESA)</td></tr>
            <tr class="gv-compare-key"><th scope="row">Amount</th><td data-label="AOSF Scholarship">Some or all tuition costs</td><td data-label="CHOOSE Act ESA">Up to $7,000 per student</td></tr>
            <tr><th scope="row">Who qualifies</th><td data-label="AOSF Scholarship">Income-based; priority for students zoned to a "priority school"</td><td data-label="CHOOSE Act ESA">K5–12 Alabama residents with household income up to 300% of the Federal Poverty Level</td></tr>
            <tr><th scope="row">When to apply</th><td data-label="AOSF Scholarship"><span class="gv-pill">Not open yet</span> 2027–28 applications typically open in March</td><td data-label="CHOOSE Act ESA"><span class="gv-pill">Not open yet</span> 2027–28 dates not announced yet. Last year: renewals Dec 15, new families Jan 2</td></tr>
            <tr><th scope="row">Where to apply</th><td data-label="AOSF Scholarship"><a class="gv-btn gv-btn-line gv-btn-sm" href="https://www.alabamascholarshipfund.org/" target="_blank" rel="noopener">AOSF Website</a></td><td data-label="CHOOSE Act ESA"><a class="gv-btn gv-btn-line gv-btn-sm" href="https://classwallet.com/alchoose/" target="_blank" rel="noopener">CHOOSE Act Portal</a></td></tr>
          </tbody>
        </table>
        </div>
      </div>
    </div>
  </section>

  <section class="gv gv-section gv-white" id="aosf" aria-labelledby="gv-aosf-title">
    <div class="gv-wrap">
      <div class="gv-split" style="margin-bottom:56px">
        <div data-reveal="left">
          <span class="gv-eyebrow gv-eyebrow-num"><span class="gv-num">1</span>Program 1 of 2 &middot; Scholarship</span>
          <h2 id="gv-aosf-title">Alabama Opportunity Scholarship Fund</h2>
          <p class="gv-lead" style="color:var(--muted);margin-top:16px">The Alabama Opportunity Scholarship Fund (AOSF) is a scholarship-granting organization (SGO) established under the Alabama Accountability Act of 2013. It provides need-based scholarships for K5–12 students to attend private schools like Covenant Christian School.</p>
          <div class="gv-actions">
            <a class="gv-btn" href="https://www.alabamascholarshipfund.org/"{NEW_TAB}>{ICON["external"]}Visit the AOSF Website</a>
            <a class="gv-btn gv-btn-line" href="mailto:help@alosf.org">{ICON["mail"]}Email AOSF</a>
          </div>
        </div>
        <div class="gv-split-img" data-reveal="right"><img src="{IMG}covenant-164-9598717.jpg" alt="" loading="lazy"></div>
      </div>
      <div class="gv-panels">
        <div class="gv-panel" data-reveal>
          <div class="gv-panel-icon">{ICON["users"]}</div>
          <h4>Eligibility Requirements</h4>
          <ul>
            <li>Students must meet income-based criteria.</li>
            <li>Priority is given to students zoned to a public school deemed a "priority school" (those receiving a D or F on the Alabama School Report Card).</li>
          </ul>
        </div>
        <div class="gv-panel" data-reveal>
          <div class="gv-panel-icon">{ICON["info"]}</div>
          <h4>Key Details</h4>
          <ul>
            <li>Scholarships cover some or all tuition costs.</li>
            <li>Students already receiving AOSF scholarships may be eligible to transfer their award to Covenant Christian School.</li>
          </ul>
        </div>
        <div class="gv-panel" data-reveal>
          <div class="gv-panel-icon">{ICON["calendar"]}</div>
          <h4>How to Apply</h4>
          <ul>
            <li><strong>Applications for 2027–2028 are not open yet.</strong> They typically open in March, so check back then.</li>
            <li>Visit the <a href="https://www.alabamascholarshipfund.org/"{NEW_TAB}>AOSF website</a> regularly for updates.</li>
            <li>For assistance, email <a href="mailto:help@alosf.org">help@alosf.org</a>.</li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <section class="gv gv-section gv-paper" id="choose" aria-labelledby="gv-choose-title">
    <div class="gv-wrap">
      <div class="gv-head" data-reveal>
        <span class="gv-eyebrow gv-eyebrow-num"><span class="gv-num">2</span>Program 2 of 2 &middot; Education Savings Account</span>
        <h2 id="gv-choose-title">CHOOSE Act Alabama Scholarship</h2>
        <p>The CHOOSE Act establishes Alabama's Education Savings Account (ESA) program, providing eligible families with up to $7,000 per student to cover tuition and other qualifying educational expenses. Funds may be used for approved educational services beginning in the 2026–2027 academic year.</p>
      </div>
      <div class="gv-split" style="align-items:start">
        <div data-reveal="left">
          <h3>Who Qualifies for 2026–2027?</h3>
          <p style="color:var(--muted);margin:10px 0 16px">To be eligible, a student must:</p>
          <ul class="gv-checks">
            <li>Be enrolled in grades K5–12</li>
            <li>Be a resident of Alabama</li>
            <li>Live in a household whose income does not exceed 300% of the Federal Poverty Level (FPL) for the 2025 tax year</li>
          </ul>
          <h4 style="margin:30px 0 12px">Also served by the program</h4>
          <ul class="gv-checks">
            <li>The first 500 students with special needs</li>
            <li>Dependents of active-duty service members zoned for a priority school</li>
            <li>Students with family incomes up to 300% of the federal poverty level</li>
          </ul>
        </div>
        <div class="gv-table-card" data-reveal="right">
          <h4>Income Eligibility</h4>
          <p>300% of the 2025 Federal Poverty Level</p>
          <table class="gv-table">
            <caption class="sr-only">Income limits by household size: 300% of the 2025 Federal Poverty Guideline</caption>
            <thead><tr><th scope="col">Household size</th><th scope="col">Income limit</th></tr></thead>
            <tbody>{rows}</tbody>
          </table>
          <p class="gv-table-note">More than 8 people? Add $16,500 for each additional person.</p>
        </div>
      </div>

      <div style="margin-top:64px">
        <h3 data-reveal style="margin-bottom:18px">Application Timeline</h3>
        <div class="gv-notice" data-reveal>{ICON["calendar"]}<div><strong>2027–2028 applications are not open yet.</strong><p>The state hasn't announced dates for next school year. Check back here for updates. Families are encouraged to apply as early as possible once the portal opens.</p></div></div>
        <p data-reveal class="gv-timeline-label">For reference, last year's dates (2026–2027):</p>
        <ol class="gv-timeline">
          <li data-reveal><span class="gv-date"><b>Dec</b><span>15</span></span><h4>Renewals opened</h4><p>For current participants: December 15, 2025</p></li>
          <li data-reveal><span class="gv-date"><b>Jan</b><span>2</span></span><h4>New family applications opened</h4><p>For new families: January 2, 2026</p></li>
        </ol>
      </div>

      <div style="margin-top:56px">
        <h3 data-reveal style="margin-bottom:22px">Parent Resources</h3>
        <div class="gv-resources">
          <a class="gv-resource" data-reveal href="https://classwallet.com/alchoose/assets/CHOOSE_ACT_parent_guide_2026-2027.pdf"{NEW_TAB}><span class="gv-resource-icon">{ICON["file"]}</span><span><strong>Parent Guide (PDF)</strong><span>Program details, approved expenses and step-by-step instructions</span></span></a>
          <a class="gv-resource" data-reveal href="https://drive.google.com/file/d/1f1fXEO_dFj1NRuJusxzScO4yMQC-Nj_t/view?usp=sharing"{NEW_TAB}><span class="gv-resource-icon">{ICON["play"]}</span><span><strong>Watch the Presentation</strong><span>The CHOOSE Act explained</span></span></a>
          <a class="gv-resource" data-reveal href="https://classwallet.com/alchoose/"{NEW_TAB}><span class="gv-resource-icon">{ICON["external"]}</span><span><strong>CHOOSE Act Portal</strong><span>Official program website</span></span></a>
        </div>
      </div>
    </div>
  </section>
{credit_block("A New Way Friends and Family Can Help", "Grandparents, relatives and supporters in any state will be able to redirect part of their federal income taxes to AOSF scholarships for Covenant families through the new Education Freedom Tax Credit.", "covenant-21-9528197.jpg").replace('class="gv-section', 'class="gv gv-section')}

  <section class="gv gv-section gv-soft" id="notes" aria-labelledby="gv-note-title">
    <div class="gv-wrap">
      <div class="gv-head" data-reveal><span class="gv-eyebrow">Before you apply</span><h2 id="gv-note-title">Things to Note</h2></div>
      <div class="gv-cards gv-cards-2">
        <div class="gv-panel" data-reveal>
          <div class="gv-panel-icon">{ICON["check"]}</div>
          <h4>Complete Enrollment</h4>
          <p>Families must complete Covenant Christian School's enrollment process to ensure space is available in the desired grade level.</p>
          <div class="gv-actions"><a class="gv-btn" href="/new-student-application">Apply Today</a></div>
        </div>
        <div class="gv-panel" data-reveal>
          <div class="gv-panel-icon">{ICON["info"]}</div>
          <h4>Scholarship &ne; Enrollment</h4>
          <p>Scholarships or ESAs do not guarantee enrollment.</p>
          <div class="gv-actions"><a class="gv-btn gv-btn-line" href="https://content.app-sources.com/s/641329925069930801/uploads/PDF_Files/External_Scholarships_Info_Dec2024-4631514.pdf"{NEW_TAB}>{ICON["file"]}Scholarships Info (PDF)</a></div>
        </div>
      </div>
    </div>
  </section>
{help_strip("We encourage you to explore these opportunities to make a Covenant Christian School education possible for your family. Contact our office with questions; we're here to help guide you every step of the way!").replace('class="gv-section', 'class="gv gv-section')}
'''


# ---------------------------------------------------------------- Federal tax credit
WIDGET = """<div id="theodore-giving-embed"></div>
<script src="https://aosf.theolearning.com/embed.js"
        data-base-url="https://aosf.theolearning.com"
        data-public-key="JGBH9Zv13Fsr6hKWbMGDrydX"
        data-primary-color="#daad86"
        data-secondary-color="#153553"></script>"""


def tax_credit():
    return f'''
  <section class="gv gv-tc-top" aria-labelledby="gv-tc-title" style="--hero-img: url('{IMG}covenant-151_1-9523341.jpg')">
    <div class="gv-wrap gv-tc-grid">
      <div class="gv-tc-hero">
        <span class="gv-badge gv-badge-tan">New in 2027</span>
        <h1 id="gv-tc-title">Turn Your Federal Taxes Into Scholarships for Covenant Students</h1>
        <p class="gv-lead">The Education Freedom Tax Credit lets you redirect part of your federal income taxes to scholarships for Covenant Christian School families, starting January 2027.</p>
        <div class="gv-tc-chips">
          <div><strong data-count="1700" data-prefix="$">$1,700</strong><span>credit per individual</span></div>
          <div><strong data-count="3400" data-prefix="$">$3,400</strong><span>married filing jointly</span></div>
        </div>
      </div>

      <div class="gv-tc-form" id="pledge">
        <div class="gv-tc-card">
          <div class="gv-tc-card-head"><h2>Make Your Pledge</h2><p>No payment is due today.</p></div>
          {WIDGET}
          <noscript><p style="padding:16px 24px">This form needs JavaScript. Please <a href="/contact">contact our office</a> to pledge.</p></noscript>
          <p class="gv-tc-trust">{ICON["lock"]}Pledges are handled by the Alabama Opportunity Scholarship Fund</p>
        </div>
      </div>

      <div class="gv-tc-below" id="how">
        <h2 data-reveal>How It Works</h2>
        <ol class="gv-steps">
          <li data-reveal><span class="gv-step-icon">{ICON["pen"]}</span><h4>Pledge today</h4><p>Use the form to let us know you plan to give. Pledging now helps us plan scholarships for next year.</p></li>
          <li data-reveal><span class="gv-step-icon">{ICON["gift"]}</span><h4>Give through AOSF in 2027</h4><p>When the program opens in January 2027, your gift goes to the Alabama Opportunity Scholarship Fund, a scholarship-granting organization, with Covenant Christian School selected as your school.</p></li>
          <li data-reveal><span class="gv-step-icon">{ICON["receipt"]}</span><h4>Claim your credit</h4><p>Claim the dollar-for-dollar credit on your 2027 federal tax return. Your tax professional can confirm how it applies to you.</p></li>
        </ol>
      </div>
    </div>
  </section>

  <section class="gv gv-section gv-soft" aria-labelledby="gv-know-title">
    <div class="gv-wrap">
      <div class="gv-head" data-reveal><span class="gv-eyebrow">Good to know</span><h2 id="gv-know-title">Why Pledge Now?</h2></div>
      <div class="gv-panels">
        <div class="gv-panel" data-reveal><div class="gv-panel-icon">{ICON["map"]}</div><h4>Any state can give</h4><p>Grandparents, alumni and friends anywhere in the country can take part, not just Alabama residents.</p></div>
        <div class="gv-panel" data-reveal><div class="gv-panel-icon">{ICON["clock"]}</div><h4>First come, first served</h4><p>Credits are limited by a national cap, so pledging early helps make sure your gift counts.</p></div>
        <div class="gv-panel" data-reveal><div class="gv-panel-icon">{ICON["users"]}</div><h4>Helps Covenant families</h4><p>Scholarships support K–12 students in households earning up to 300% of their area's median income.</p></div>
      </div>
    </div>
  </section>

  <section class="gv gv-section gv-paper" aria-labelledby="gv-faq-title">
    <div class="gv-wrap">
      <div class="gv-head" data-reveal><span class="gv-eyebrow">Questions</span><h2 id="gv-faq-title">Frequently Asked Questions</h2></div>
      <div class="gv-faq">
        <details data-reveal><summary>What is the Education Freedom Tax Credit?</summary><div><p>A new federal tax credit that starts in 2027. When you give to a scholarship-granting organization like the Alabama Opportunity Scholarship Fund, you can receive a dollar-for-dollar credit on your federal income taxes.</p></div></details>
        <details data-reveal><summary>How much can I redirect?</summary><div><p>Up to $1,700 per individual taxpayer, or up to $3,400 for married couples filing jointly.</p></div></details>
        <details data-reveal><summary>Do I need to live in Alabama?</summary><div><p>No. Taxpayers in any state can give to an Alabama scholarship-granting organization and claim the credit.</p></div></details>
        <details data-reveal><summary>Does my gift go directly to Covenant?</summary><div><p>Your gift goes to the Alabama Opportunity Scholarship Fund (AOSF), which awards scholarships to students. You select Covenant Christian School on the form.</p></div></details>
        <details data-reveal><summary>Do I pay anything when I pledge?</summary><div><p>No. A pledge lets us know you plan to give. You'll make your gift once the program opens in January 2027.</p></div></details>
        <details data-reveal><summary>Is the credit refundable?</summary><div><p>No. It is a nonrefundable credit, which means it can reduce the federal income tax you owe. Please talk with a tax professional about your situation.</p></div></details>
      </div>
      <p class="gv-disclaimer">Covenant Christian School does not provide tax advice. Please consult a tax professional about your situation.</p>
    </div>
  </section>

  <section class="gv gv-section gv-dark">
    <div class="gv-wrap gv-help" data-reveal>
      <div>
        <h2>Ready to Help a Covenant Student?</h2>
        <p>Make your pledge today, or reach out with questions. You can also learn more from the <a href="https://www.alabamascholarshipfund.org/"{NEW_TAB}>Alabama Opportunity Scholarship Fund</a>.</p>
      </div>
      <div class="gv-actions"><a class="gv-btn gv-btn-gold" href="#pledge">Make Your Pledge</a><a class="gv-btn gv-btn-ghost" href="/contact">Contact Our Office</a></div>
    </div>
  </section>
'''


# ---------------------------------------------------------------- assembly
def shell(source, chrome="scholarship-opportunities.html"):
    """Page <head> from `source`; body chrome (solid white header, footer) from `chrome`
    so all giving pages share the same header instead of the transparent overlay one."""
    html = (PAGES / source).read_text()
    if chrome != source:
        base = (PAGES / chrome).read_text()
        html = html[:html.index("</head>")] + base[base.index("</head>"):]
    html = re.sub(r'<section class="eftc eftc-callout"[\s\S]*?</section>\s*', '', html)
    html = html.replace('<link rel="stylesheet" href="/assets/eftc.css"><script src="/assets/eftc.js" defer></script>', '')
    html = html.replace('<link rel="stylesheet" href="/assets/eftc.css">', '')
    html = re.sub(r'<link rel="stylesheet" href="/assets/giving\.css[^"]*"><script src="/assets/giving\.js[^"]*" defer></script>', '', html)
    html = html.replace("</head>", HEAD_EXTRA + "</head>", 1)
    return html


def with_main(html, content):
    start = html.index('<main id="main-content" tabindex="-1">') + len('<main id="main-content" tabindex="-1">')
    end = html.index("</main>")
    return html[:start] + "\n<div class=\"content-wrapper\"><div class=\"content\">" + content + "</div></div>\n  " + html[end:]


def build():
    (OUT / "ways-to-give.html").write_text(with_main(shell("ways-to-give.html"), ways_to_give()))
    (OUT / "scholarship-opportunities.html").write_text(with_main(shell("scholarship-opportunities.html"), scholarships()))
    # Tax credit page: reuse its current head (title, meta), swap in the new body.
    tc = shell("federal-tax-credit.html")
    (PAGES / "federal-tax-credit.html").write_text(with_main(tc, tax_credit()))
    print("Built ways-to-give.html, scholarship-opportunities.html, federal-tax-credit.html")


if __name__ == "__main__":
    build()
