// On-page lightbox for (1) Square donation links and (2) documents marked with data-doc="Title"
// (PDFs and the Google Drive presentation). Without JavaScript, or with a modifier-click,
// links open normally. Documents use the lightbox only on computers: phone browsers can't
// show PDFs inside a page, so on phones those links keep opening in the phone's own viewer.
(function () {
  if (typeof HTMLDialogElement !== "function") return;
  var SQUARE = /^https:\/\/checkout\.square\.site\//i;
  var bigScreen = window.matchMedia ? matchMedia("(min-width: 768px) and (pointer: fine)") : { matches: true };
  var dialog, frame, newTab, title, loading, note, closeBtn, lastFocus;

  function build() {
    dialog = document.createElement("dialog");
    dialog.className = "ccs-donate";
    dialog.setAttribute("aria-labelledby", "ccs-donate-title");
    dialog.innerHTML =
      '<div class="ccs-donate-bar">' +
        '<h2 id="ccs-donate-title"></h2>' +
        '<a class="ccs-donate-newtab" target="_blank" rel="noopener">Open in a new tab</a>' +
        '<button type="button" class="ccs-donate-close">&times;</button>' +
      '</div>' +
      '<div class="ccs-donate-body"><p class="ccs-donate-loading"></p><iframe></iframe></div>' +
      '<p class="ccs-donate-note"></p>';
    document.body.appendChild(dialog);
    frame = dialog.querySelector("iframe");
    newTab = dialog.querySelector(".ccs-donate-newtab");
    title = dialog.querySelector("h2");
    loading = dialog.querySelector(".ccs-donate-loading");
    note = dialog.querySelector(".ccs-donate-note");
    closeBtn = dialog.querySelector(".ccs-donate-close");
    frame.addEventListener("load", function () { dialog.classList.add("is-loaded"); });
    closeBtn.addEventListener("click", close);
    newTab.addEventListener("click", function () { setTimeout(close, 0); });
    dialog.addEventListener("click", function (e) { if (e.target === dialog) close(); }); // backdrop
    dialog.addEventListener("close", function () {
      document.documentElement.classList.remove("ccs-donate-open");
      frame.removeAttribute("src"); // start fresh next time
      dialog.classList.remove("is-loaded");
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    });
  }

  function open(o) {
    if (!dialog) build();
    lastFocus = document.activeElement;
    dialog.classList.toggle("is-doc", o.kind === "doc");
    title.textContent = o.title;
    loading.innerHTML = o.loading;
    note.innerHTML = o.note;
    closeBtn.setAttribute("aria-label", "Close " + o.title);
    frame.title = o.frameTitle;
    if (o.kind === "donate") frame.setAttribute("allow", "payment *"); else frame.removeAttribute("allow");
    newTab.href = o.url;
    frame.src = o.embed || o.url;
    document.documentElement.classList.add("ccs-donate-open");
    dialog.showModal();
    closeBtn.focus();
  }
  function close() { if (dialog && dialog.open) dialog.close(); }

  // Google Drive "view" links embed through the /preview address.
  function embedUrl(url) {
    return url.replace(/^(https:\/\/drive\.google\.com\/file\/d\/[^/]+)\/view.*$/i, "$1/preview");
  }

  function stripNewTab(a) {
    var label = a.getAttribute("aria-label");
    if (label) a.setAttribute("aria-label", label.replace(/\s*\(opens in (a )?new tab\)/i, ""));
  }
  function prepLinks() {
    document.querySelectorAll('a[href^="https://checkout.square.site/"]').forEach(function (a) {
      a.removeAttribute("target");
      a.setAttribute("aria-haspopup", "dialog");
      stripNewTab(a);
    });
    if (bigScreen.matches) {
      document.querySelectorAll("a[data-doc]").forEach(function (a) {
        a.setAttribute("aria-haspopup", "dialog");
        stripNewTab(a);
      });
    }
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", prepLinks); else prepLinks();
  window.addEventListener("load", prepLinks);

  document.addEventListener("click", function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target.closest && e.target.closest("a[href]");
    if (!a || (dialog && dialog.contains(a))) return;
    if (SQUARE.test(a.href)) {
      e.preventDefault();
      open({ kind: "donate", url: a.href, title: "Make a Donation",
        frameTitle: "Covenant Christian School donation form (Square secure checkout)",
        loading: "Loading secure checkout&hellip;",
        note: "Secure checkout by Square. Trouble with the form? Use &ldquo;Open in a new tab.&rdquo;" });
    } else if (a.hasAttribute("data-doc") && bigScreen.matches) {
      e.preventDefault();
      var name = a.getAttribute("data-doc") || "Document";
      open({ kind: "doc", url: a.href, embed: embedUrl(a.href), title: name, frameTitle: name,
        loading: "Loading&hellip;",
        note: "To print or download, use &ldquo;Open in a new tab.&rdquo;" });
    }
  });
})();
