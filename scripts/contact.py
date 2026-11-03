"""Preview-only redesign of /contact. FAQ wording is word-for-word from the live page;
links are added on words already in the answers, plus a clear next-step button where one helps."""
import re
from pathlib import Path

APP = "https://aware3.net/shortcode/?code=covenantchristianschool-f"
INFO = "https://ccs-al.client.renweb.com/oa/inquiry.cfm?memberid=3143"
TEL = '<a href="tel:251-633-8055">251-633-8055</a>'
MAIL = '<a href="mailto:info@covenantschool.com">info@covenantschool.com</a>'

def map_src(pages):
    t = (pages / "contact.html").read_text()
    return re.search(r'src="(https://www\.google\.com/maps/embed[^"]*)"', t).group(1)

def contact(ICON, IMG, NEW_TAB, MAPS, pages):
    def btn(href, label, ext=False, cls="gv-btn-line"):
        return f'<a class="gv-btn {cls}" href="{href}"{NEW_TAB if ext else ""}>{label}</a>'
    FAQ = [
        ("grades", "What grade levels does CCS serve?",
         "<p>We serve students from K3 (pre-school) through 8th grade (junior high school).</p>",
         [btn("/new-student-application", "New Student Application"), btn("/tuition", "Tuition &amp; Fees")]),
        ("accredited", "Is CCS accredited?",
         "<p>We have met the requirements of the Accreditation Commission of the American Association of Christian Schools (AACS), and the requirements for membership in the American Association of Christian Schools. As members of AACS, our school is recognized as an educational partner by the State of Alabama Department of Education, the US Department of Education, and other private and Christian Schools.</p>",
         [btn("https://www.aacs.org/", "Visit AACS", True)]),
        ("open-house", "Do you have an annual Open House?",
         f"<p>Yes! Our Open House for the upcoming school year will be held in January each year from 4:30-6:30 p.m. Call the school office at {TEL} for more details or to schedule a personal tour. Join us for a campus tour, introduction to your child’s prospective teacher, and discover what makes CCS a great school!</p>",
         [btn("/schedule-tour", "Schedule a Tour", cls="gv-btn-gold"), btn("tel:251-633-8055", "Call 251-633-8055")]),
        ("hours", "What are the hours of operation?",
         """<dl class="ct-hours">
           <div><dt>K3 &amp; K4</dt><dd>We offer a three-day or five-day program that runs Monday-Friday from 8:00-12:00 (half day) or 8:00-3:00. AfterCare is available until 3:00 or 5:30.</dd></div>
           <div><dt>K5</dt><dd>Our five-day, half-day program runs Monday-Friday from 8:00-12:00 (half day) or 8:00-3:00. AfterCare is available until 3:00 or 5:30.</dd></div>
           <div><dt>1st-5th</dt><dd>Classes run Monday-Friday from 8:00-3:00.</dd></div>
           <div><dt>6th-8th</dt><dd>Classes run Monday-Friday from 8:00-3:10.</dd></div>
         </dl>
         <p><a href="/aftercare">AfterCare</a> is available for full day students as soon as school dismisses until 5:30. Please contact our office for a rate schedule.</p>
         <p>Early room is a supervised area that begins at 7:30 each school day morning and runs until 7:50. You may drop off your student during that time and he or she will be released to go to their respective classroom at 7:50.</p>""",
         [btn("/aftercare", "AfterCare Program"), btn("tel:251-633-8055", "Call for AfterCare rates")]),
        ("class-sizes", "What are the class sizes?",
         """<p>We believe smaller class sizes benefit students. Our class size goals are:</p>
         <ul class="ct-sizes"><li><b>11</b><span>K3 – 11 students</span></li><li><b>12</b><span>K4 – 12 students</span></li><li><b>20</b><span>K5 &amp; 1st – 20 students per class</span></li><li><b>20-22</b><span>2nd-8th grades – 20-22 students per class</span></li></ul>""",
         []),
        ("classes", "What other classes do student attend during the week?",
         "<p>All of our elementary students (except K3) attend physical education, daily Bible, weekly Chapel, art, and music classes. Students in Grades 1–5 also have scheduled Science Labs to supplement regular classroom lessons. Middle school students attend Bible, Chapel, and PE, and may choose from a variety of elective classes, including art.</p><p>*Private instrument lessons are also available on campus.</p>",
         [btn("/curriculum", "Curriculum"), btn("/athletics", "Athletics")]),
        ("registration", "When does registration begin?",
         "<p>Each year, we have an Open House in January to begin our fall registration process. Prospective parents and students are invited to visit our campus and classrooms and meet our teachers. Registration will be open to the public at the end of January / beginning of February and continues until classes are full.</p>",
         [btn("/new-student-application", "New Student Application", cls="gv-btn-gold"), btn("/tuition", "Tuition &amp; Fees")]),
        ("grades-online", "Do you offer online access to student grades?",
         """<p>We partner with FACTS Management to help streamline school operations for our families. In addition, the Covenant Christian School app gives all registered parents convenient access to:</p>
         <ul class="ct-ticks"><li>Student grades</li><li>Real-time announcements</li><li>School calendars</li><li>And much more</li></ul>
         <p>Recent features now make it even easier to manage school life, including the ability to:</p>
         <ul class="ct-ticks"><li>Pay tuition online</li><li>Order student lunches</li><li>Pay for field trips</li></ul>
         <p>To get started, simply download the Covenant Christian School app from your device’s app store.</p>""",
         [btn(APP, "Download the App Now", True, "gv-btn-gold")]),
        ("denomination", "What denomination is CCS affiliated with?",
         f'<p>Covenant Christian School is affiliated with <a href="https://covenantmobile.com/"{NEW_TAB}>Covenant Church of Mobile</a>, a non-denominational church. Our teachings are based on Biblical standards. We have students &amp; families from many different churches in Mobile and surrounding areas. Many are members of Baptist, Methodist, Catholic, and other non-denominational churches in the area.</p>',
         [btn("https://covenantmobile.com/", "Visit Covenant Church", True), btn("/mission-values", "Mission &amp; Values")]),
        ("curriculum", "What curriculum is used in the classroom?",
         '<p>Our curriculum has been carefully chosen to meet and exceed State of Alabama standards. For details about our curriculum, visit our <a href="/curriculum">Curriculum</a> page.</p>',
         [btn("/curriculum", "View Curriculum")]),
        ("lunch", "Do you serve lunch?",
         f'<p>We have a cafeteria that is open daily for students in K5-8th grades to purchase snacks and lunches. Parents order through the lunch module on the school’s <a href="{APP}"{NEW_TAB}>custom app</a>.</p>',
         [btn(APP, "Download the App", True)]),
    ]
    faqs = "".join(f'''<details class="tu-acc ct-faq" id="faq-{i}"><summary><span class="ct-q">{q}</span><span class="tu-acc-x" aria-hidden="true"></span></summary><div class="tu-acc-body ct-a">{a}{('<div class="ct-cta">' + "".join(c) + '</div>') if c else ""}</div></details>''' for i, q, a, c in FAQ)
    tiles = [
        ("phone", "Phone", "251-633-8055", "tel:251-633-8055", "Call us"),
        ("clock", "Hours", "Mon - Fri | 7:30am - 3:30pm", None, None),
        ("pin", "Address", "7150 Hitt Rd. Mobile, AL 36695", MAPS, "Directions"),
        ("mail", "Front Office", "info@covenantschool.com", "mailto:info@covenantschool.com", "Email"),
        ("users", "Principal, Felicia Boren", "fboren@covenantschool.com", "mailto:fboren@covenantschool.com", "Email"),
    ]
    tile_html = "".join(
        (f'<a class="ct-tile" href="{h}"{NEW_TAB if h == MAPS else ""}>' if h else '<div class="ct-tile">') +
        f'<span class="hm-col-icon">{ICON[ic]}</span><span class="ct-k">{k}</span><span class="ct-v">{v}</span>' +
        (f'<span class="ct-go">{go} <span aria-hidden="true">&rarr;</span></span></a>' if h else '</div>')
        for ic, k, v, h, go in tiles)
    return f'''
  <section class="gv gv-hero gv-hero-split ep-hero st-hero ct-hero">
    <img class="ep-hero-eagle" src="{IMG}eagle-mark-white.png" alt="" width="900" height="321">
    <div class="gv-hero-photo" style="background-image: url('{IMG}covenant-86-9595976.jpg')" aria-hidden="true"></div>
    <div class="gv-wrap">
      <div class="gv-hero-copy">
        <span class="gv-eyebrow">7150 Hitt Rd. Mobile, AL 36695</span>
        <h1>Get in Touch</h1>
        <p class="gv-lead"><strong>Have a question? We have the answers.</strong> Give us a call – we're here to help you discover why Covenant Christian School is the perfect choice for your educational journey!</p>
        <div class="gv-actions">
          <a class="gv-btn gv-btn-gold" href="tel:251-633-8055">{ICON["phone"]}Call 251-633-8055</a>
          <a class="gv-btn gv-btn-ghost" href="/schedule-tour">Schedule a Tour</a>
        </div>
      </div>
    </div>
  </section>

  <section class="gv gv-section gv-white ct-info" aria-label="Contact information">
    <div class="gv-wrap">
      <div class="ct-tiles" data-reveal>{tile_html}</div>
      <div class="ct-map" data-reveal>
        <iframe src="{map_src(pages)}" title="Map: Covenant Christian School, 7150 Hitt Rd, Mobile, AL" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
        <div class="ct-map-card">
          <h2>Visit us<span class="mv-dot" aria-hidden="true">.</span></h2>
          <p>7150 Hitt Rd.<br>Mobile, AL 36695</p>
          <div class="ct-map-actions">
            <a class="gv-btn gv-btn-line" href="{MAPS}"{NEW_TAB}>{ICON["pin"]}Directions</a>
          </div>
          <div class="gv-social ct-social">
            <a href="https://www.facebook.com/covenantchristianschoolmobile"{NEW_TAB} aria-label="Covenant Christian School on Facebook">{ICON["facebook"]}</a>
            <a href="https://www.instagram.com/ccs_eagles_of_al/"{NEW_TAB} aria-label="Covenant Christian School on Instagram">{ICON["instagram"]}</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="gv gv-section gv-paper" id="faq" aria-labelledby="ct-faq-title">
    <div class="gv-wrap ct-faq-grid">
      <div class="ct-faq-head" data-reveal>
        <span class="gv-eyebrow">Problems Solved</span>
        <h2 id="ct-faq-title">Your Frequently Asked Questions Answered<span class="mv-dot" aria-hidden="true">.</span></h2>
        <p>Can't find the answer you're looking for here? Call us at {TEL} or email {MAIL} and we'll be in touch with you shortly.</p>
        <a class="gv-btn gv-btn-line" href="{INFO}"{NEW_TAB}>Request More Information</a>
      </div>
      <div class="tu-accs ct-accs" data-reveal>{faqs}</div>
    </div>
  </section>

  <section class="gv gv-band gv-band-parallax" aria-labelledby="ct-tour-title">
    <div class="gv-band-bg" style="background-image: url('{IMG}covenant-151_1-9523341.jpg')" aria-hidden="true"></div>
    <div class="gv-wrap" data-reveal>
      <h2 id="ct-tour-title">TOUR OUR CAMPUS</h2>
      <p class="gv-band-sub">Your child's exceptional education experience awaits.</p>
      <div class="gv-actions"><a class="gv-btn gv-btn-gold" href="/schedule-tour">SCHEDULE A TOUR</a></div>
    </div>
  </section>
'''
