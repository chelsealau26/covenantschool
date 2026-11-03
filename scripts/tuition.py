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
    enroll = "".join(f'''<li class="tu-step" data-reveal><span class="tu-dot" aria-hidden="true"></span><h4>{n}</h4><p class="tu-when">{d}</p><p class="tu-price">{p} <span>({m})</span></p><p class="tu-nr">(Non-refundable)</p></li>''' for n, d, p, m in ENROLL)
    rows = "".join(f'''<tr><th scope="row"><strong>{g}</strong><span>{s}</span></th><td class="tu-annual">{a}</td><td class="tu-month">{mo}<span>(includes $5 service fee)</span></td></tr>''' for g, s, a, mo in TUITION)
    plans = "".join(f'''<li data-reveal><h4>{n}</h4><p>{d}</p><span class="tu-tag">{f}</span></li>''' for n, d, f in PLANS)
    fees = "".join(f'''<tr><th scope="row">{n}<span>{w}</span></th><td>{"<br>".join(a)}</td></tr>''' for n, w, a in FEES)
    cur = "".join(f'<tr><th scope="row">{n}</th><td>{p}</td></tr>' for n, p in CURRICULUM)
    return f'''
  <section class="gv gv-hero gv-hero-split ep-hero st-hero tu-hero">
    <img class="ep-hero-eagle" src="{IMG}eagle-mark-white.png" alt="" width="900" height="321">
    <div class="gv-hero-photo" style="background-image: url('{IMG}covenant-24-9584556.jpg')" aria-hidden="true"></div>
    <div class="gv-wrap">
      <div class="gv-hero-copy">
        <h1>Tuition and Fees</h1>
        <p class="gv-lead">Explore our approachable tuition and fees structure, offering key insights into payment schedules, grade-specific pricing, school fees, and beneficial multi-student savings.</p>
        <div class="gv-actions">
          <a class="gv-btn gv-btn-gold" href="/new-student-application">New Student Enrollment</a>
          <a class="gv-btn gv-btn-ghost" href="{PORTAL}"{NEW_TAB}>CCS Student Re-Enrollment</a>
        </div>
      </div>
    </div>
  </section>

  <nav class="gv gv-jump tu-jump" aria-label="On this page">
    <div class="gv-wrap">
      <div class="gv-jump-links">
        <a href="#enrollment">Enrollment dates</a><a href="#tuition">Tuition</a><a href="#payments">Payment options</a><a href="#fees">Additional fees</a><a href="#discount">Multi-student discount</a><a href="#choose">Choose Act</a>
      </div>
    </div>
  </nav>

  <section class="gv gv-section gv-white" id="enrollment" aria-labelledby="tu-enroll-title">
    <div class="gv-wrap">
      <div class="tu-head" data-reveal><h2 id="tu-enroll-title">Save Your Spot for Next Year!</h2><p>Re-enrollment opens January 16th. Don’t miss early bird savings! Open enrollment starts February 22nd. Limited spots—apply early!</p></div>
      <div class="tu-tracks">
        <div class="tu-track">
          <div class="tu-track-head"><h3>CCS Student Re-Enrollment</h3><a class="ns-link" href="{PORTAL}"{NEW_TAB}>Start Here <span aria-hidden="true">&rarr;</span></a></div>
          <ol class="tu-steps">{enroll}</ol>
        </div>
        <div class="tu-track tu-track-new">
          <div class="tu-track-head"><h3>New Student Enrollment</h3><a class="ns-link" href="/new-student-application">Start Here <span aria-hidden="true">&rarr;</span></a></div>
          <ol class="tu-steps"><li class="tu-step" data-reveal><span class="tu-dot" aria-hidden="true"></span><h4>Open Enrollment</h4><p class="tu-when">February 22nd</p><p class="tu-price">$200 / New Student <span>(Max $750/Family)</span></p><p class="tu-nr">(Non-refundable)</p></li></ol>
        </div>
      </div>
    </div>
  </section>

  <section class="gv gv-section gv-paper" aria-labelledby="tu-sched-title">
    <div class="gv-wrap tu-sched">
      <div data-reveal>
        <span class="gv-eyebrow">New Families</span>
        <h2 id="tu-sched-title">Tuition &amp; Fees Schedule<span class="mv-dot" aria-hidden="true">.</span></h2>
      </div>
      <ul class="tu-index" data-reveal>
        <li><a href="#payments"><span class="hm-col-icon">{ICON["calendar"]}</span>Clear due dates for tuition and fees</a></li>
        <li><a href="#tuition"><span class="hm-col-icon">{ICON["school"]}</span>Tailored rates for each grade level</a></li>
        <li><a href="#fees"><span class="hm-col-icon">{ICON["receipt"]}</span>Breakdown of additional fees</a></li>
        <li><a href="#discount"><span class="hm-col-icon">{ICON["users"]}</span>Save with our multi-student discounts</a></li>
      </ul>
    </div>
  </section>

  <section class="gv gv-section gv-white" id="tuition" aria-labelledby="tu-rate-title">
    <div class="gv-wrap">
      <div class="tu-head" data-reveal>
        <span class="gv-eyebrow">Tuition</span>
        <h2 id="tu-rate-title">Investing in Your Child's Future<span class="mv-dot" aria-hidden="true">.</span></h2>
        <p>Discover our competitive tuition rates and flexible payment options, ensuring accessibility to quality education for every student.</p>
      </div>
      <div class="tu-table-wrap" data-reveal>
        <table class="tu-table">
          <caption class="gv-sr">Tuition by grade level</caption>
          <thead><tr><th scope="col">Grade level</th><th scope="col">Annual Tuition</th><th scope="col">11 Monthly Tuition Payments</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
      <p class="tu-note" data-reveal><span class="hm-col-icon">{ICON["info"]}</span><span><strong>Note:</strong> Your tuition amount may be different based on your enrollment date. Call our office for your specific amount. Tuition rates for the 2026–2027 school year will be available in early January 2026.</span></p>
    </div>
  </section>

  <section class="gv gv-section gv-dark tu-plans" id="payments" aria-labelledby="tu-plans-title">
    <img class="mv-faith-eagle" src="{IMG}eagle-mark-white.png" alt="" width="900" height="321">
    <div class="gv-wrap">
      <div class="tu-head" data-reveal><h2 id="tu-plans-title">Clear due dates for tuition and fees<span class="mv-dot" aria-hidden="true">.</span></h2></div>
      <ul class="tu-plan-grid">{plans}</ul>
    </div>
  </section>

  <section class="gv gv-section gv-white" id="fees" aria-labelledby="tu-fees-title">
    <div class="gv-wrap">
      <div class="tu-head" data-reveal>
        <h2 id="tu-fees-title">Additional Fees<span class="mv-dot" aria-hidden="true">.</span></h2>
        <p>For K3-8th grade, the curriculum fee includes use of all textbooks, consumable workbooks, classroom activities &amp; celebrations, and other materials required for curriculum. Also included is student accident insurance for on &amp; off campus school related activities. Athletic expenses and field trip fees are excluded. All fees are non-refundable.</p>
      </div>
      <div class="tu-fees" data-reveal>
        <table class="tu-table tu-fee-table"><caption class="gv-sr">Additional fees</caption><tbody>{fees}</tbody></table>
        <div class="tu-cur">
          <h3>Curriculum Fees</h3><p class="tu-cur-when">Non-refundable due June 1st</p>
          <table class="tu-table tu-cur-table"><caption class="gv-sr">Curriculum fees</caption><tbody>{cur}</tbody></table>
        </div>
      </div>
    </div>
  </section>

  <section class="gv gv-band gv-band-left gv-band-parallax tu-discount" id="discount" data-focus=".3" aria-labelledby="tu-disc-title">
    <div class="gv-band-bg" style="background-image: url('{IMG}covenant-94-9522791.jpg')" aria-hidden="true"></div>
    <div class="gv-wrap" data-reveal>
      <span class="gv-eyebrow">Multi Student Discount</span>
      <h2 id="tu-disc-title">The Bigger The Family, The More The Savings</h2>
      <p>There is a 3% discount for the second and third child. Additional discounts for 4th + additional students are determined by administrative staff. No multiple student discounts apply for half-day programs. Please contact the school office for more information.</p>
      <div class="gv-actions"><a class="gv-btn gv-btn-gold" href="/new-student-application">Apply Today</a><a class="gv-btn gv-btn-ghost" href="{INFO}"{NEW_TAB}>Request More Information</a></div>
    </div>
  </section>

  <section class="gv gv-section gv-paper" id="choose" aria-labelledby="tu-choose-title">
    <div class="gv-wrap tu-choose">
      <div data-reveal>
        <span class="gv-eyebrow">Apply Now</span>
        <h2 id="tu-choose-title">Choose Act Alabama Is Open<span class="mv-dot" aria-hidden="true">.</span></h2>
        <p class="mv-body">The Choose Act Alabama application portals are now open for both current participants and new families. Don’t miss your opportunity to secure funding for the upcoming school year.</p>
        <p class="tu-small">Applications are managed through ClassWallet, the official platform for the Choose Act Alabama program. Call ClassWallet support at <a class="ns-tel" href="tel:877-969-5536">877-969-5536</a> for assistance.</p>
        <a class="gv-btn gv-btn-line" href="{CHOOSE}"{NEW_TAB}>Apply Today · Deadline March 31, 2026</a>
      </div>
      <div class="tu-choose-facts" data-reveal>
        <h3>Key Dates &amp; Details</h3>
        <dl>
          <div><dt>Renewal Applications (Current Participants)</dt><dd>Open December 15, 2025 – March 31, 2026</dd></div>
          <div><dt>New Family Applications ('26–'27 Academic Year)</dt><dd>Open January 2, 2026 – March 31, 2026</dd></div>
          <div class="tu-big"><dt>Funding Amount</dt><dd>Up to $7,000 per participating student</dd></div>
        </dl>
      </div>
    </div>
  </section>
'''
