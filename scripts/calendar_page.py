"""Preview-only redesign of /calendar. The calendar widget (events, legend, day popup) is copied
from the live page on every build, so event updates made there carry over automatically."""
import re, json

PDF = "https://raw.githubusercontent.com/chelsealau26/covenantschool/main/pdfs/2026-2027_School_Calendar.pdf"
APP = "https://aware3.net/shortcode/?code=covenantchristianschool-f"

def calendar_page(ICON, IMG, NEW_TAB, pages):
    I = ICON
    live = (pages / "calendar.html").read_text()
    m = live[live.index("<main"):live.index("</main>")]
    a = m.index("<!-- FullCalendar -->")
    b = m.rindex("</script>") + len("</script>")
    widget = m[a:b]
    # The day pop-up's weekday label is not a section heading (keeps the heading outline clean).
    widget = re.sub(r'<h3 id="cal-popup-weekday"[^>]*></h3>', '<p id="cal-popup-weekday" class="cal-pop-wd" aria-hidden="true"></p>', widget)
    js = re.findall(r"var SCHOOL_EVENTS = (\[[\s\S]*?\]);", widget)[0]
    events = json.dumps(json.loads(js), separators=(",", ":"))
    return f'''
  <section class="gv cal-hero" aria-labelledby="cal-title">
    <div class="gv-wrap cal-hero-in">
      <div>
        <span class="gv-eyebrow">Parent Central</span>
        <h1 id="cal-title">School Calendar</h1>
      </div>
    </div>
  </section>

  <section class="gv gv-section gv-paper cal-sec" id="cal-month" aria-label="School calendar">
    <div class="gv-wrap cal-grid">
      <div class="cal-main">{widget}</div>
      <aside class="cal-side" aria-labelledby="cal-next-title">
        <h2 id="cal-next-title">Coming Up</h2>
        <ol class="cal-next" id="cal-next"></ol>
        <a class="gv-btn gv-btn-gold cal-side-btn" href="{PDF}"{NEW_TAB}>Download the 2026-2027 Calendar</a>
        <a class="cal-side-app" href="{APP}"{NEW_TAB}><span class="hm-col-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="6" y="2" width="12" height="20" rx="2.5"/><path d="M11 18h2"/></svg></span><span>Download the App</span></a>
      </aside>
    </div>
    <script type="application/json" id="cal-events-data">{events}</script>
  </section>
'''
