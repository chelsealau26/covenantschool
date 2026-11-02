// Opens Square donation links in an on-page lightbox instead of a new tab.
// Without JavaScript (or with a modifier-click) the link still opens Square normally.
(function () {
  if (typeof HTMLDialogElement !== "function") return;
  var SQUARE = /^https:\/\/checkout\.square\.site\//i;
  var dialog, frame, newTab, lastFocus;

  function build() {
    dialog = document.createElement("dialog");
    dialog.className = "ccs-donate";
    dialog.setAttribute("aria-labelledby", "ccs-donate-title");
    dialog.innerHTML =
      '<div class="ccs-donate-bar">' +
        '<h2 id="ccs-donate-title">Make a Donation</h2>' +
        '<a class="ccs-donate-newtab" target="_blank" rel="noopener">Open in a new tab</a>' +
        '<button type="button" class="ccs-donate-close" aria-label="Close donation form">&times;</button>' +
      '</div>' +
      '<div class="ccs-donate-body"><p class="ccs-donate-loading">Loading secure checkout&hellip;</p>' +
        '<iframe title="Covenant Christian School donation form (Square secure checkout)" allow="payment *"></iframe></div>' +
      '<p class="ccs-donate-note">Secure checkout by Square. Trouble with the form? Use &ldquo;Open in a new tab.&rdquo;</p>';
    document.body.appendChild(dialog);
    frame = dialog.querySelector("iframe");
    newTab = dialog.querySelector(".ccs-donate-newtab");
    frame.addEventListener("load", function () { dialog.classList.add("is-loaded"); });
    dialog.querySelector(".ccs-donate-close").addEventListener("click", close);
    newTab.addEventListener("click", function () { setTimeout(close, 0); });
    dialog.addEventListener("click", function (e) { if (e.target === dialog) close(); }); // backdrop
    dialog.addEventListener("close", function () {
      document.documentElement.classList.remove("ccs-donate-open");
      frame.removeAttribute("src"); // start fresh next time
      dialog.classList.remove("is-loaded");
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    });
  }

  function open(url) {
    if (!dialog) build();
    lastFocus = document.activeElement;
    newTab.href = url;
    frame.src = url;
    document.documentElement.classList.add("ccs-donate-open");
    dialog.showModal();
    dialog.querySelector(".ccs-donate-close").focus();
  }
  function close() { if (dialog && dialog.open) dialog.close(); }

  document.addEventListener("click", function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target.closest && e.target.closest("a[href]");
    if (!a || !SQUARE.test(a.href) || (dialog && dialog.contains(a))) return;
    e.preventDefault();
    open(a.href);
  });
})();
