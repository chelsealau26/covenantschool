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
