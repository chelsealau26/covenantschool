// Preview only: "Download the App" opens a lightbox with the store links instead of a new tab.
(function () {
  var IOS = "https://apps.apple.com/us/app/id1636762809";
  var AND = "https://play.google.com/store/apps/details?id=com.airealmobile.covenantchristianschool_f_35647";
  var dlg, opener;
  function isApp(a) { return a && /aware3\.net\/shortcode/i.test(a.getAttribute("href") || ""); }
  function build() {
    var ua = navigator.userAgent, ios = /iPhone|iPad|iPod|Macintosh/.test(ua) && !/Android/.test(ua), and = /Android/.test(ua);
    dlg = document.createElement("dialog");
    dlg.className = "ccs-app";
    dlg.setAttribute("aria-labelledby", "ccs-app-title");
    dlg.innerHTML =
      '<button type="button" class="ccs-app-x" aria-label="Close">&times;</button>' +
      '<img class="ccs-app-logo" src="/assets/eagle-mark-white.png" alt="" width="72" height="72">' +
      '<h2 id="ccs-app-title">Download the CCS App</h2>' +
      '<p>Get the Covenant Christian School app on your phone.</p>' +
      '<div class="ccs-app-btns">' +
      '<a class="ccs-app-btn' + (and ? "" : " is-main") + '" href="' + IOS + '" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M16.4 12.6c0-2.6 2.1-3.8 2.2-3.9-1.2-1.8-3.1-2-3.7-2-1.6-.2-3.1.9-3.9.9-.8 0-2-.9-3.4-.9-1.7 0-3.3 1-4.2 2.6-1.8 3.1-.5 7.7 1.3 10.2.9 1.2 1.9 2.6 3.2 2.6 1.3-.1 1.8-.8 3.3-.8 1.6 0 2 .8 3.4.8 1.4 0 2.3-1.3 3.1-2.5 1-1.4 1.4-2.8 1.4-2.9-.1 0-2.7-1-2.7-4.1zM13.9 5c.7-.9 1.2-2.1 1.1-3.3-1 0-2.3.7-3 1.6-.7.8-1.2 2-1.1 3.2 1.1.1 2.3-.6 3-1.5z"/></svg><span><small>Download on the</small>App Store</span></a>' +
      '<a class="ccs-app-btn' + (and ? " is-main" : "") + '" href="' + AND + '" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M3.6 2.3c-.3.3-.5.8-.5 1.4v16.6c0 .6.2 1.1.5 1.4l9.3-9.7-9.3-9.7zm10.4 8.6 2.6-2.7L5.4 1.8c-.4-.2-.8-.3-1.1-.2l9.7 9.3zm0 2.2-9.7 9.3c.3.1.7 0 1.1-.2l11.2-6.4-2.6-2.7zm6.6-2.6-3-1.7-2.8 2.9 2.8 2.9 3-1.7c.9-.5.9-1.9 0-2.4z"/></svg><span><small>Get it on</small>Google Play</span></a>' +
      "</div>";
    document.body.appendChild(dlg);
    dlg.querySelector(".ccs-app-x").addEventListener("click", function () { dlg.close(); });
    dlg.addEventListener("click", function (e) { if (e.target === dlg) dlg.close(); });
    dlg.addEventListener("close", function () { document.documentElement.classList.remove("ccs-app-open"); if (opener) opener.focus(); });
  }
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a");
    if (!isApp(a) || e.metaKey || e.ctrlKey || e.shiftKey) return;
    if (!window.HTMLDialogElement) return;
    e.preventDefault();
    if (!dlg) build();
    opener = a;
    document.documentElement.classList.add("ccs-app-open");
    dlg.showModal();
    dlg.querySelector(".ccs-app-btn.is-main").focus();
  });
})();
