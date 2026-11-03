"""Preview-only redesign of /employment-openings.
The application form (fields, spam protection, submit script) is copied at build time from the
live page, so it always matches what /api/employment-application expects."""
import re

def form_block(pages):
    t = (pages / "employment-openings.html").read_text()
    m = t[t.index("<main"):t.index("</main>")]
    return m[m.index("<style"):m.rindex("</script>") + len("</script>")]

def employment(ICON, IMG, pages):
    return f'''
  <section class="gv gv-hero ep-hero" style="--hero-img: url('{IMG}covenant-123-9584556.jpg')">
    <div class="gv-wrap">
      <div class="gv-hero-copy">
        <span class="gv-eyebrow">Join our team</span>
        <h1>Employment Opportunities</h1>
        <p class="gv-lead">Discover the career opportunities and joy-filled days awaiting you at Covenant Christian School.</p>
        <div class="gv-actions"><a class="gv-btn gv-btn-ghost" href="#apply">Apply below</a></div>
      </div>
    </div>
  </section>

  <section class="gv gv-section gv-paper" id="apply" aria-labelledby="ep-apply-title">
    <div class="gv-wrap ep-grid">
      <div class="ep-side" data-reveal>
        <h2 id="ep-apply-title">Apply<span class="mv-dot" aria-hidden="true">.</span></h2>
        <p class="ep-intro">Interested in joining the Covenant faculty or staff? We’d love to hear from you! Please fill out the form below and we will be in touch with you shortly.</p>
        <div class="hm-frame ep-frame"><svg class="hm-frame-line" aria-hidden="true" focusable="false"><rect x="1" y="1" rx="4" ry="4"/></svg><img src="{IMG}covenant-44-9527765.jpg" alt="A Covenant teacher helping a student with her work" loading="lazy"></div>
        <ul class="ep-contact" aria-label="Questions about working at Covenant">
          <li><span class="hm-col-icon">{ICON["phone"]}</span><a href="tel:251-633-8055">251-633-8055</a></li>
          <li><span class="hm-col-icon">{ICON["mail"]}</span><a href="mailto:info@covenantschool.com">info@covenantschool.com</a></li>
        </ul>
      </div>
      <div class="ep-card" data-reveal>
        {form_block(pages)}
      </div>
    </div>
  </section>
'''
