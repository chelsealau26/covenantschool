"""Preview-only redesign of /technology. All wording is word-for-word from the live page."""
from mission_values import EXTRA_ICONS

def technology(ICON, IMG):
    I = dict(ICON); I.update(EXTRA_ICONS)
    I["nodevice"] = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="5" y="2" width="14" height="20" rx="2"/><path d="M11 18h2"/><path d="M3 3l18 18"/></svg>'
    I["wallet"] = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 7V5a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-4a2 2 0 0 0 0 4h4v2a1 1 0 0 1-1 1H5a2 2 0 0 1-2-2V6"/></svg>'
    def checks(items):
        return '<ul class="te-checks">' + "".join(f'<li><span class="te-tick" aria-hidden="true">{I["check"]}</span><span>{x}</span></li>' for x in items) + "</ul>"
    skills = ["Microsoft Office (Word, Excel, PowerPoint)", "Google Classroom", "Typing and keyboarding", "Design and presentation tools like Canva"]
    finds = ["Students retain information better when learning is not screen-based",
             "Screens can reduce focus, engagement, and critical thinking",
             "Personal devices often create unnecessary distractions in the classroom"]
    return f'''
  <section class="gv tu-hero2 te-hero" data-scroll-dim aria-labelledby="te-title">
    <div class="tu-hero2-img" style="background-image: url('{IMG}covenant-10-9527833.jpg')" aria-hidden="true"></div>
    <div class="te-hero-grid" aria-hidden="true"></div>
    <div class="gv-wrap tu-hero2-copy">
      <span class="gv-eyebrow">Technology</span>
      <h1 id="te-title">Technology <span class="te-l2">With Purpose<span class="te-caret" aria-hidden="true"></span></span></h1>
      <p class="gv-lead">Using technology wisely to support learning, without losing focus on what matters most.</p>
      <div class="gv-actions"><a class="gv-btn gv-btn-gold" href="#approach">Learn About Our Approach</a></div>
    </div>
  </section>

  <section class="gv gv-section gv-white te-commit" aria-labelledby="te-commit-title">
    <div class="gv-wrap te-commit-grid">
      <div data-reveal>
        <h2 id="te-commit-title">Our Commitment to Learning<span class="mv-dot" aria-hidden="true">.</span></h2>
        <p class="te-big">At Covenant Christian School, our goal is simple: help students learn deeply, think clearly, and grow confidently, academically and spiritually.</p>
      </div>
      <p class="ns-statement" data-reveal="left">Technology is one of many tools we use, but it is never the focus. Our approach is thoughtful, research-informed, and rooted in what helps students learn best.</p>
    </div>
  </section>

  <section class="gv gv-section te-challenge te-grid" aria-labelledby="te-challenge-title">
    <div class="gv-wrap te-challenge-grid">
      <figure class="te-window" data-reveal="right"><div class="te-window-bar" aria-hidden="true"><i></i><i></i><i></i><span>covenantschool.com/learning</span></div><img src="{IMG}covenant-78-9798253.jpg" alt="A student taking handwritten notes with a school iPad beside her" loading="lazy"></figure>
      <div data-reveal>
        <h2 id="te-challenge-title">The Challenge We’ve Seen</h2>
        <p class="te-challenge-intro">Over time, teachers and administrators observed that too much screen use can interfere with learning. Research and classroom experience show that:</p>
        <ol class="te-finds">{"".join(f'<li><span class="te-num" aria-hidden="true">0{i}</span><h3>{x}</h3></li>' for i, x in enumerate(finds, 1))}</ol>
        <p class="te-seen"><span class="hm-col-icon">{I["check"]}</span><span>We’ve also seen fewer behavioral issues and stronger focus in classrooms where personal devices are not used.</span></p>
      </div>
    </div>
  </section>

  <section class="gv gv-section gv-paper te-approach" id="approach" aria-labelledby="te-approach-title">
    <div class="gv-wrap">
      <div class="te-solution" data-reveal>
        <span class="gv-eyebrow">Our Solution</span>
        <h2 id="te-approach-title">A More Intentional Approach</h2>
        <p>To better support student learning, Covenant is shifting to a school-managed, purpose-driven technology model—one that reduces distractions and strengthens academic skills.</p>
      </div>
      <div class="tu-head te-use-head" data-reveal>
        <h2 id="te-use-title">Technology Use At Covenant<span class="mv-dot" aria-hidden="true">.</span></h2>
        <p>Intentional, school-guided technology with focused learning and fewer distractions.</p>
      </div>
      <div class="te-plans">
        <article class="te-plan" data-reveal aria-labelledby="te-ms">
          <svg class="hm-frame-line" aria-hidden="true" focusable="false"><rect x="1" y="1" rx="4" ry="4"/></svg>
          <div class="te-plan-in">
            <span class="te-grades">Grades 6-8</span>
            <h3 id="te-ms">Middle School Technology</h3>
            <p class="te-plan-lead">Beginning August 2026, middle school students will use technology in a dedicated computer lab setting.</p>
            {checks(["Students will use school-owned Chromebooks", "Devices are used only during scheduled computer classes", "Instruction focuses on essential academic skills, including:"])}
            <ul class="te-skills">{"".join(f"<li>{s}</li>" for s in skills)}</ul>
            <img class="te-plan-img te-plan-img-ms" src="{IMG}covenant-118-9528193.jpg" alt="Middle school students working together on school devices" loading="lazy">
            <p class="te-plan-note">This model better prepares students for high school expectations while keeping classroom learning focused and effective.</p>
          </div>
        </article>
        <article class="te-plan" data-reveal aria-labelledby="te-el">
          <svg class="hm-frame-line" aria-hidden="true" focusable="false"><rect x="1" y="1" rx="4" ry="4"/></svg>
          <div class="te-plan-in">
            <span class="te-grades">Kindergarten - Grade 5</span>
            <h3 id="te-el">Elementary Technology Use</h3>
            <p class="te-plan-lead">Younger students will continue to use school-owned iPads occasionally and intentionally.</p>
            {checks(["Technology is used in small, purposeful ways", "Screen time is balanced with hands-on learning, discussion, and written work", "iPads support instruction—not replace traditional learning tools"])}
            <img class="te-plan-img" src="{IMG}covenant-47-9584556.jpg" alt="A teacher working one-on-one with an elementary student on a school iPad" loading="lazy">
          </div>
        </article>
      </div>
    </div>
  </section>

  <section class="gv gv-section te-policy te-grid" aria-labelledby="te-policy-title">
    <div class="gv-wrap">
      <div class="te-policy-head" data-reveal>
        <h2 id="te-policy-title">Personal Device Policy</h2>
        <p>To create consistency and reduce distractions:</p>
      </div>
      <ul class="te-policy-list" data-reveal>
        <li><span class="hm-col-icon">{I["nodevice"]}</span><span>Students are no longer allowed to bring personal iPads or devices to campus</span></li>
        <li><span class="hm-col-icon">{I["school"]}</span><span>All technology used during the school day is provided and managed by the school</span></li>
        <li><span class="hm-col-icon">{I["wallet"]}</span><span>No device purchases are required by families</span></li>
      </ul>
    </div>
  </section>

  <section class="gv gv-band gv-band-parallax te-why" data-focus=".2" aria-labelledby="te-why-title">
    <div class="gv-band-bg" style="background-image: url('{IMG}covenant-121-9598740.jpg')" aria-hidden="true"></div>
    <div class="gv-wrap" data-reveal>
      <h2 id="te-why-title">Why This Matters</h2>
      <p class="gv-band-sub">At Covenant Christian School, we believe technology should support learning and honor the way God designed our children to grow and learn. By guiding how and when technology is used, we help students stay focused, build strong foundations, and develop wise, responsible habits that will serve them well in the future.</p>
      <p class="gv-band-sub">We value our partnership with families and remain committed to doing what is best for our students—academically, spiritually, and developmentally.</p>
      <div class="gv-actions"><a class="gv-btn gv-btn-gold" href="/schedule-tour">SCHEDULE A TOUR</a></div>
    </div>
  </section>
'''
