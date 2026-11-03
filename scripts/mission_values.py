"""Preview-only redesign of /mission-values. All wording is the client's, unchanged."""

EXTRA_ICONS = {
    "layers": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m12 2 10 5-10 5L2 7Z"/><path d="m2 17 10 5 10-5"/><path d="m2 12 10 5 10-5"/></svg>',
    "teacher": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="8" cy="7" r="3"/><path d="M2 21v-2a5 5 0 0 1 5-5h2"/><rect x="12" y="4" width="10" height="8" rx="1"/><path d="m14 17 3-5 3 5"/></svg>',
    "chat": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2Z"/></svg>',
    "mountain": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m8 3 4 8 5-5 5 15H2Z"/></svg>',
    "book": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 4h6a4 4 0 0 1 4 4v13a3 3 0 0 0-3-3H2Z"/><path d="M22 4h-6a4 4 0 0 0-4 4v13a3 3 0 0 1 3-3h7Z"/></svg>',
    "flask": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 2h6"/><path d="M10 2v7L4 20a1.5 1.5 0 0 0 1.3 2h13.4A1.5 1.5 0 0 0 20 20L14 9V2"/><path d="M7 15h10"/></svg>',
    "tablet": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="2" width="16" height="20" rx="2"/><path d="M11 18h2"/></svg>',
    "home": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m3 10 9-7 9 7v10a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1Z"/></svg>',
}

HISTORY = [
    ("1983", "Covenant School was founded in 1983 by a group of parents who believed Christian education was fundamental to Christian discipleship."),
    ("1988", "1988 marked a milestone in our history with the graduation of our first 8th grade class."),
    ("1992", "During the summer of 1992, the word “Christian” was added to the school name to clarify our identity publicly."),
    ("2000", "By the year 2000, school enrollment reached over 200 and a strong K-8 program had been established."),
    ("2017–18", "During the 2017-2018 school year, CCS sought and was awarded accreditation."),
]

WHY = [
    ("layers", "Strong Foundations", "We carry traditional foundations of learning and teaching along with innovative ideas and creativity."),
    ("teacher", "Qualified Teachers", "CCS teachers lead our students to see how the lesson at hand fits into God’s big picture and His purpose for their lives."),
    ("chat", "Open Communication", "We have an open door of communication between parents and teachers concerning the child’s best interests as well as easy online access to grades and important information."),
    ("mountain", "Helpful Challenges", "We strive to challenge students in a safe environment where there is respect for his/her individual dignity. We want them to think beyond just memorizing facts in order to develop problem-solving skills for the future."),
    ("book", "Quality Curriculum", "CCS curriculum is chosen specifically and carefully to provide a well-balanced, solid foundation in all core subjects, best suitable for each class. We utilize computers, interactive technology, and online resources to prepare our students to be on the cutting edge of influence and productivity."),
    ("flask", "Science Labs", "We take hands-on science seriously at CCS. Regularly scheduled science labs supplement classroom teaching for grades 1-5. Our Junior High students have access to a full lab where they perform dissections, blood-typing, chemistry labs, physics and engineering projects and much more!"),
    ("trophy", "Sports &amp; Activities", "CCS offers a variety of extracurricular activities. Students work closely with staff, coaches, and parents to learn new skills and to serve within a Christ-centered community. Our athletic department fields teams for cross-country, volleyball, cheerleading, basketball, soccer, and track. YDL athletics creates opportunities for participation starting in 3rd grade (1st grade for soccer!) Our Scholar’s Bowl team excels in regional competitions."),
    ("tablet", "Technology", "CCS leverages technology to engage this generation of “digital natives”. In addition to Smartboards, Mimeos, overhead projectors and document cameras, CCS has been using iPads to enhance student learning in grades 1-8 with instant response class review games, IXL differentiated learning in math and language, opportunities to create multimedia projects, and much more. Junior High students bring their own iPads to school, use digital planners and have access to virtual classrooms which greatly aided our transition to remote learning during COVID. They have a full period of Computer Connections daily which includes instruction in typing skills, digital citizenship, MS Word, Excel, and PowerPoint."),
]

