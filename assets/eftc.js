// Gentle fade-up for the Federal Tax Credit sections as they scroll into view.
// Content stays visible without JavaScript or with "reduce motion" turned on.
(function () {
  if (!("IntersectionObserver" in window)) return;
  if (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  var groups = [
    ".eftc-intro > .eftc-badge, .eftc-intro > h2, .eftc-intro > p",
    ".eftc-amount", ".eftc-intro > h3", ".eftc-steps li", ".eftc-facts",
    ".eftc-card", ".eftc-help h2, .eftc-help p", ".eftc-callout-inner"
  ];
  function start() {
    var targets = [];
    groups.forEach(function (sel) {
      document.querySelectorAll(sel).forEach(function (el, i) {
        el.classList.add("eftc-reveal");
        el.style.transitionDelay = Math.min(i, 4) * 90 + "ms";
        targets.push(el);
      });
    });
    if (!targets.length) return;
    document.documentElement.classList.add("eftc-anim");
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("is-visible"); io.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.1 });
    targets.forEach(function (el) { io.observe(el); });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
