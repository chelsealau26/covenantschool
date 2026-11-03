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
    D = {
        "Preschool Teacher (K3/K4)": ("Guide our youngest learners through joyful, hands-on days.", ["Three-day or five-day programs", "Half day (8:00-12:00) or full day (8:00-3:00)", "Class size goals: K3 – 11, K4 – 12"]),
        "Kindergarten Teacher (K5)": ("Build the foundations of reading, math and faith.", ["Five-day program, half or full day", "Class size goal: 20 students", "Daily Bible and weekly Chapel"]),
        "Elementary Teacher (1st–5th)": ("Lead a classroom where every lesson fits God's big picture.", ["Classes 8:00-3:00, Monday-Friday", "Class size goals: 20-22 students", "Scheduled Science Labs supplement lessons"]),
        "Middle School Teacher (6th–8th)": ("Prepare junior high students to understand, communicate with and influence their world.", ["Classes 8:00-3:10, Monday-Friday", "Students bring their own iPads", "Electives, Bible, Chapel and PE"]),
        "Specials Teacher": ("Teach the classes students look forward to all week.", ["Physical education, art and music", "Bible and weekly Chapel", "Serve elementary and middle school"]),
        "Substitute Teacher": ("Step in wherever you're needed, from K3 to 8th grade.", ["Flexible, as-needed days", "Supportive teachers and staff", "A loving Christian environment"]),
        "Aftercare Staff": ("Give students a safe, engaging place after school.", ["After dismissal until 5:30", "Monday-Friday during the school year", "Work alongside our school family"]),
        "Coach": ("Help students learn new skills and serve within a Christ-centered community.", ["Cross-country, volleyball, cheerleading", "Basketball, soccer and track", "YDL athletics from 3rd grade (1st for soccer)"]),
        "Office / Administrative Staff": ("Be the welcoming heart of the front office.", ["Office hours Mon - Fri, 7:30am - 3:30pm", "Support families, teachers and students", "Organized, friendly and detail-minded"]),
        "Other": ("Don't see your role? We'd still love to hear how you'd like to serve.", ["Tell us about your gifts and experience", "We'll be in touch with you shortly"]),
    }
    def det(p):
        lead, items = D.get(p, ("", []))
        return f'<p>{lead}</p><ul>' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"
    chips = "".join(
        f'<li><details class="ep-role"><summary><span class="ep-role-n" aria-hidden="true">{i:02d}</span><span class="ep-role-t">{H.escape(p)}</span>'
        f'<span class="ep-role-go" aria-hidden="true"></span></summary><div class="ep-role-body">{det(p)}'
        f'<button type="button" class="gv-btn gv-btn-gold ep-role-apply" data-pick-position="{H.escape(p, quote=True)}">Apply Now</button></div></details></li>'
        for i, p in enumerate(positions(block), 1))
    return f'''
  <section class="gv ns-hero ep-hero3" data-scroll-dim aria-labelledby="ep-title">
    <div class="ns-hero-img" style="background-image: url('{IMG}covenant-47-9584556.jpg')" aria-hidden="true"></div>
    <div class="gv-wrap ns-hero-copy">
      <span class="gv-eyebrow">Join our team</span>
      <h1 id="ep-title">Employment Opportunities</h1>
      <p class="gv-lead">Discover the career opportunities and joy-filled days awaiting you at Covenant Christian School.</p>
      <div class="ns-hero-bottom"><div class="gv-actions"><a class="gv-btn gv-btn-gold" href="#apply">Apply Below</a></div></div>
    </div>
  </section>

  <section class="gv gv-section gv-white ep-roles" aria-labelledby="ep-roles-title">
    <div class="gv-wrap">
      <div class="ep-roles-head" data-reveal>
        <h2 id="ep-roles-title">Positions you can apply for<span class="mv-dot" aria-hidden="true">.</span></h2>
        <p>Open a position to learn more, then apply in one step.</p>
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
        <div class="hm-frame ep-frame"><svg class="hm-frame-line" aria-hidden="true" focusable="false"><rect x="1" y="1" rx="4" ry="4"/></svg><img src="{IMG}fb/ccs-teachers.jpg" alt="Three smiling Covenant teachers" loading="lazy"></div>
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
