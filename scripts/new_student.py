"""Preview-only redesign of /new-student-application. All wording from the live page."""

APPLY = "https://sis.factsmgt.com/admissions-parent/home?districtCode=ccs-al&memberId=3143"
INFO = "https://ccs-al.client.renweb.com/oa/inquiry.cfm?memberid=3143"
CREATE = "https://ccs-al.client.renweb.com/oa/register.cfm?memberid=3143"

def new_student(ICON, IMG, NEW_TAB):
    kinder = "".join(f'''<li data-reveal><span class="ns-grade">{g}</span><p>Students must be <strong>{n} years old</strong> before September 1{extra}</p></li>'''
                     for g, n, extra in [("K3", 3, " and must be fully toilet trained"), ("K4", 4, ""), ("K5", 5, "")])
    return f'''
  <section class="gv gv-hero gv-hero-split ep-hero st-hero ns-hero">
    <img class="ep-hero-eagle" src="{IMG}eagle-mark-white.png" alt="" width="900" height="321">
    <div class="gv-hero-photo" style="background-image: url('{IMG}covenant-114-9584701.jpg')" aria-hidden="true"></div>
    <div class="gv-wrap">
      <div class="gv-hero-copy">
        <span class="gv-eyebrow">Admissions</span>
        <h1>Welcome New Students!</h1>
        <p class="gv-lead">Explore how easy it is to become a part of Covenant Christian School and start your journey toward academic success and personal growth.</p>
        <div class="gv-actions">
          <a class="gv-btn gv-btn-gold" href="{APPLY}"{NEW_TAB}>{ICON["pen"]}Apply Now</a>
          <a class="gv-btn gv-btn-ghost" href="{INFO}"{NEW_TAB}>Request More Information</a>
        </div>
      </div>
    </div>
  </section>

  <section class="gv gv-section gv-white ns-intro" aria-labelledby="ns-intro-title">
    <div class="gv-wrap ns-intro-grid">
      <div data-reveal>
        <span class="gv-eyebrow">Academic Excellence &amp; Personal Growth</span>
        <h2 id="ns-intro-title">Experience the Covenant Difference<span class="mv-dot" aria-hidden="true">.</span></h2>
      </div>
      <p class="mv-body" data-reveal>Welcome to Covenant Christian School, and thank you for considering us for your student's education. Our goal is to provide exceptional educational services tailored to your child's needs. The application process is convenient and entirely online through our parent portal. Follow the simple steps below to complete your application today. For any questions about enrollment, please don't hesitate to reach out to our office at <a class="ns-tel" href="tel:251-633-8055">251-633-8055</a>. We look forward to welcoming you into our school family!</p>
    </div>
  </section>

  <section class="gv gv-section gv-paper" id="how-to-apply" aria-labelledby="ns-how-title">
    <div class="gv-wrap">
      <div class="ep-roles-head" data-reveal>
        <h2 id="ns-how-title">How to Apply<span class="mv-dot" aria-hidden="true">.</span></h2>
        <ul class="ns-facts" aria-label="Good to know">
          <li>{ICON["calendar"]}Applications begin in January</li>
          <li>{ICON["receipt"]}$22.00 non-refundable fee per application</li>
        </ul>
      </div>
      <ol class="ns-steps">
        <li class="ns-step" data-reveal>
          <span class="ns-step-n">01</span>
          <h3>Apply for New Student(s)</h3>
          <p>Our application process begins in January. Applying is easy using our Online Application. Families are now required to apply online as it simplifies submission and provides parents a tool for tracking online the status of their admission after their application has been submitted. A non-refundable fee of $22.00 must be submitted with each application.</p>
          <a class="gv-btn gv-btn-line" href="{APPLY}"{NEW_TAB}>Apply Now</a>
        </li>
        <li class="ns-step" data-reveal>
          <span class="ns-step-n">02</span>
          <h3>Create an Online Application</h3>
          <p>To begin the Online Application process, Create an Account. Then log in to your account and Create A New Student Application for your child. You will then have the flexibility to log in and out of your account and access your open application.</p>
          <p>After submitting the application, you will be able to track online your admissions status at the school by logging in to your account. There you will be able to print the completed applications, monitor when the school receives supplemental application forms and, if necessary, reprint the supplemental forms.</p>
          <a class="gv-btn gv-btn-line" href="{CREATE}"{NEW_TAB}>Create Application</a>
        </li>
        <li class="ns-step" data-reveal>
          <span class="ns-step-n">03</span>
          <h3>Need Some More Information?</h3>
          <p>If you need more information about the admissions process, want to schedule a tour, or have any questions, please contact our admissions office. We'll be happy to assist you and look forward to connecting with you soon!</p>
          <a class="gv-btn gv-btn-line" href="{INFO}"{NEW_TAB}>Request Information</a>
        </li>
      </ol>
    </div>
  </section>

  <section class="gv gv-section gv-dark ns-kinder" aria-labelledby="ns-kinder-title">
    <img class="mv-faith-eagle" src="{IMG}eagle-mark-white.png" alt="" width="900" height="321">
    <div class="gv-wrap">
      <div class="ns-kinder-head" data-reveal>
        <span class="gv-eyebrow">All you need to know</span>
        <h2 id="ns-kinder-title">Kinder Requirements<span class="mv-dot" aria-hidden="true">.</span></h2>
        <p>Explore a few things about our kindergarten requirements to ensure a smooth application process and a successful start for your child.</p>
      </div>
      <ul class="ns-kinder-grid">{kinder}</ul>
    </div>
  </section>

  <section class="gv gv-band gv-band-parallax" aria-labelledby="ns-tour-title">
    <div class="gv-band-bg" style="background-image: url('{IMG}covenant-151_1-9523341.jpg')" aria-hidden="true"></div>
    <div class="gv-wrap" data-reveal>
      <h2 id="ns-tour-title">TOUR OUR CAMPUS</h2>
      <p class="gv-band-sub">Your child's exceptional education experience awaits.</p>
      <div class="gv-actions"><a class="gv-btn gv-btn-gold" href="/schedule-tour">SCHEDULE A TOUR</a></div>
    </div>
  </section>

  <section class="gv gv-section gv-white ns-legal" aria-label="Nondiscrimination policy">
    <div class="gv-wrap"><p>Covenant Christian School does not discriminate on the basis of race, color, national and ethnic origin in administration of its educational policies, admissions policies, scholarship and loan programs, and athletic and other school-administered programs.</p></div>
  </section>
'''
