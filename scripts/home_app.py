"""Homepage 'Download the App' section (preview only)."""

APP = "https://aware3.net/shortcode/?code=covenantchristianschool-f"
IOS = "https://apps.apple.com/us/app/id1636762809"
AND = "https://play.google.com/store/apps/details?id=com.airealmobile.covenantchristianschool_f_35647"
APPLE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M16.4 12.6c0-2.6 2.1-3.8 2.2-3.9-1.2-1.8-3.1-2-3.7-2-1.6-.2-3.1.9-3.9.9-.8 0-2-.9-3.4-.9-1.7 0-3.3 1-4.2 2.6-1.8 3.1-.5 7.7 1.3 10.2.9 1.2 1.9 2.6 3.2 2.6 1.3-.1 1.8-.8 3.3-.8 1.6 0 2 .8 3.4.8 1.4 0 2.3-1.3 3.1-2.5 1-1.4 1.4-2.8 1.4-2.9-.1 0-2.7-1-2.7-4.1zM13.9 5c.7-.9 1.2-2.1 1.1-3.3-1 0-2.3.7-3 1.6-.7.8-1.2 2-1.1 3.2 1.1.1 2.3-.6 3-1.5z"/></svg>'
PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M3.6 2.3c-.3.3-.5.8-.5 1.4v16.6c0 .6.2 1.1.5 1.4l9.3-9.7-9.3-9.7zm10.4 8.6 2.6-2.7L5.4 1.8c-.4-.2-.8-.3-1.1-.2l9.7 9.3zm0 2.2-9.7 9.3c.3.1.7 0 1.1-.2l11.2-6.4-2.6-2.7zm6.6-2.6-3-1.7-2.8 2.9 2.8 2.9 3-1.7c.9-.5.9-1.9 0-2.4z"/></svg>'
S = 'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'
EXTRA = {
    "apple": f'<svg {S}><path d="M12 7c-1.5-1.2-4-1.4-5.5 0C4.7 8.7 5 12.5 6.6 15.5 7.8 17.8 9.3 20 11 19.6c.6-.1.7-.4 1-.4s.4.3 1 .4c1.7.4 3.2-1.8 4.4-4.1C19 12.5 19.3 8.7 17.5 7c-1.5-1.4-4-1.2-5.5 0Z"/><path d="M12 7c0-2 1-3.5 3-4"/></svg>',
    "megaphone": f'<svg {S}><path d="M3 11v3a1 1 0 0 0 1 1h2l4 4V6L6 10H4a1 1 0 0 0-1 1Z"/><path d="M14 8a5 5 0 0 1 0 8"/><path d="M17 5a9 9 0 0 1 0 14"/></svg>',
    "grade": f'<svg {S}><circle cx="12" cy="12" r="9"/><path d="m8 15 2.5-6 2.5 6"/><path d="M9 13h3"/><path d="M16 9v4M14 11h4"/></svg>',
    "dollar": f'<svg {S}><rect x="2" y="5" width="20" height="14" rx="2"/><path d="M12 9v6M14 10h-2.5a1.5 1.5 0 0 0 0 3h1a1.5 1.5 0 0 1 0 3H10"/></svg>',
    "bell": f'<svg {S}><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/></svg>',
}

def app_section(ICON, IMG, NEW_TAB):
    I = dict(ICON); I.update(EXTRA)
    feats = [("apple", "Lunch", "Order by 5pm Sunday"), ("megaphone", "Announcements", "News as it happens"),
             ("calendar", "Calendar", "Every school day & event"), ("grade", "Gradebook", "Grades at a glance"),
             ("pen", "Homework", "Assignments in one place"), ("file", "Lesson Plans", "See what's being taught"),
             ("dollar", "Financials", "Tuition & payments"), ("users", "Directory", "Reach teachers & staff"),
             ("clock", "Schedule", "Your student's day"), ("mail", "Inbox", "Messages from school")]
    chips = "".join(f'<li class="hm-app-chip c{n}" style="--d:{n * .35:.2f}s"><span class="hm-app-ic">{I[ic]}</span><span><strong>{t}</strong><small>{d}</small></span></li>' for n, (ic, t, d) in enumerate(feats))
    return f'''<section class="gv gv-section hm-app" aria-labelledby="hm-app-title">
    <div class="hm-app-glow" aria-hidden="true"></div>
    <div class="gv-wrap hm-app-grid">
      <div class="hm-app-copy" data-reveal>
        <span class="gv-eyebrow">The CCS App</span>
        <h2 id="hm-app-title">School Life, <span>Right in Your Pocket.</span></h2>
        <p class="hm-app-lead">Lunch orders, grades, homework, announcements and the school calendar, all in one free app for Covenant families.</p>
        <div class="hm-app-lunch"><span class="hm-app-ic">{I["apple"]}</span><p><strong>Order Lunch</strong> Conveniently order lunch on our app! Simplify your busy schedule by placing your lunch orders by 5pm on the Sunday before each week of service.</p></div>
        <div class="hm-app-stores">
          <a class="hm-app-store" href="{IOS}"{NEW_TAB}>{APPLE}<span><small>Download on the</small>App Store</span></a>
          <a class="hm-app-store" href="{AND}"{NEW_TAB}>{PLAY}<span><small>Get it on</small>Google Play</span></a>
        </div>
      </div>
      <div class="hm-app-stage" data-reveal="left">
        <div class="hm-app-ring" aria-hidden="true"></div>
        <div class="hm-app-phone"><img src="{IMG}app-home.jpg" alt="The Covenant Christian School app home screen" loading="lazy"></div>
        <ul class="hm-app-chips" aria-label="What you can do in the app">{chips}</ul>
      </div>
    </div>
  </section>'''
