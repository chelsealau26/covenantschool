"""Preview-only redesign of /athletics. All wording and links from the live page."""
import re

PDF = "https://content.app-sources.com/s/641329925069930801/uploads/PDF_Files/"
APP = "https://aware3.net/shortcode/?code=covenantchristianschool-f"

def athletics(ICON, IMG, NEW_TAB, pages):
    I = ICON
    live = (pages / "athletics.html").read_text()
    portal = re.search(r'href="(https://sis\.factsmgt\.com/accounts/Account/Login[^"]+)"', live).group(1)
    sports = ["Cheer", "Volleyball", "Track", "Basketball", "Soccer"]
    run = "".join(f"<span>{s}</span><i></i>" for s in sports + ["Cross-Country"])
    forms = [("Athletic Agreement", "All set for the upcoming sports season? Please download and complete our Athletic Agreement.", "CCS_Athlete_Agreement_and_Consent-2620686.pdf"),
             ("Physical Form", "Download and turn completed form in to the office to ensure you are ready to play.", "Sports-Physical-Form-20-21-2624521.pdf"),
             ("Concussion Form", "Download and turn completed form in to the office to meet all the necessary safety requirements.", "2024-25_Concussion_Form-3822474.pdf")]
    gallery = [("IMG9765835418510632102-2618059.jpg", "Covenant girls' basketball team in navy jerseys posing with their two coaches", "at-g1"),
               ("fb/ccs-vb-ready.jpg", "A smiling Covenant volleyball player ready to receive the ball", "at-g2"),
               ("IMG967725093324521546-2618059.jpg", "Covenant boys' basketball team in navy jerseys posing with their coaches in the gym", "at-g3"),
               ("fb/ccs-track-medals.jpg", "Three Covenant runners wearing their race medals", "at-g4"),
               ("IMG_3459-2618059.jpg", "Covenant girls' soccer team in navy jerseys posing together on the soccer field", "at-g5"),
               ("fb/ccs-xc-team.jpg", "The Covenant cross-country team and cheerleaders together on the grass", "at-g6")]
    return f'''
  <section class="gv tu-hero2 at-hero" data-scroll-dim aria-labelledby="at-title">
    <div class="tu-hero2-img" style="background-image: url('{IMG}fb/ccs-vb-set.jpg')" aria-hidden="true"></div>
    <div class="gv-wrap tu-hero2-copy">
      <span class="gv-eyebrow">Cheer • Volleyball • Track • Basketball • Soccer</span>
      <h1 id="at-title">Get in the Game: <span class="at-l2">Explore Covenant Athletics</span></h1>
      <p class="gv-lead">We aim to inspire teamwork, skill development, and sportsmanship through our vibrant athletic programs.</p>
      <div class="gv-actions">
        <a class="gv-btn gv-btn-gold" href="#forms">Athletic Forms</a>
        <a class="gv-btn gv-btn-ghost" href="#schedules">Game Schedules</a>
      </div>
    </div>
  </section>

  <div class="at-ticker" aria-hidden="true"><div class="at-ticker-run">{run}{run}{run}</div></div>

  <section class="gv gv-section gv-white at-join" aria-labelledby="at-join-title">
    <div class="gv-wrap at-join-grid">
      <div class="at-join-text" data-reveal>
        <span class="gv-eyebrow">Join the Excitement</span>
        <h2 id="at-join-title">Discover Your Passion and Be Part of Our Winning Teams<span class="mv-dot" aria-hidden="true">.</span></h2>
        <p class="at-big">The athletic department at Covenant offers many opportunities for our students!</p>
        <p>We field elementary and middle school teams in Cross-Country, Track, Cheer, Girls Volleyball, Girls and Boys Basketball, and Girls and Boys Soccer.</p>
        <p class="ns-statement">Our goals are to teach strong fundamentals and teamwork in a positive, Christ-honoring environment. Many of our graduates have gone on to successful experiences in high school athletics.</p>
      </div>
      <div class="at-gallery" data-reveal="left">{"".join(f'<figure class="{c}"><img src="{IMG}{s}" alt="{a}" loading="lazy"></figure>' for s, a, c in gallery)}</div>
    </div>
  </section>

  <section class="gv gv-section at-sched" id="schedules" aria-labelledby="at-sched-title">
    <div class="gv-wrap at-sched-grid">
      <div class="hm-frame at-sched-photo" data-reveal="right"><svg class="hm-frame-line" aria-hidden="true" focusable="false"><rect x="1" y="1" rx="4" ry="4"/></svg><img src="{IMG}fb/ccs-vb-serve.jpg" alt="A Covenant volleyball player serving during a game" loading="lazy"></div>
      <div data-reveal>
        <span class="gv-eyebrow">Game Day</span>
        <h2 id="at-sched-title">Stay Up-to-Date on Game Schedules</h2>
        <p>All athletic events are available in real time through the Family Portal. For the most accurate and current info, check the Covenant app or log in.</p>
        <div class="gv-actions">
          <a class="gv-btn gv-btn-gold" href="{APP}"{NEW_TAB}>Download the App</a>
          <a class="gv-btn gv-btn-ghost" href="{portal}"{NEW_TAB}>Check the Parent Portal</a>
        </div>
      </div>
    </div>
  </section>

  <section class="gv gv-section gv-paper at-forms" id="forms" aria-labelledby="at-forms-title">
    <div class="gv-wrap">
      <div class="tu-head at-forms-head" data-reveal>
        <span class="gv-eyebrow">Athletic Forms</span>
        <h2 id="at-forms-title">Explore the Essentials<span class="mv-dot" aria-hidden="true">.</span></h2>
        <p>Stay up-to-date and download important athletic forms to ensure your child is ready to participate in Covenant's exciting sports programs.</p>
      </div>
      <ol class="at-form-list">{"".join(f'<li data-reveal><span class="at-form-n" aria-hidden="true">0{n}</span><div class="at-form-body"><h3>{t}</h3><p>{d}</p></div><a class="at-form-dl" href="{PDF}{f}"{NEW_TAB} aria-label="Download Now: {t} (PDF)"><span class="at-dl-ic" aria-hidden="true">{I["file"]}</span>Download Now</a></li>' for n, (t, d, f) in enumerate(forms, 1))}</ol>
    </div>
  </section>

  <section class="gv at-cta" aria-labelledby="at-cta-title">
    <div class="at-cta-img" style="background-image: url('{IMG}fb/ccs-volleyball-team.jpg')" aria-hidden="true"></div>
    <div class="gv-wrap at-cta-copy" data-reveal>
      <h2 id="at-cta-title">Interested in playing a sport this year? Reach out to our Athletic Department!</h2>
      <div class="gv-actions"><a class="gv-btn gv-btn-gold" href="mailto:athletics@covenantschool.com">Email Athletic Director</a></div>
    </div>
  </section>
'''
