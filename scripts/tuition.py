"""Preview-only redesign of /tuition. Content is word-for-word from the live page; only layout changes."""

PORTAL = "https://familyportal.renweb.com/"
INFO = "https://ccs-al.client.renweb.com/oa/inquiry.cfm?memberid=3143"
CHOOSE = "http://www.classwallet.com/alchoose"

ENROLL = [  # name, dates, price, track
    ("Priority Re-Enrollment", "January 16th - February 21st", "$175 / Student", "Max $350/Family"),
    ("Re-Enrollment", "February 22nd - April 1st", "$225 / Student", "Max $450/Family"),
    ("Late Re-Enrollment", "April 2nd", "$375 / Student", "Max $750/Family"),
]
TUITION = [
    ("K3/K4", "3 Day Half Day", "$2,899", "$264"),
    ("K3/K4", "3 Day Full Day", "$4,062", "$369"),
    ("K3/K4/K5", "5 Day Half Day", "$5,130", "$466"),
    ("K3/K4/K5", "5 Day Full Day", "$6,831", "$621"),
    ("Elementary", "1st-5th Grade", "$7,053", "$641"),
    ("Junior High", "6th-8th Grade", "$7,229", "$657"),
]
PLANS = [
    ("Annually", "Paid by June 1st &amp; receive a 2% discount", "$25/yr FACTS fee"),
    ("Bi-Annually", "Equal payments due on June 1st &amp; December 1st", "$25/yr FACTS fee"),
    ("Quarterly", "Equal tuition payments paid on June 1st, September 1st, December 1st, March 1st", "$55/yr FACTS fee"),
    ("Monthly", "July-May 11 mo. Tuition payments", "$55/yr FACTS fee"),
]
FEES = [  # name, when, amounts
    ("New Student Screening Fee", "Non-refundable fee paid at the school", ["$20 (K3-K5)", "$30 (1st-8th)"]),
    ("Registration Fee", "Non-refundable fee due at enrollment", ["$200 per student", "Max $400 / family"]),
    ("New Family Processing Fee", "Non-refundable fee due at enrollment", ["$150 per family"]),
    ("FACTS Application Fee", "Non-refundable fee due at enrollment", ["$25 per student"]),
    ("Building / FTP Fees", "Due June 1st", ["$320 per family"]),
]
CURRICULUM = [("K3/K4 3 day half day", "$250"), ("K3/K4 3 day full day", "$250"), ("K3-K5 5 day half day", "$300"), ("K3-K5 5 day full day", "$425"), ("1st-8th Grade", "$425")]

