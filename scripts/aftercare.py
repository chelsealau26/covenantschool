"""Preview-only redesign of /aftercare. All wording and links from the live page."""

APP = "https://aware3.net/shortcode/?code=covenantchristianschool-f"
IOS = "https://apps.apple.com/us/app/id1636762809"
AND = "https://play.google.com/store/apps/details?id=com.airealmobile.covenantchristianschool_f_35647"
APPLE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M16.4 12.6c0-2.6 2.1-3.8 2.2-3.9-1.2-1.8-3.1-2-3.7-2-1.6-.2-3.1.9-3.9.9-.8 0-2-.9-3.4-.9-1.7 0-3.3 1-4.2 2.6-1.8 3.1-.5 7.7 1.3 10.2.9 1.2 1.9 2.6 3.2 2.6 1.3-.1 1.8-.8 3.3-.8 1.6 0 2 .8 3.4.8 1.4 0 2.3-1.3 3.1-2.5 1-1.4 1.4-2.8 1.4-2.9-.1 0-2.7-1-2.7-4.1zM13.9 5c.7-.9 1.2-2.1 1.1-3.3-1 0-2.3.7-3 1.6-.7.8-1.2 2-1.1 3.2 1.1.1 2.3-.6 3-1.5z"/></svg>'
PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M3.6 2.3c-.3.3-.5.8-.5 1.4v16.6c0 .6.2 1.1.5 1.4l9.3-9.7-9.3-9.7zm10.4 8.6 2.6-2.7L5.4 1.8c-.4-.2-.8-.3-1.1-.2l9.7 9.3zm0 2.2-9.7 9.3c.3.1.7 0 1.1-.2l11.2-6.4-2.6-2.7zm6.6-2.6-3-1.7-2.8 2.9 2.8 2.9 3-1.7c.9-.5.9-1.9 0-2.4z"/></svg>'
AFFIDAVIT = "https://content.app-sources.com/s/641329925069930801/uploads/PDF_Files/K3K4AfterCare_DHRrequired_Parent_Affidavit__ExemptNotifcation_Updated_5-6-2025-7687155.pdf"

def aftercare(ICON, IMG, NEW_TAB):
    I = ICON
    steps = [("01", "AfterCare Enrollment", "Please review our AfterCare policies, complete and submit in order to sign up for AfterCare services.", APP, "Enroll Now", "portal"),
             ("02", "AfterCare Affidavit", "Complete and submit your affidavit to ensure all the requirements are met to sign up for AfterCare services.", AFFIDAVIT, "Download Now", "file"),
             ("03", "Weekly Sign Up", 'Please submit this form each Friday by 2:30 p.m. If changes occur please call the office at <a href="tel:251-633-8055">251-633-8055</a>.', APP, "Sign Up Now", "calendar")]
    rates = [("$155", "/mo", "AfterCare 3:30pm - 5:30pm", "CCS Aftercare $155/mo (3+days/wk regular daily attendance)"),
             ("$10", "/day", "AfterCare Cost Per Day", "CCS Aftercare $10/day (1-2 days regular daily attendance/wk)"),
             ("$30", "/day", "Emergency Drop-In", "CCS Aftercare $30/day drop-in attendance for all programs.")]
    return f'''
  <section class="gv tu-hero2 ac-hero" data-scroll-dim aria-labelledby="ac-title">
    <div class="tu-hero2-img" style="background-image: url('{IMG}covenant-92-9517625.jpg')" aria-hidden="true"></div>
    <div class="gv-wrap tu-hero2-copy">
      <span class="gv-eyebrow">Parent Central</span>
      <h1 id="ac-title">AfterCare</h1>
      <p class="gv-lead">Explore our aftercare program designed to provide a safe and engaging environment for students after school hours. Visit our Family Portal Resource section to sign up for AfterCare services.</p>
      <div class="gv-actions">
        <a class="gv-btn gv-btn-gold" href="{APP}"{NEW_TAB}>Weekly Sign Up</a>
        <a class="gv-btn gv-btn-ghost" href="{APP}"{NEW_TAB}>Enroll Now</a>
      </div>
    </div>
  </section>

  <section class="gv gv-section gv-white ac-steps-sec" aria-labelledby="ac-steps-title">
    <div class="gv-wrap">
      <div class="tu-head ac-head" data-reveal>
        <span class="gv-eyebrow">AfterCare</span>
        <h2 id="ac-steps-title">Getting Started<span class="mv-dot" aria-hidden="true">.</span></h2>
      </div>
      <ol class="ac-steps">{"".join(f'<li data-reveal><span class="ac-step-n" aria-hidden="true">{n}</span><span class="hm-col-icon">{I[ic]}</span><h3>{t}</h3><p>{d}</p><a class="ac-step-link" href="{h}"{NEW_TAB}>{b}<span aria-hidden="true"> →</span></a></li>' for n, t, d, h, b, ic in steps)}</ol>
    </div>
  </section>

  <section class="gv gv-section ac-rates" id="ac-rates" aria-labelledby="ac-rates-title">
    <div class="gv-wrap ac-rates-grid">
      <div class="ac-rates-photo hm-frame" data-reveal="right"><svg class="hm-frame-line" aria-hidden="true" focusable="false"><rect x="1" y="1" rx="4" ry="4"/></svg><img src="{IMG}covenant-89-9603932.jpg" alt="Two Covenant students playing basketball outside" loading="lazy"></div>
      <div data-reveal>
        <h2 id="ac-rates-title" class="ftp-sr">AfterCare rates</h2>
        <ul class="ac-rate-list">{"".join(f'<li><div class="ac-price"><strong>{p}</strong><span>{u}</span></div><div><h3>{t}</h3><p>{d}</p></div></li>' for p, u, t, d in rates)}</ul>
        <div class="ac-pay"><span class="hm-col-icon">{I["receipt"]}</span><div><h3>AfterCare Payments</h3><p>Payments for AfterCare will be added to your monthly school tuition.</p></div></div>
      </div>
    </div>
  </section>

  <section class="gv gv-section gv-paper ac-app" aria-labelledby="ac-app-title">
    <div class="gv-wrap ac-app-grid">
      <div class="ac-app-text" data-reveal>
        <span class="gv-eyebrow">Sign Up in the App</span>
        <h2 id="ac-app-title">Download the School App<span class="mv-dot" aria-hidden="true">.</span></h2>
        <p>AfterCare enrollment and weekly sign up are both done in the Covenant Christian School app. Download it to sign up each Friday by 2:30 p.m.</p>
        <div class="ac-stores">
          <a class="ac-store" href="{IOS}"{NEW_TAB}>{APPLE}<span><small>Download on the</small>App Store</span></a>
          <a class="ac-store" href="{AND}"{NEW_TAB}>{PLAY}<span><small>Get it on</small>Google Play</span></a>
        </div>
      </div>
      <div class="ac-phones" data-reveal="left">
        <img class="ac-ph ac-ph-back" src="{IMG}app-splash.jpg" alt="" loading="lazy">
        <img class="ac-ph ac-ph-front" src="{IMG}app-home.jpg" alt="The Covenant Christian School app home screen with Calendar, Financials, Gradebook and Resources" loading="lazy">
      </div>
    </div>
  </section>
'''
