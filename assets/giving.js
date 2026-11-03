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

// Photo bands marked .gv-band-parallax: the photo moves at a slower pace than the page.
(function () {
  var bands = document.querySelectorAll(".gv-band-parallax");
  if (!bands.length) return;
  if (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  var ticking = false;
  function update() {
    ticking = false;
    var vh = window.innerHeight;
    bands.forEach(function (band) {
      var r = band.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      var progress = (r.top + r.height / 2 - vh / 2) / (vh / 2 + r.height / 2); // -1..1
      var bg = band.querySelector(".gv-band-bg");
      if (bg) bg.style.setProperty("--py", (progress * r.height * 0.2).toFixed(1) + "px");
    });
  }
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(update); } }
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);
  update();
})();