def tuition(ICON, IMG, NEW_TAB):
    import html as H
    chips = "".join(
        f'''<button type="button" class="tu-chip" role="radio" aria-checked="{"true" if k == 0 else "false"}" data-annual="{a}" data-month="{mo}" data-label="{g} · {sub}"><strong>{g}</strong><span>{sub}</span></button>'''
        for k, (g, sub, a, mo) in enumerate(TUITION))
    g0, s0, a0, m0 = TUITION[0]
    rows = "".join(f'''<tr><th scope="row">{g} <span>{sub}</span></th><td>{a}</td><td>{mo}</td></tr>''' for g, sub, a, mo in TUITION)
    enroll = "".join(f'''<li><strong>{n}</strong><span class="tu-when">{d}</span><span class="tu-amt">{p} <em>(Max {m.replace("Max ", "")})</em></span></li>''' for n, d, p, m in ENROLL)
    plans = "".join(f'''<li><strong>{n}</strong><span>{d}</span><em>({f})</em></li>''' for n, d, f in PLANS)
    fees = "".join(f'''<li><strong>{n}</strong><span>{w}</span><b>{" · ".join(a)}</b></li>''' for n, w, a in FEES)
    cur = "".join(f'''<li><strong>{n}</strong><b>{p}</b></li>''' for n, p in CURRICULUM)
    def item(icon, title, body, open_=False, id_=""):
        return f'''<details class="tu-acc"{(' id='+chr(34)+id_+chr(34)) if id_ else ''}{" open" if open_ else ""}><summary><span class="hm-col-icon">{ICON[icon]}</span><span class="tu-acc-t">{title}</span><span class="tu-acc-x" aria-hidden="true"></span></summary><div class="tu-acc-body">{body}</div></details>'''
    return f'''
  <section class="gv gv-hero gv-hero-split ep-hero st-hero tu-hero">
    <img class="ep-hero-eagle" src="{IMG}eagle-mark-white.png" alt="" width="900" height="321">
    <div class="gv-hero-photo" style="background-image: url('{IMG}covenant-24-9584556.jpg')" aria-hidden="true"></div>
    <div class="gv-wrap">
      <div class="gv-hero-copy">
        <span class="gv-eyebrow">New Families</span>
        <h1>Tuition and Fees</h1>
        <p class="gv-lead">Explore our approachable tuition and fees structure, offering key insights into payment schedules, grade-specific pricing, school fees, and beneficial multi-student savings.</p>
        <ul class="tu-checks">
          <li>Clear due dates for tuition and fees</li>
          <li>Tailored rates for each grade level</li>
          <li>Breakdown of additional fees</li>
          <li>Save with our multi-student discounts</li>
        </ul>
      </div>
    </div>
  </section>

  <section class="gv gv-section gv-white tu-calc-sec" id="tuition" aria-labelledby="tu-rate-title">
    <div class="gv-wrap">
      <div class="tu-head tu-center" data-reveal>
        <span class="gv-eyebrow">Tuition</span>
        <h2 id="tu-rate-title">Investing in Your Child's Future<span class="mv-dot" aria-hidden="true">.</span></h2>
        <p>Discover our competitive tuition rates and flexible payment options, ensuring accessibility to quality education for every student.</p>
      </div>
      <div class="tu-calc" data-reveal>
        <div class="tu-chips" role="radiogroup" aria-label="Grade level">{chips}</div>
        <div class="tu-result" aria-live="polite">
          <span class="tu-result-label" data-out="label">{g0} · {s0}</span>
          <div class="tu-result-row">
            <div><span class="tu-k">Annual Tuition</span><span class="tu-big" data-out="annual">{a0}</span></div>
            <div class="tu-or">or</div>
            <div><span class="tu-k">11 Monthly Tuition Payments</span><span class="tu-big tu-big-sm" data-out="month">{m0}</span><span class="tu-fine">(includes $5 service fee)</span></div>
          </div>
        </div>
        <table class="tu-plain"><caption class="gv-sr">Tuition by grade level</caption><thead><tr><th scope="col">Grade level</th><th scope="col">Annual Tuition</th><th scope="col">11 Monthly Tuition Payments (includes $5 service fee)</th></tr></thead><tbody>{rows}</tbody></table>
      </div>
      <p class="tu-note2" data-reveal><strong>Note:</strong> Your tuition amount may be different based on your enrollment date. Call our office for your specific amount. Tuition rates for the 2026–2027 school year will be available in early January 2026.</p>
    </div>
  </section>


  <section class="gv gv-section gv-paper tu-est-sec" id="estimate" aria-labelledby="tu-est-title">
    <div class="gv-wrap">
      <div class="tu-head tu-center" data-reveal>
        <span class="gv-eyebrow">Estimate</span>
        <h2 id="tu-est-title">Add up your family's tuition<span class="mv-dot" aria-hidden="true">.</span></h2>
        <p>Add each child, choose a payment plan, and include any scholarships to see an estimated yearly total.</p>
      </div>
      <div class="tu-est" data-reveal hidden>
        <div class="tu-est-form">
          <fieldset class="tu-est-block">
            <legend>Your students</legend>
            <ol class="tu-kids" id="tu-kids"></ol>
            <button type="button" class="tu-add" id="tu-add"><span aria-hidden="true">+</span> Add another student</button>
          </fieldset>
          <fieldset class="tu-est-block tu-est-row">
            <legend>Your family</legend>
            <label class="tu-field"><span>Family</span>
              <select id="tu-family"><option value="new">New to Covenant</option><option value="returning">Re-enrolling (Priority Re-Enrollment)</option></select></label>
            <label class="tu-field"><span>Payment plan</span>
              <select id="tu-plan"><option value="annual">Annually (2% discount)</option><option value="biannual">Bi-Annually</option><option value="quarterly">Quarterly</option><option value="monthly" selected>Monthly (11 payments)</option></select></label>
            <label class="tu-field"><span>Other scholarships or aid (per year)</span>
              <span class="tu-money"><span aria-hidden="true">$</span><input id="tu-aid" type="number" inputmode="numeric" min="0" step="50" placeholder="0" aria-describedby="tu-aid-hint"></span>
              <small id="tu-aid-hint">For example, an AOSF scholarship award.</small></label>
          </fieldset>
        </div>
        <aside class="tu-est-out" aria-live="polite">
          <h3>Your estimate</h3>
          <dl class="tu-lines" id="tu-lines"></dl>
          <div class="tu-total"><span>Estimated tuition for the year</span><strong id="tu-total">$0</strong><em id="tu-per"></em></div>
          <details class="tu-fees-est"><summary>Plus fees <strong id="tu-fees-total"></strong></summary><dl class="tu-lines" id="tu-fee-lines"></dl></details>
          <p class="tu-disclaimer">This is an estimate only. Your tuition amount may be different based on your enrollment date and your scholarship awards. Call our office at <a href="tel:251-633-8055">251-633-8055</a> for your specific amount.</p>
        </aside>
      </div>
      <noscript><p class="tu-note2">Call our office at 251-633-8055 for your family's specific amount.</p></noscript>
    </div>
  </section>

  <section class="gv gv-section gv-white" id="schedules" aria-labelledby="tu-sched-title">
    <div class="gv-wrap tu-acc-wrap">
      <div class="tu-head tu-center" data-reveal>
        <h2 id="tu-sched-title">Tuition &amp; Fees Schedule<span class="mv-dot" aria-hidden="true">.</span></h2>
      </div>
      <div class="tu-accs" data-reveal>
        {item("calendar", "Save Your Spot for Next Year!", f'''<p>Re-enrollment opens January 16th. Don’t miss early bird savings! Open enrollment starts February 22nd. Limited spots—apply early!</p>
          <h4>CCS Student Re-Enrollment</h4><ul class="tu-list">{enroll}</ul>
          <h4>New Student Enrollment</h4><ul class="tu-list"><li><strong>Open Enrollment</strong><span class="tu-when">February 22nd</span><span class="tu-amt">$200 / New Student <em>(Max $750/Family)</em></span></li></ul>
          <p class="tu-fine">All enrollment fees are non-refundable.</p>''')}
        {item("clock", "Clear due dates for tuition and fees", f'<ul class="tu-list">{plans}</ul>')}
        {item("receipt", "Additional Fees", id_="additional-fees", body=f'''<p>For K3-8th grade, the curriculum fee includes use of all textbooks, consumable workbooks, classroom activities &amp; celebrations, and other materials required for curriculum. Also included is student accident insurance for on &amp; off campus school related activities. Athletic expenses and field trip fees are excluded. All fees are non-refundable.</p>
          <ul class="tu-list">{fees}</ul>
          <h4>Curriculum Fees <span>Non-refundable due June 1st</span></h4><ul class="tu-list">{cur}</ul>''')}
        {item("users", "The Bigger The Family, The More The Savings", id_="discount", body='<span class="tu-label">Multi Student Discount</span><p>There is a 3% discount for the second and third child. Additional discounts for 4th + additional students are determined by administrative staff. No multiple student discounts apply for half-day programs. Please contact the school office for more information.</p>')}
        {item("school", "Choose Act Alabama Is Open", id_="choose", body=f'''<span class="tu-label">Apply Now</span><p>The Choose Act Alabama application portals are now open for both current participants and new families. Don’t miss your opportunity to secure funding for the upcoming school year.</p>
          <h4>Key Dates &amp; Details</h4><ul class="tu-list"><li><strong>Renewal Applications (Current Participants)</strong><span>Open December 15, 2025 – March 31, 2026</span></li><li><strong>New Family Applications ('26–'27 Academic Year)</strong><span>Open January 2, 2026 – March 31, 2026</span></li><li><strong>Funding Amount</strong><b>Up to $7,000 per participating student</b></li></ul>
          <p>Applications are managed through ClassWallet, the official platform for the Choose Act Alabama program. Call ClassWallet support at <a class="ns-tel" href="tel:877-969-5536">877-969-5536</a> for assistance.</p>
          <a class="gv-btn gv-btn-line" href="{CHOOSE}"{NEW_TAB}>Apply Today · Deadline March 31, 2026</a>''')}
      </div>
    </div>
  </section>

  <section class="gv gv-band gv-band-parallax" aria-labelledby="tu-cta-title">
    <div class="gv-band-bg" style="background-image: url('{IMG}covenant-151_1-9523341.jpg')" aria-hidden="true"></div>
    <div class="gv-wrap" data-reveal>
      <h2 id="tu-cta-title">SAVE YOUR SPOT FOR NEXT YEAR!</h2>
      <p class="gv-band-sub">Limited spots—apply early!</p>
      <div class="gv-actions"><a class="gv-btn gv-btn-gold" href="/new-student-application">New Student Enrollment · Start Here</a><a class="gv-btn gv-btn-ghost" href="{PORTAL}"{NEW_TAB}>CCS Student Re-Enrollment · Start Here</a></div>
      <p class="tu-cta-more"><a href="{INFO}"{NEW_TAB}>Request More Information <span aria-hidden="true">&rarr;</span></a></p>
    </div>
  </section>
'''
