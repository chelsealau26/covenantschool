"""Final SEO pass for generated pages (runs at the end of every build).
- Share image (og/twitter) = the page's own hero photo, on covenantschool.com
- og:site_name; hero image preload for faster first paint (LCP)
- FAQPage data for FAQ accordions; Event data for the school calendar
"""
import re, json, html as H

SITE = "https://covenantschool.com"

def _text(s):
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", s))).strip()

def _hero(main):
    m = re.search(r"background-image:\s*url\('([^']+)'\)", main) or re.search(r'<img[^>]+src="([^"]+)"', main)
    return m.group(1) if m else None

def _ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"

def finalize(page_html, name):
    page_html = re.sub(r"<!--seo-->[\s\S]*?<!--/seo-->", "", page_html)   # idempotent (some pages rebuild from themselves)
    head_end = page_html.index("</head>")
    head, rest = page_html[:head_end], page_html[head_end:]
    main = rest[rest.index("<main"):rest.index("</main>")] if "<main" in rest else ""
    extra = []

    hero = _hero(main)
    if hero and hero.startswith("/assets/"):
        abs_url = SITE + hero
        head = re.sub(r'(<meta property="og:image" content=")[^"]*(")', r"\g<1>" + abs_url + r"\g<2>", head)
        head = re.sub(r'(<meta name="twitter:image" content=")[^"]*(")', r"\g<1>" + abs_url + r"\g<2>", head)
        if "og:image" not in head:
            extra.append(f'<meta property="og:image" content="{abs_url}">')
        extra.append(f'<link rel="preload" as="image" href="{hero}" fetchpriority="high">')
    if 'og:site_name' not in head:
        extra.append('<meta property="og:site_name" content="Covenant Christian School">')

    # FAQ accordions -> FAQPage
    qa = []
    for d in re.finditer(r"<details[^>]*>\s*<summary>([\s\S]*?)</summary>([\s\S]*?)</details>", main):
        q = _text(re.sub(r'<span class="ct-n"[^>]*>[\s\S]*?</span>', "", d.group(1)))
        a = _text(re.sub(r'<div class="ct-cta">[\s\S]*?</div>', "", d.group(2)))
        if q.endswith("?") and len(a) > 20:
            qa.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
    if len(qa) >= 2:
        extra.append(_ld({"@context": "https://schema.org", "@type": "FAQPage", "@id": f"{SITE}/{name}#faq", "mainEntity": qa}))

    # School calendar -> Event list
    cal = re.search(r'<script type="application/json" id="cal-events-data">([\s\S]*?)</script>', main)
    if cal:
        place = {"@type": "Place", "name": "Covenant Christian School",
                 "address": {"@type": "PostalAddress", "streetAddress": "7150 Hitt Rd", "addressLocality": "Mobile", "addressRegion": "AL", "postalCode": "36695", "addressCountry": "US"}}
        evs = []
        for e in json.loads(cal.group(1)):
            if e.get("color") == "#c0392b": continue          # "No School" days are not events
            ev = {"@type": "Event", "name": e["title"], "startDate": e["start"], "eventStatus": "https://schema.org/EventScheduled",
                  "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode", "location": place,
                  "organizer": {"@id": f"{SITE}/#school"}}
            if e.get("end"): ev["endDate"] = e["end"]
            evs.append(ev)
        if evs:
            extra.append(_ld({"@context": "https://schema.org", "@type": "ItemList", "name": "Covenant Christian School Calendar",
                              "itemListElement": [{"@type": "ListItem", "position": i, "item": ev} for i, ev in enumerate(evs, 1)]}))

    return head + "<!--seo-->" + "".join(extra) + "<!--/seo-->" + rest
