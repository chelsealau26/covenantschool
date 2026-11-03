"""Preview-only redesign of /employment-openings.
The application form (fields, spam protection, submit script) is copied at build time from the
live page, so it always matches what /api/employment-application expects. The position chips are
read from the form's own <select>, so they can never list a role the form doesn't offer."""
import re, html as H

def form_block(pages):
    t = (pages / "employment-openings.html").read_text()
    m = t[t.index("<main"):t.index("</main>")]
    return m[m.index("<style"):m.rindex("</script>") + len("</script>")]

def positions(block):
    sel = re.search(r'<select id="ef-position"[\s\S]*?</select>', block).group(0)
    return [H.unescape(o).strip() for o in re.findall(r"<option>([^<]+)</option>", sel)]

def employment(ICON, IMG, pages):
    block = form_block(pages)
    chips = "".join(
        f'<li><button type="button" class="ep-role" data-pick-position="{H.escape(p, quote=True)}">'
        f'<span class="ep-role-n" aria-hidden="true">{i:02d}</span><span class="ep-role-t">{H.escape(p)}</span>'
        f'<span class="ep-role-go" aria-hidden="true"></span></button></li>'
        for i, p in enumerate(positions(block), 1))
    return f'''
  <section class="gv gv-hero gv-hero-split ep-hero">
    <img class="ep-hero-eagle" src="{IMG}eagle-mark-white.png" alt="" width="900" height="321">
    <div class="gv-hero-photo" style="background-image: url('{IMG}covenant-2-9598822.jpg')" aria-hidden="true"></div>
    <div class="gv-wrap">
      <div class="gv-hero-copy">
        <span class="gv-eyebrow">Join our team</span>
        <h1>Employment Opportunities</h1>
        <p class="gv-lead">Discover the career opportunities and joy-filled days awaiting you at Covenant Christian School.</p>
        <div class="gv-actions"><a class="gv-btn gv-btn-ghost" href="#apply">Apply below</a></div>
      </div>
    </div>
  </section>

  <section class="gv gv-section gv-white ep-roles" aria-labelledby="ep-roles-title">
    <div class="gv-wrap">
      <div class="ep-roles-head" data-reveal>
        <h2 id="ep-roles-title">Positions you can apply for<span class="mv-dot" aria-hidden="true">.</span></h2>
        <p>Choose one to start your application.</p>
      </div>
      <ul class="ep-role-grid" data-reveal>{chips}</ul>
    </div>
  </section>

  <section class="gv gv-section ep-apply" id="apply" aria-labelledby="ep-apply-title">
    <img class="ep-apply-eagle" src="{IMG}eagle-mark-white.png" alt="" width="900" height="321">
    <div class="gv-wrap ep-grid">
      <div class="ep-side" data-reveal>
        <h2 id="ep-apply-title">Apply<span class="mv-dot" aria-hidden="true">.</span></h2>
        <p class="ep-intro">Interested in joining the Covenant faculty or staff? We’d love to hear from you! Please fill out the form below and we will be in touch with you shortly.</p>
        <div class="hm-frame ep-frame"><svg class="hm-frame-line" aria-hidden="true" focusable="false"><rect x="1" y="1" rx="4" ry="4"/></svg><img src="{IMG}covenant-47-9584556.jpg" alt="A Covenant teacher helping a student with her tablet assignment" loading="lazy"></div>
        <ul class="ep-contact" aria-label="Questions about working at Covenant">
          <li><span class="hm-col-icon">{ICON["phone"]}</span><a href="tel:251-633-8055">251-633-8055</a></li>
          <li><span class="hm-col-icon">{ICON["mail"]}</span><a href="mailto:info@covenantschool.com">info@covenantschool.com</a></li>
        </ul>
      </div>
      <div class="ep-card" data-reveal>
        {block}
      </div>
    </div>
  </section>
'''
