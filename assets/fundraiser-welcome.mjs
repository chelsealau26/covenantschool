import { hasEnded } from "./fundraiser-lifecycle.mjs";

const dialog = document.getElementById("fundraiser-welcome");
// Older versions remembered a dismissal for 7 days / the whole session under these keys.
// The popup now shows on every home page visit, so clear any leftovers.
const LEGACY_KEYS = [
  ["localStorage", "covenant:fundraiser-welcome:2026:until"],
  ["sessionStorage", "covenant:fundraiser-welcome:2026:seen"]
];

// Optional existing tracker only: never install a second tracker or wait for it.
const trackWelcome = (event, device, method) => {
  try {
    const data = { device };
    if (method) data.method = method;
    const result = window.umami?.track(event, data);
    // Some tracker versions return a promise; rejection must remain harmless.
    Promise.resolve(result).catch(() => {});
  } catch { /* Analytics cannot interrupt the popup or navigation. */ }
};

if (dialog) {
  LEGACY_KEYS.forEach(([storage, key]) => { try { window[storage].removeItem(key); } catch {} });

  let timer;
  let interrupted = false;
  let shown = false;
  let previousFocus;
  let scrollState;
  let retired = false;
  // Only stops the popup from reopening during the same page view.
  // Every new visit to the home page (link, typed URL, refresh, Back/Forward) shows it again.
  let memorySuppressed = false;
  let eventDevice;
  let outcomeRecorded = false;
  const recordOutcome = (event, method) => {
    if (!shown || !dialog.open || retired || outcomeRecorded) return;
    outcomeRecorded = true;
    trackWelcome(event, eventDevice, method);
  };
  const suppress = () => { memorySuppressed = true; };
  const isSuppressed = () => memorySuppressed;
  const eligible = () => /^\/(?:(?:pages\/)?index(?:\.html)?)?\/?$/i.test(location.pathname) && !location.hash;
  const visible = element => !!element.getClientRects().length &&
    getComputedStyle(element).visibility !== "hidden" && getComputedStyle(element).display !== "none" &&
    Number(getComputedStyle(element).opacity) !== 0;
  const busy = () => {
    const active = document.activeElement;
    if (active && active !== document.body && active !== document.documentElement) return true;
    return [...document.querySelectorAll(
      'dialog[open], [role="dialog"], [aria-modal="true"], [aria-expanded="true"], #a11y-panel, .cookies-disclaimer, .cookie-consent, #tmdp-simple-lightbox, #portfolio-popup'
    )].some(element => element !== dialog && visible(element));
  };
  const renderProgress = () => {
    try {
      const data = JSON.parse(document.getElementById("fundraiser-school-progress").textContent);
      const raised = Number(data.raised);
      const goal = Number(data.goal);
      if (!Number.isFinite(raised) || raised < 0 || !Number.isFinite(goal) || goal <= 0) return false;
      const percent = Math.round(raised / goal * 100);
      const money = new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 });
      dialog.querySelector("[data-welcome-raised]").textContent = money.format(raised);
      dialog.querySelector("[data-welcome-goal]").textContent = money.format(goal);
      dialog.querySelector("[data-welcome-percent]").textContent = `${percent}%`;
      const meter = dialog.querySelector('[role="progressbar"]');
      meter.setAttribute("aria-valuenow", String(Math.min(raised, goal)));
      meter.setAttribute("aria-valuemax", String(goal));
      meter.setAttribute("aria-valuetext", `${money.format(raised)} raised toward ${money.format(goal)}; ${percent}% of goal`);
      meter.style.setProperty("--welcome-progress", `${Math.min(percent, 100)}%`);
      return true;
    } catch { return false; } // Do not show independently maintained stale totals.
  };
  const lockScroll = () => {
    const body = document.body;
    const keys = ["position", "top", "left", "width", "overflow", "padding-right"];
    scrollState = {
      x: window.scrollX, y: window.scrollY,
      styles: keys.map(key => [key, body.style.getPropertyValue(key), body.style.getPropertyPriority(key)]),
      rootBehavior: document.documentElement.style.getPropertyValue("scroll-behavior"),
      rootPriority: document.documentElement.style.getPropertyPriority("scroll-behavior")
    };
    const gutter = window.innerWidth - document.documentElement.clientWidth;
    const padding = parseFloat(getComputedStyle(body).paddingRight) || 0;
    body.style.setProperty("position", "fixed");
    body.style.setProperty("top", `${-scrollState.y}px`);
    body.style.setProperty("left", `${-scrollState.x}px`);
    body.style.setProperty("width", "100%");
    body.style.setProperty("overflow", "hidden");
    if (gutter > 0) body.style.setProperty("padding-right", `${padding + gutter}px`);
  };
  const restore = () => {
    if (scrollState) {
      const state = scrollState;
      scrollState = null;
      state.styles.forEach(([key, value, priority]) => {
        if (value) document.body.style.setProperty(key, value, priority);
        else document.body.style.removeProperty(key);
      });
      document.documentElement.style.setProperty("scroll-behavior", "auto", "important");
      window.scrollTo(state.x, state.y);
      if (state.rootBehavior) document.documentElement.style.setProperty("scroll-behavior", state.rootBehavior, state.rootPriority);
      else document.documentElement.style.removeProperty("scroll-behavior");
    }
    if (previousFocus?.isConnected && typeof previousFocus.focus === "function") previousFocus.focus({ preventScroll: true });
    previousFocus = null;
  };
  const dismiss = () => {
    clearTimeout(timer);
    suppress();
    if (dialog.open) dialog.close();
    restore(); // Native close events are queued; expiry cleanup must be synchronous.
  };
  const retire = () => {
    retired = true;
    dismiss();
    dialog.remove();
  };
  document.addEventListener("fundraiser:ended", retire);
  dialog.addEventListener("close", () => { suppress(); restore(); });
  dialog.addEventListener("cancel", event => {
    event.preventDefault();
    recordOutcome("fundraiser_popup_dismiss", "escape");
    dismiss();
  });
  dialog.addEventListener("keydown", event => {
    if (event.key !== "Tab") return;
    const controls = [...dialog.querySelectorAll('a[href], button:not([disabled]), [tabindex="0"]')].filter(visible);
    const first = controls[0], last = controls.at(-1);
    if ((event.shiftKey && document.activeElement === first) ||
        (!event.shiftKey && document.activeElement === last)) {
      event.preventDefault();
      (event.shiftKey ? last : first)?.focus();
    }
  });
  dialog.querySelectorAll("[data-welcome-dismiss]").forEach(button => button.addEventListener("click", () => {
    recordOutcome("fundraiser_popup_dismiss", button.classList.contains("welcome-close") ? "close" : "continue");
    dismiss();
  }));
  dialog.querySelector(".welcome-cta").addEventListener("click", () => {
    recordOutcome("fundraiser_popup_click");
    dismiss();
  });

  const stop = () => { interrupted = true; clearTimeout(timer); };
  const interaction = event => {
    if (shown || dialog.contains(event.target)) return;
    if (event.type === "keydown" || event.type === "focusin" ||
      event.target.closest?.('a, button, input, select, textarea, nav, form, [role="button"], [role="dialog"], [contenteditable]')) stop();
  };
  ["keydown", "pointerdown", "focusin"].forEach(type => document.addEventListener(type, interaction, true));
  window.addEventListener("hashchange", stop);
  window.addEventListener("popstate", stop);
  window.addEventListener("pagehide", () => { stop(); if (dialog.open) dismiss(); });

  const schedule = () => {
    clearTimeout(timer);
    if (hasEnded()) { retire(); return; }
    if (retired || shown || interrupted || !eligible() || isSuppressed() || document.hidden ||
      typeof dialog.showModal !== "function") return;
    timer = setTimeout(() => {
      if (hasEnded()) { retire(); return; }
      if (retired || shown || interrupted || !eligible() || isSuppressed() || document.hidden) return;
      if (busy() || !renderProgress()) { stop(); return; }
      previousFocus = document.activeElement;
      try {
        lockScroll();
        dialog.showModal();
        shown = true;
        suppress(); // Don't reopen during this same page view.
        dialog.querySelector(".welcome-close").focus({ preventScroll: true });
        eventDevice = window.matchMedia("(max-width: 767px)").matches ? "mobile" : "desktop";
        trackWelcome("fundraiser_popup_impression", eventDevice);
      } catch { restore(); stop(); }
    }, 500);
  };

  // Coming back with Back/Forward restores the page from the browser's cache without reloading it.
  // Treat that as a new visit so the popup shows again.
  window.addEventListener("pageshow", event => {
    if (!event.persisted || retired) return;
    if (dialog.open) dismiss();
    shown = false;
    interrupted = false;
    memorySuppressed = false;
    outcomeRecorded = false;
    schedule();
  });
  document.addEventListener("visibilitychange", () => {
    if (hasEnded()) retire();
    else if (document.hidden) clearTimeout(timer);
    else schedule();
  });
  if (hasEnded()) retire();
  else if (document.readyState !== "loading") schedule();
  else document.addEventListener("DOMContentLoaded", schedule, { once: true });
}