def mission_values(ICON, IMG):
    I = dict(ICON); I.update(EXTRA_ICONS)
    dot = '<span class="mv-dot" aria-hidden="true">.</span>'
    timeline = "".join(f'<li data-reveal><span class="mv-year">{y}</span><p>{t}</p></li>' for y, t in HISTORY)
    why = "".join(f'''<li class="mv-why-item" data-reveal><span class="hm-col-icon">{I[i]}</span><div><h3>{t}</h3><p>{d}</p></div></li>''' for i, t, d in WHY)
    return f'''
  <section class="gv gv-hero mv-hero" style="--hero-img: url('{IMG}fb/ccs-school-gathering.jpg')">
    <div class="mv-hero-bg" style="background-image: url('{IMG}fb/ccs-school-gathering.jpg')" aria-hidden="true"></div>
    <div class="gv-wrap">
      <div class="gv-hero-copy">
        <span class="gv-eyebrow">Mission &amp; Values</span>
        <h1>About Us</h1>
        <div class="gv-actions">
          <a class="gv-btn gv-btn-gold" href="/schedule-tour">Schedule a Tour</a>
          <a class="gv-btn gv-btn-ghost" href="#why">Why CCS?</a>
        </div>
      </div>
    </div>
  </section>

  <nav class="gv gv-jump" aria-label="On this page">
    <div class="gv-wrap">
      <span class="gv-jump-label">On this page</span>
      <div class="gv-jump-links">
        <a href="#mission">Mission</a><a href="#history">History</a><a href="#family">Family</a><a href="#faith">Statement of Faith</a><a href="#why">Why CCS?</a>
      </div>
    </div>
  </nav>

  <section class="gv gv-section gv-white mv-intro" aria-label="About Covenant Christian School">
    <div class="gv-wrap" data-reveal>
      <p>Covenant Christian School operates as a vibrant ministry under Covenant Church of Mobile. With a shared commitment to faith-based education, Covenant Church provides essential support and spiritual guidance that enriches the educational experience at our school. Together, we cultivate an environment where academic excellence, personal growth, and spiritual development are paramount. This partnership fosters a community of learning and faith, empowering students to excel academically while nurturing their spiritual journey in a supportive and inclusive environment.</p>
    </div>
  </section>

  <section class="gv gv-section gv-paper" id="mission" aria-labelledby="mv-mission-title">
    <div class="gv-wrap mv-mission">
      <div data-reveal>
        <h2 id="mv-mission-title">Mission{dot}</h2>
        <p class="mv-big">Covenant Christian School exists to support families with Christ-centered education. Our mission is to graduate students who are prepared to understand their world, to communicate with their world, and to influence their world for Jesus Christ through servant-leadership. We have identified three core values: Christ-likeness, family-focused community, and high academic standards.</p>
      </div>
      <ul class="mv-values" aria-label="Our three core values">
        <li data-reveal><span class="hm-col-icon">{I["cross"]}</span>Christ-likeness</li>
        <li data-reveal><span class="hm-col-icon">{I["users"]}</span>Family-focused community</li>
        <li data-reveal><span class="hm-col-icon">{I["school"]}</span>High academic standards</li>
      </ul>
    </div>
  </section>

  <section class="gv gv-section gv-white" id="history" aria-labelledby="mv-history-title">
    <div class="gv-wrap mv-history">
      <div class="mv-history-text">
        <h2 id="mv-history-title" data-reveal>History{dot}</h2>
        <div class="mv-timeline"><div class="mv-track" aria-hidden="true"><span class="mv-progress"></span></div><ol>{timeline}
          <li class="mv-now" data-reveal><span class="mv-year"><span data-count="500" data-suffix="+">500+</span></span><p>So far, Covenant Christian School has educated and influenced over 500 graduating alumni. And our story continues!</p></li>
        </ol></div>
      </div>
      <figure class="mv-history-photo" data-reveal><svg class="hm-frame-line" aria-hidden="true" focusable="false"><rect x="1" y="1" rx="4" ry="4"/></svg><div class="mv-hp-img"><img src="{IMG}covenant-86-9595976.jpg" alt="The front entrance of Covenant Christian School" loading="lazy"></div><figcaption><span>Est.</span> 1983</figcaption></figure>
    </div>
  </section>

  <section class="gv gv-section gv-soft" id="family" aria-labelledby="mv-family-title">
    <div class="gv-wrap mv-family">
      <div class="hm-frame" data-reveal="left"><svg class="hm-frame-line" aria-hidden="true" focusable="false"><rect x="1" y="1" rx="4" ry="4"/></svg><img src="{IMG}fb/ccs-four-friends.jpg" alt="Four smiling young students hugging each other in chapel" loading="lazy"></div>
      <div data-reveal>
        <h2 id="mv-family-title">Family{dot}</h2>
        <p class="mv-body">Covenant Christian School’s statement of mission and values are an important part of communicating “who” we are; however, the essence of our school is best displayed in the life-long relationships, the kindness, and the loyalties of our employees, parents, and students, and the support and love demonstrated to our extended families. Through the years of educating and living life together, most CCS families find that they have truly become part of the bigger picture… part of something larger than themselves. We find ourselves caught up in the realization of belonging, which is at the core of who God made us to be.</p>
      </div>
    </div>
  </section>

  <section class="gv gv-section gv-dark mv-faith" id="faith" aria-labelledby="mv-faith-title">
    <div class="mv-faith-bg" style="background-image: url('{IMG}fb/ccs-girl-praying.jpg')" aria-hidden="true"></div>
    <img class="mv-faith-eagle" src="{IMG}eagle-mark-white.png" alt="" width="900" height="321">
    <div class="gv-wrap" data-reveal>
      <h2 id="mv-faith-title">Statement of Faith{dot}</h2>
      <p class="mv-creed">We believe in God, the Father almighty, creator of heaven and earth. We believe in Jesus Christ, God’s only Son, our Lord, who was conceived by the Holy Spirit, born of the Virgin Mary, suffered under Pontius Pilate, was crucified, died, and was buried; On the third day He rose from the dead; He ascended into heaven, and is seated at the right hand of God the Father almighty; from there He will come to judge the living and the dead. We believe in the Holy Spirit, the Christian Church, the communion of saints, the forgiveness of sins, the resurrection of the body, and life everlasting. <strong>Amen.</strong></p>
    </div>
  </section>

  <section class="gv gv-section gv-paper" id="why" aria-labelledby="mv-why-title">
    <div class="gv-wrap">
      <div class="gv-head" data-reveal>
        <h2 id="mv-why-title">WHY CCS?</h2>
        <p>At Covenant Christian School, we excel in academics, character development, and spiritual growth, fostering a supportive community where every student thrives.</p>
      </div>
      <div class="mv-strip" data-reveal>
        <figure><img src="{IMG}fb/ccs-science-lab.jpg" alt="Students smiling during a science lab dissection" loading="lazy"><figcaption>Science Labs</figcaption></figure>
        <figure><img src="{IMG}fb/ccs-volleyball-team.jpg" alt="The Covenant volleyball team holding flowers on the court" loading="lazy"><figcaption>Sports &amp; Activities</figcaption></figure>
        <figure><img src="{IMG}fb/ccs-green-screen.jpg" alt="Three students smiling in front of a green screen" loading="lazy"><figcaption>Technology</figcaption></figure>
        <figure><img src="{IMG}fb/ccs-library-kids.jpg" alt="Students showing their prizes in the school library" loading="lazy"><figcaption>Strong Foundations</figcaption></figure>
      </div>
      <ul class="mv-why">{why}</ul>
    </div>
  </section>

  <section class="gv gv-band gv-band-parallax" aria-labelledby="mv-tour-title">
    <div class="gv-band-bg" style="background-image: url('{IMG}covenant-151_1-9523341.jpg')" aria-hidden="true"></div>
    <div class="gv-wrap" data-reveal>
      <h2 id="mv-tour-title">TOUR OUR CAMPUS</h2>
      <p class="gv-band-sub">Your child's exceptional education experience awaits.</p>
      <div class="gv-actions"><a class="gv-btn gv-btn-gold" href="/schedule-tour">SCHEDULE A TOUR</a></div>
    </div>
  </section>
'''
