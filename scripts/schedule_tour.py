"""Preview-only redesign of /schedule-tour. Wording kept from the live page and homepage."""

CALENDLY = "https://calendly.com/kdees-covenantschool/30min?hide_gdpr_banner=1&primary_color=153553"

GALLERY = [  # file, alt, layout class
    ("covenant-21-9528197", "Middle school students working at their desks", "is-wide"),
    ("covenant-47-9584556", "A teacher helping a student with her tablet assignment", ""),
    ("covenant-142-9598319", "A smiling young student putting together a puzzle", "is-tall"),
    ("covenant-126-9598381", "A young student writing at his desk", ""),
    ("covenant-2-9598822", "A teacher working one-on-one with a student", ""),
    ("covenant-89-9603932", "Two boys playing basketball outside", "is-wide"),
    ("covenant-78-9798253", "A student taking notes next to her tablet", ""),
    ("covenant-66-9527920", "Students reading and writing at their desks", "is-wide"),
    ("fb/ccs-chapel-friends", "Three smiling little girls hugging in chapel", ""),
    ("fb/ccs-letter-jackets", "Middle school girls in Covenant letter jackets", "is-wide"),
    ("fb/ccs-science-lab", "Students smiling during a science lab", ""),
    ("fb/ccs-worship-band", "Students leading worship in chapel", "is-wide"),
]

def schedule_tour(ICON, IMG, maps_url, new_tab):
    tiles = "".join(f'<figure class="st-g {c}"><img src="{IMG}{f}.jpg" alt="{a}" loading="lazy"></figure>' for f, a, c in GALLERY)
    return f'''
  <section class="gv gv-hero gv-hero-split ep-hero st-hero">
    <img class="ep-hero-eagle" src="{IMG}eagle-mark-white.png" alt="" width="900" height="321">
    <div class="gv-hero-photo" style="background-image: url('{IMG}covenant-95-9602737.jpg')" aria-hidden="true"></div>
    <div class="gv-wrap">
      <div class="gv-hero-copy">
        <span class="gv-eyebrow">Admissions</span>
        <h1>Schedule Your School Tour Today!</h1>
        <p class="gv-lead">Take the next step in your child’s future! Fill out the scheduling form below or give us a call at <a class="st-tel" href="tel:251-633-8055">251-633-8055</a> to book your personal tour. Come see firsthand how Covenant Christian School can inspire and shape your child’s growth and success.</p>
        <div class="gv-actions">
          <a class="gv-btn gv-btn-gold" href="#book">{ICON["calendar"]}Pick a Tour Time</a>
          <a class="gv-btn gv-btn-ghost" href="tel:251-633-8055">{ICON["phone"]}Call 251-633-8055</a>
        </div>
      </div>
    </div>
  </section>

  <section class="gv gv-section ep-apply st-book" id="book" aria-labelledby="st-book-title">
    <img class="ep-apply-eagle" src="{IMG}eagle-mark-white.png" alt="" width="900" height="321">
    <div class="gv-wrap ep-grid st-grid">
      <div class="ep-side" data-reveal>
        <h2 id="st-book-title">Book your tour<span class="mv-dot" aria-hidden="true">.</span></h2>
        <ol class="st-steps">
          <li><span class="st-n">01</span><div><h3>Choose a time</h3><p>Pick any open 30-minute slot on the calendar.</p></div></li>
          <li><span class="st-n">02</span><div><h3>Explore!</h3><p>Tour the campus, visit classrooms, and meet prospective teachers.</p></div></li>
          <li><span class="st-n">03</span><div><h3>Where?</h3><p>7150 Hitt Rd.<br>Mobile, AL 36695</p><a class="gv-btn gv-btn-ghost st-dir" href="{maps_url}"{new_tab}>{ICON["pin"]}Directions</a></div></li>
        </ol>
        <p class="st-call">Prefer to talk to someone? <a href="tel:251-633-8055">Call 251-633-8055</a></p>
      </div>
      <div class="ep-card st-card" data-reveal>
        <iframe src="{CALENDLY}" title="Schedule a school tour (booking calendar)" loading="lazy"></iframe>
      </div>
    </div>
  </section>

  <section class="gv gv-section gv-white st-life" aria-labelledby="st-life-title">
    <div class="gv-wrap">
      <div class="ep-roles-head" data-reveal>
        <h2 id="st-life-title">A glimpse of campus life<span class="mv-dot" aria-hidden="true">.</span></h2>
        <p>What you’ll see on your visit.</p>
      </div>
      <div class="st-gallery" data-reveal>{tiles}</div>
    </div>
  </section>
'''
