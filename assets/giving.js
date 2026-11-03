// Scroll-in reveals and number count-ups for the giving / scholarship / tax credit pages.
// Everything stays visible without JavaScript or with "reduce motion" turned on.
(function () {
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce || !("IntersectionObserver" in window)) return;

  function countUp(el) {
    var target = parseFloat(el.getAttribute("data-count"));
    var prefix = el.getAttribute("data-prefix") || "", suffix = el.getAttribute("data-suffix") || "";
    var start = null, dur = 1200;
    function fmt(n) { return prefix + Math.round(n).toLocaleString("en-US") + suffix; }
    function step(t) {
      if (start === null) start = t;
      var p = Math.min((t - start) / dur, 1), eased = 1 - Math.pow(1 - p, 3);
      el.textContent = fmt(target * eased);
      if (p < 1) requestAnimationFrame(step);
    }
    el.textContent = fmt(0);
    requestAnimationFrame(step);
  }

  function start() {
    var items = document.querySelectorAll(".gv [data-reveal]");
    var counters = document.querySelectorAll(".gv [data-count]");
    if (!items.length && !counters.length) return;
    // Stagger siblings that reveal together.
    items.forEach(function (el) {
      var sibs = Array.prototype.filter.call(el.parentNode.children, function (c) { return c.hasAttribute("data-reveal"); });
      var i = sibs.indexOf(el);
      if (i > 0) el.style.transitionDelay = Math.min(i, 5) * 100 + "ms";
    });
    document.documentElement.classList.add("gv-anim");
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add("is-visible");
        e.target.querySelectorAll("[data-count]").forEach(countUp);
        if (e.target.hasAttribute("data-count")) countUp(e.target);
        io.unobserve(e.target);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.12 });
    items.forEach(function (el) { io.observe(el); });
    counters.forEach(function (el) { if (!el.closest("[data-reveal]")) io.observe(el); });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();

// Homepage hero photos: first shows immediately; the rest load after the page, then each
// fades into the next every 6 seconds. Off for "reduce motion"; pauses when the tab is hidden.
(function () {
  var slides = Array.prototype.slice.call(document.querySelectorAll(".hm-slide"));
  if (slides.length < 2) return;
  if (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  function load(el) {
    var src = el.getAttribute("data-src"), img = el.querySelector("img");
    if (src && !img.getAttribute("src")) img.src = src;
  }
  function ready(el) { var img = el.querySelector("img"); return img.getAttribute("src") && img.complete && img.naturalWidth > 0; }
  window.addEventListener("load", function () {
    slides.forEach(load);
    var i = 0;
    setInterval(function () {
      if (document.hidden) return;
      var next = slides[(i + 1) % slides.length];
      if (!ready(next)) return;
      slides[i].classList.remove("on");
      i = (i + 1) % slides.length;
      next.classList.add("on");
    }, 6000);
  });
})();

// Photo bands marked .gv-band-parallax: like the current site, the photo is shown full width at
// its natural shape and drifts at about a quarter of the scroll speed behind the band.
(function () {
  var bands = Array.prototype.slice.call(document.querySelectorAll(".gv-band-parallax"));
  if (!bands.length) return;
  var still = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var SPEED = 0.28, ticking = false;
  // Read each photo's real shape so it can be shown full width without cropping its height.
  bands.forEach(function (band) {
    var bg = band.querySelector(".gv-band-bg");
    band._ratio = 1.5;
    var m = bg && /url\(["']?([^"')]+)/.exec(bg.style.backgroundImage);
    if (!m) return;
    var img = new Image();
    img.onload = function () { band._ratio = img.naturalWidth / img.naturalHeight; onScroll(); };
    img.src = m[1];
  });
  function update() {
    ticking = false;
    var vh = window.innerHeight;
    bands.forEach(function (band) {
      var bg = band.querySelector(".gv-band-bg");
      if (!bg) return;
      var r = band.getBoundingClientRect();
      var h = Math.max(r.width / band._ratio, r.height);
      bg.style.height = h + "px";
      var room = h - r.height;
      var focus = parseFloat(band.getAttribute("data-focus") || ".5");
      var y = -room * focus - (still ? 0 : SPEED * (r.top + r.height / 2 - vh / 2));
      bg.style.setProperty("--py", Math.max(-room, Math.min(0, y)).toFixed(1) + "px");
    });
  }
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(update); } }
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);
  update();
})();

