"""Preview-only redesign of /ftp (Family Teacher Partnership). All wording from the live page."""

FB = "https://www.facebook.com/covenantchristianschoolmobile"

def ftp(ICON, IMG, NEW_TAB):
    I = ICON
    pillars = [("handshake", "Support and Empowerment", "Enhance your child’s education by actively supporting our school community."),
               ("heart", "Foster School Spirit", "Help build and celebrate Covenant pride and unity."),
               ("gift", "Enhance School Resources", "Contribute to purchasing vital resources and improving facilities with funds raised.")]
    steps = [("calendar", "Attend Meetings", "Join our fall and spring meetings to connect and contribute."),
             ("hand", "Volunteer", "Help with campus clean-ups, teacher appreciation, and more."),
             ("users", "Join a Committee", "Participate in committees like Hospitality, Fundraising, or Family Fun Day."),
             ("facebook", "Stay Connected", f'Follow updates via email and our <a href="{FB}"{NEW_TAB}>Facebook page</a>.')]
    return f'''
  <section class="gv tu-hero2 ftp-hero" data-scroll-dim aria-labelledby="ftp-title">
    <div class="tu-hero2-img" style="background-image: url('{IMG}fb/ccs-dads-big-deal.jpg')" aria-hidden="true"></div>
    <div class="gv-wrap tu-hero2-copy">
      <span class="gv-eyebrow">Covenant FTP</span>
      <h1 id="ftp-title">Family Teacher <span class="ftp-l2">Partnership</span></h1>
      <p class="gv-lead">At Covenant Christian School, we believe that a strong partnership between families and the school is crucial to creating a vibrant, supportive community for our students.</p>
      <div class="gv-actions">
        <a class="gv-btn gv-btn-gold" href="/contact">Get In Touch</a>
        <a class="gv-btn gv-btn-ghost" href="#involved">How Can You Get Involved?</a>
      </div>
    </div>
  </section>

  <section class="gv gv-section gv-white ftp-intro" aria-labelledby="ftp-intro-title">
    <div class="gv-wrap ftp-intro-grid">
      <div class="ftp-intro-text">
        <h2 id="ftp-intro-title" class="ftp-sr">About the Covenant FTP</h2>
        <p class="ns-statement" data-reveal>That’s why we are excited to introduce you to the Covenant FTP—a cornerstone of our school community dedicated to enhancing the experience of our students, teachers, and administrators.</p>
        <ul class="ftp-pillars">{"".join(f'<li data-reveal><span class="hm-col-icon">{I[ic]}</span><div><h3>{t}</h3><p>{d}</p></div></li>' for ic, t, d in pillars)}</ul>
      </div>
      <div class="ftp-collage" data-reveal="left">
        <div class="hm-frame ftp-c1"><svg class="hm-frame-line" aria-hidden="true" focusable="false"><rect x="1" y="1" rx="4" ry="4"/></svg><img src="{IMG}fb/ccs-woot-cart.jpg" alt="FTP volunteers sharing the Woot Cart of teacher treats" loading="lazy"></div>
        <img class="ftp-c2" src="{IMG}fb/ccs-woot-cart-2.jpg" alt="Two FTP moms with the Woot Cart sign outside a classroom" loading="lazy">
      </div>
    </div>
  </section>

  <section class="gv gv-section ftp-involved" id="involved" aria-labelledby="ftp-inv-title">
    <div class="gv-wrap">
      <div class="ftp-inv-top">
        <div class="ftp-inv-head" data-reveal>
          <span class="gv-eyebrow">Every Family Belongs</span>
          <h2 id="ftp-inv-title">How Can You Get Involved?</h2>
          <p>All registered families are automatically members of the FTP. To make the most of your membership, we encourage active participation throughout the year. Here’s how you can contribute:</p>
        </div>
        <figure class="ftp-inv-photo" data-reveal="left"><img src="{IMG}fb/ccs-dads-ftp-sign.jpg" alt="Dads of Covenant holding a sign inviting families to the first FTP meeting" loading="lazy"></figure>
      </div>
      <ol class="ftp-steps">{"".join(f'<li data-reveal><span class="ftp-step-n" aria-hidden="true">0{n}</span><span class="hm-col-icon">{I[ic]}</span><h3>{t}</h3><p>{d}</p></li>' for n, (ic, t, d) in enumerate(steps, 1))}</ol>
    </div>
  </section>

  <section class="gv gv-section gv-paper ftp-cta" aria-labelledby="ftp-band-title">
    <div class="gv-wrap ftp-cta-grid">
      <div class="hm-frame ftp-cta-photo" data-reveal="right"><svg class="hm-frame-line" aria-hidden="true" focusable="false"><rect x="1" y="1" rx="4" ry="4"/></svg><img src="{IMG}fb/ccs-dad-high-five.jpg" alt="A Covenant dad giving a student a high five at morning drop-off" loading="lazy"></div>
      <div class="ftp-cta-text" data-reveal>
        <span class="gv-eyebrow">Better Together</span>
        <h2 id="ftp-band-title">Your involvement makes a direct impact—get engaged and see the difference you can make!</h2>
        <div class="gv-actions"><a class="gv-btn gv-btn-gold" href="/contact">Get In Touch</a></div>
      </div>
    </div>
  </section>
'''
