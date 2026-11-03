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