// Homepage photo outline: draws itself in when the photo is about half on screen.
(function () {
  var lines = document.querySelectorAll(".hm-frame-line");
  if (!lines.length || !("IntersectionObserver" in window)) return;
  if (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  lines.forEach(function (svg) {
    var rect = svg.querySelector("rect");
    var w = svg.clientWidth - 2, h = svg.clientHeight - 2;
    if (!w || !h) return;
    rect.setAttribute("width", w); rect.setAttribute("height", h);
    var len = Math.ceil(2 * (w + h)) + 4;
    svg.style.setProperty("--len", len + "px");
    svg.classList.add("is-ready");
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        svg.getBoundingClientRect(); // lock in the hidden state before animating
        requestAnimationFrame(function () { svg.classList.add("is-drawn"); });
        io.disconnect();
      });
    }, { threshold: 0.5 });
    io.observe(svg.parentNode);
  });
})();

// Homepage hero: the photo deepens toward navy as you scroll down past it.
(function () {
  var hero = document.querySelector(".gv-hero-home, [data-scroll-dim]");
  if (!hero) return;
  var ticking = false;
  function update() {
    ticking = false;
    var h = hero.offsetHeight || 1;
    var dim = Math.min(Math.max(window.scrollY / (h * 0.55), 0), 1);
    hero.style.setProperty("--hero-dim", dim.toFixed(3));
  }
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
  update();
})();

// Mission & Values timeline: a tan line fills as you scroll; each year lights up when the line reaches it.
(function () {
  document.querySelectorAll(".mv-timeline").forEach(function (tl) {
  var bar = tl.querySelector(".mv-progress"), track = tl.querySelector(".mv-track");
  var items = Array.prototype.slice.call(tl.querySelectorAll("li"));
  if (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches) {
    items.forEach(function (li) { li.classList.add("is-reached"); });
    return; // (inside forEach: skips just this timeline)
  }
  tl.classList.add("is-live");
  var ticking = false;
  function update() {
    ticking = false;
    var r = track.getBoundingClientRect();
    var mark = window.innerHeight * 0.62;              // where the "reading line" sits on screen
    var p = Math.min(Math.max((mark - r.top) / (r.height || 1), 0), 1);
    tl.style.setProperty("--mv-p", p.toFixed(3));
    items.forEach(function (li) {
      li.classList.toggle("is-reached", li.getBoundingClientRect().top + 16 <= mark);
    });
  }
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(update); } }
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);
  update();
  });
})();

// Employment: tapping a position tile chooses it in the application form and brings the form into view.
(function () {
  var tiles = document.querySelectorAll("[data-pick-position]");
  var select = document.getElementById("ef-position");
  if (!tiles.length || !select) return;
  var still = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  tiles.forEach(function (b) {
    b.addEventListener("click", function () {
      select.value = b.getAttribute("data-pick-position");
      select.dispatchEvent(new Event("change", { bubbles: true }));
      var card = select.closest(".ep-card") || select;
      card.scrollIntoView({ behavior: still ? "auto" : "smooth", block: "start" });
      card.classList.remove("is-picked"); void card.offsetWidth; card.classList.add("is-picked");
      setTimeout(function () { var n = document.getElementById("ef-name"); (n || select).focus({ preventScroll: true }); }, still ? 0 : 600);
    });
  });
})();

// Tuition: choose a grade level to see its annual and monthly tuition.
(function () {
  var chips = document.querySelectorAll(".tu-chip");
  if (!chips.length) return;
  document.documentElement.classList.add("tu-js");
  var out = {}; document.querySelectorAll("[data-out]").forEach(function (el) { out[el.getAttribute("data-out")] = el; });
  function pick(c) {
    chips.forEach(function (x) { x.setAttribute("aria-checked", x === c ? "true" : "false"); x.tabIndex = x === c ? 0 : -1; });
    out.label.textContent = c.getAttribute("data-label");
    out.annual.textContent = c.getAttribute("data-annual");
    out.month.textContent = c.getAttribute("data-month");
  }
  chips.forEach(function (c, i) {
    c.tabIndex = i === 0 ? 0 : -1;
    c.addEventListener("click", function () { pick(c); });
    c.addEventListener("keydown", function (e) {
      var k = e.key, n = null;
      if (k === "ArrowRight" || k === "ArrowDown") n = chips[(i + 1) % chips.length];
      if (k === "ArrowLeft" || k === "ArrowUp") n = chips[(i - 1 + chips.length) % chips.length];
      if (n) { e.preventDefault(); pick(n); n.focus(); }
    });
  });
})();

