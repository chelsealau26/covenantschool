"""Preview-only redesign of /curriculum. Wording and curriculum lists are word-for-word from the live page."""
import re, html as H
from mission_values import EXTRA_ICONS

SUBJECTS = ["Spelling & Phonics", "Reading", "Language", "Math", "History", "Science"]

def read_grades(pages):
    t = (pages / "curriculum.html").read_text()
    m = t[t.index("<main"):t.index("</main>")]
    m = re.sub(r"<(script|style)[\s\S]*?</\1>", "", m)
    out, cur = {}, None
    for x in re.finditer(r"<(h3|p)\b[^>]*>([\s\S]*?)</\1>", m):
        txt = re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", x.group(2)))).replace("﻿", "").strip()
        if x.group(1) == "h3": cur = txt; out.setdefault(cur, {}); continue
        if cur and " : " in txt:
            k, v = txt.split(" : ", 1)
            out[cur].setdefault(k.strip(), v.strip())
    return out

def curriculum(ICON, IMG, pages):
    I = dict(ICON); I.update(EXTRA_ICONS)
    I["calc"] = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="2" width="16" height="20" rx="2"/><path d="M8 6h8"/><path d="M8 11h.01M12 11h.01M16 11h.01M8 15h.01M12 15h.01M16 15h.01M8 19h.01M12 19h4"/></svg>'
    SI = {"Spelling & Phonics": "pen", "Reading": "book", "Language": "chat", "Math": "calc", "History": "map", "Science": "flask"}
    G = read_grades(pages)
    groups = [("Early Learning", ["K3", "K4", "K5"]), ("Elementary", ["1st Grade", "2nd Grade", "3rd Grade", "4th Grade", "5th Grade"]), ("Junior High", ["6th Grade", "7th Grade", "8th Grade"])]
    def gid(g): return "cu-" + re.sub(r"[^a-z0-9]+", "-", g.lower()).strip("-")
    tabs = "".join(
        f'<div class="cu-group"><span class="cu-group-k">{name}</span><div class="cu-tabs" role="tablist" aria-label="{name}">' +
        "".join(f'<button type="button" role="tab" class="cu-tab" id="{gid(g)}-tab" aria-controls="{gid(g)}" aria-selected="{"true" if g == "K3" else "false"}">{g.replace(" Grade", "")}<span class="cu-tab-sub">{"Grade" if "Grade" in g else ""}</span></button>' for g in gs) +
        "</div></div>" for name, gs in groups)
    panels = "".join(
        f'<section class="cu-panel" id="{gid(g)}" role="tabpanel" aria-labelledby="{gid(g)}-tab"><h3 class="cu-panel-title">{g}</h3><ul class="cu-subjects">' +
        "".join(f'<li><span class="hm-col-icon">{I[SI[s]]}</span><div><strong>{H.escape(s)}</strong><span>{H.escape(G[g].get(s, ""))}</span></div></li>' for s in SUBJECTS) +
        "</ul></section>" for _, gs in groups for g in gs)
    return f'''
  <section class="gv tu-hero2 cu-hero" data-scroll-dim aria-labelledby="cu-title">
    <div class="tu-hero2-img" style="background-image: url('{IMG}covenant-21-9528197.jpg')" aria-hidden="true"></div>
    <div class="gv-wrap tu-hero2-copy">
      <span class="gv-eyebrow">Curriculum</span>
      <h1 id="cu-title">Solid Foundation <span class="cu-l2">in All Core Subjects</span></h1>
      <p class="gv-lead">CCS curriculum objectives are based on Alabama Course of Study Standards, Iowa test standards, and our own philosophy of Christian education.</p>
      <div class="gv-actions"><a class="gv-btn gv-btn-gold" href="#by-grade">Discover Curriculum By Grade</a></div>
    </div>
  </section>

  <section class="gv gv-section gv-white cu-intro" aria-label="Our approach">
    <div class="gv-wrap cu-intro-grid">
      <p class="ns-statement" data-reveal>Teachers look for ways to authentically integrate faith and Bible truth into daily class life and lessons.</p>
      <div class="hm-frame" data-reveal="left"><svg class="hm-frame-line" aria-hidden="true" focusable="false"><rect x="1" y="1" rx="4" ry="4"/></svg><img src="{IMG}fb/ccs-library-kids.jpg" alt="Smiling students holding their prizes in the school library" loading="lazy"></div>
    </div>
  </section>

  <section class="gv gv-section gv-paper" id="by-grade" aria-labelledby="cu-grade-title">
    <div class="gv-wrap">
      <div class="tu-head" data-reveal>
        <span class="gv-eyebrow">Building Blocks for the Future</span>
        <h2 id="cu-grade-title">Discover Curriculum By Grade<span class="mv-dot" aria-hidden="true">.</span></h2>
      </div>
      <div class="cu-tools" data-reveal>
        <span class="hm-col-icon">{I["tablet"]}</span>
        <p>In addition to our grade level curriculum items listed below, grades 1-8 utilize the use of the Renaissance Learning (Accelerated Reader) and iXL Math platforms. <strong>Accelerated Reader</strong> encourages independent reading while promoting comprehension and literacy skills. <strong>iXL Math</strong> offers personalized math practice with targeted exercises, helping students become confident in their mastery skills.</p>
      </div>
      <div class="cu-browser" data-reveal>
        <div class="cu-picker">{tabs}</div>
        <div class="cu-panels">{panels}</div>
      </div>
    </div>
  </section>

  <section class="gv gv-band gv-band-parallax" aria-labelledby="cu-tour-title">
    <div class="gv-band-bg" style="background-image: url('{IMG}covenant-151_1-9523341.jpg')" aria-hidden="true"></div>
    <div class="gv-wrap" data-reveal>
      <h2 id="cu-tour-title">TOUR OUR CAMPUS</h2>
      <p class="gv-band-sub">Your child's exceptional education experience awaits.</p>
      <div class="gv-actions"><a class="gv-btn gv-btn-gold" href="/schedule-tour">SCHEDULE A TOUR</a></div>
    </div>
  </section>
'''