// Tuition: links to a section (e.g. /tuition#additional-fees) open that row.
(function () {
  function openHash() { var el = location.hash && document.getElementById(location.hash.slice(1)); if (el && el.tagName === "DETAILS") { el.open = true; el.scrollIntoView({ block: "start" }); } }
  window.addEventListener("hashchange", openHash);
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", openHash); else openHash();
})();

// Tuition estimator: tuition per student, 3% for the 2nd and 3rd child (not half-day programs),
// payment-plan discount, CHOOSE Act and other scholarships, and the published fees.
(function () {
  var box = document.querySelector(".tu-est");
  if (!box) return;
  box.hidden = false;
  var PROGRAMS = [
    { id: "k3h", name: "K3/K4 · 3 Day Half Day", tuition: 2899, cur: 250, half: true, young: true },
    { id: "k3f", name: "K3/K4 · 3 Day Full Day", tuition: 4062, cur: 250, half: false, young: true },
    { id: "k5h", name: "K3/K4/K5 · 5 Day Half Day", tuition: 5130, cur: 300, half: true, young: true },
    { id: "k5f", name: "K3/K4/K5 · 5 Day Full Day", tuition: 6831, cur: 425, half: false, young: true },
    { id: "el", name: "Elementary · 1st-5th Grade", tuition: 7053, cur: 425, half: false, young: false },
    { id: "jh", name: "Junior High · 6th-8th Grade", tuition: 7229, cur: 425, half: false, young: false }
  ];
  var FACTS = { annual: 25, biannual: 25, quarterly: 55, monthly: 55 };
  var PAYMENTS = { annual: 1, biannual: 2, quarterly: 4, monthly: 11 };
  var list = document.getElementById("tu-kids"), add = document.getElementById("tu-add");
  var family = document.getElementById("tu-family"), aid = document.getElementById("tu-aid");
  var plan = { get value() { var c = box.querySelector('input[name="tu-plan"]:checked'); return c ? c.value : "monthly"; } };
  var lines = document.getElementById("tu-lines"), feeLines = document.getElementById("tu-fee-lines");
  var totalEl = document.getElementById("tu-total"), perEl = document.getElementById("tu-per"), feesTotal = document.getElementById("tu-fees-total");
  var n = 0;
  function $(v) { return "$" + Math.round(v).toLocaleString("en-US"); }
  function row(dl, label, value, cls) { var dt = document.createElement("dt"), dd = document.createElement("dd"); dt.textContent = label; dd.textContent = value; if (cls) { dt.className = dd.className = cls; } dl.appendChild(dt); dl.appendChild(dd); }
  function addKid(pid) {
    n++;
    var li = document.createElement("li"); li.className = "tu-kid";
    var opts = PROGRAMS.map(function (p) { return '<option value="' + p.id + '"' + (p.id === pid ? " selected" : "") + ">" + p.name + " — " + $(p.tuition) + "</option>"; }).join("");
    li.innerHTML = '<span class="tu-kid-n" aria-hidden="true"></span>' +
      '<label class="tu-field"><span>Grade level</span><select class="tu-kid-p">' + opts + "</select></label>" +
      '<label class="tu-check"><input type="checkbox" class="tu-kid-choose"><span>CHOOSE Act ESA <small>(up to $7,000, grades K5–12)</small></span></label>' +
      '<button type="button" class="tu-remove" aria-label="Remove this student">&times;</button>';
    list.appendChild(li);
    li.querySelector(".tu-remove").addEventListener("click", function () { li.remove(); calc(); });
    li.querySelectorAll("select,input").forEach(function (el) { el.addEventListener("change", calc); });
    calc();
  }
  function calc() {
    var kids = Array.prototype.map.call(list.children, function (li, i) {
      li.querySelector(".tu-kid-n").textContent = String(i + 1).padStart(2, "0");
      li.querySelector(".tu-remove").hidden = list.children.length === 1;
      var p = PROGRAMS.filter(function (x) { return x.id === li.querySelector(".tu-kid-p").value; })[0];
      var cb = li.querySelector(".tu-kid-choose"), k3 = p.id === "k3h" || p.id === "k3f";
      cb.disabled = k3; if (k3) cb.checked = false;   // CHOOSE Act covers grades K5-12
      cb.closest("label").classList.toggle("is-off", k3);
      return { p: p, choose: cb.checked };
    });
    lines.innerHTML = ""; feeLines.innerHTML = "";
    var sum = 0, disc = 0, eligible = 0, staff = false;
    kids.forEach(function (k, i) {
      row(lines, "Student " + (i + 1) + " · " + k.p.name, $(k.p.tuition));
      sum += k.p.tuition;
      if (!k.p.half) { eligible++; if (eligible === 2 || eligible === 3) disc += k.p.tuition * 0.03; else if (eligible >= 4) staff = true; }
    });
    var net = sum - disc;
    if (disc) row(lines, "Multi-student discount (3% for 2nd & 3rd child)", "−" + $(disc), "is-save");
    else if (kids.length > 1) row(lines, "Multi-student discount — no multiple student discounts apply for half-day programs", "$0", "is-note");
    var pl = plan.value;
    if (pl === "annual") { var ad = net * 0.02; net -= ad; row(lines, "Paid annually by June 1st (2% discount)", "−" + $(ad), "is-save"); }
    var choose = 0;
    kids.forEach(function (k) { if (k.choose) choose += Math.min(7000, k.p.tuition); });
    if (choose) row(lines, "CHOOSE Act ESA (estimated)", "−" + $(choose), "is-save");
    var other = Math.max(0, parseFloat(aid.value) || 0);
    if (other) row(lines, "Other scholarships or aid", "−" + $(other), "is-save");
    if (pl === "quarterly" || pl === "monthly") row(lines, "Payment plan", (pl === "monthly" ? "11 monthly" : "4 quarterly") + " payments", "is-note");
    var total = Math.max(0, net - choose - other);
    if (staff) row(lines, "4th + additional students", "Ask our office", "is-note");
    totalEl.textContent = $(total);
    var pays = PAYMENTS[pl];
    perEl.textContent = pays > 1 && total > 0 ? "about " + $(total / pays) + " × " + pays + " payments" : "";
    // Fees
    var fees = 0, kidsN = kids.length, isNew = family.value === "new";
    function fee(label, v) { if (v) { row(feeLines, label, $(v)); fees += v; } }
    if (isNew) {
      var scr = kids.reduce(function (s, k) { return s + (k.p.young ? 20 : 30); }, 0);
      fee("New Student Screening Fee", scr);
      fee("Registration Fee ($200 per student, max $400 / family)", Math.min(400, 200 * kidsN));
      fee("New Family Processing Fee", 150);
      fee("FACTS Application Fee ($25 per student)", 25 * kidsN);
    } else {
      fee("Priority Re-Enrollment ($175 / student, max $350 / family)", Math.min(350, 175 * kidsN));
    }
    fee("Curriculum Fees", kids.reduce(function (s, k) { return s + k.p.cur; }, 0));
    fee("Building / FTP Fees", 320);
    fee("FACTS payment plan fee (per year)", FACTS[pl]);
    feesTotal.textContent = $(fees);
    var tip = document.getElementById("tu-tip");
    if (tip) { var saveAnnual = (sum - disc) * 0.02 + (FACTS[pl] - 25); tip.textContent = pl === "annual" ? "You’re saving with the annual 2% discount." : "Paying annually by June 1st would save about " + $(saveAnnual) + " a year."; }
  }
  add.addEventListener("click", function () { addKid("el"); var s = list.lastElementChild.querySelector("select"); s.focus(); });
  family.addEventListener("change", calc);
  box.querySelectorAll('input[name="tu-plan"]').forEach(function (r) { r.addEventListener("change", calc); });
  aid.addEventListener("input", calc);
  addKid("el");
})();

// Secondary-page heroes: photo layer moves at ~70% of scroll speed while the hero is on screen.
// Mid-page photo sections (Statement of Faith) drift gently around their resting spot.
(function () {
  var layers = document.querySelectorAll(".mv-hero-bg, .tu-hero2-img, .ns-hero-img, .st-hero .gv-hero-photo");
  var drift = document.querySelectorAll(".mv-faith-bg");
  if (!layers.length && !drift.length) return;
  if (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  var ticking = false;
  function update() {
    ticking = false;
    var vh = window.innerHeight, y = window.scrollY;
    layers.forEach(function (el) {
      var r = el.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      var base = Math.max(0, r.top + y - vh);          // scroll position where the hero first comes into view
      var shift = Math.max(0, (y - base) * 0.3);
      shift = Math.min(shift, 70 + Math.max(0, -r.top)); // never open a gap above a visible hero
      el.style.setProperty("--hp", shift.toFixed(1) + "px");
    });
    drift.forEach(function (el) {
      var r = el.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      var shift = -(r.top + r.height / 2 - vh / 2) * 0.18;
      el.style.setProperty("--hp", Math.max(-90, Math.min(90, shift)).toFixed(1) + "px");
    });
  }
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
  window.addEventListener("resize", update);
  update();
})();
