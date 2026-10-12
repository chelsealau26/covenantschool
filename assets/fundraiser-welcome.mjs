import { hasEnded } from "./fundraiser-lifecycle.mjs";

const dialog = document.getElementById("fundraiser-welcome");
const STORAGE_KEY = "covenant:fundraiser-welcome:2026:until";
const SESSION_KEY = "covenant:fundraiser-welcome:2026:seen";
const WEEK = 7 * 24 * 60 * 60 * 1000;

if (dialog) {
  let timer;
  let interrupted = false;
  let shown = false;
  let previousFocus;
  let scrollState;
  let retired = false;
  let memorySuppressed = false;
  const read = (storage, key) => {
    try { return window[storage].getItem(key); } catch { return null; }
  };
  const write = (storage, key, value) => {
    try { window[storage].setItem(key, value); } catch {
      // Session + memory still prevent repeat prompts where available.
      // Blocked/cleared storage cannot guarantee suppression across visits.
    }
  };
  const suppress = (persist = false) => {
    memorySuppressed = true;
    write("sessionStorage", SESSION_KEY, "1");
    if (persist) write("localStorage", STORAGE_KEY, String(Date.now() + WEEK));
  };
  const isSuppressed = () => memorySuppressed ||
    read("sessionStorage", SESSION_KEY) === "1" ||
    Number(read("localStorage", STORAGE_KEY)) > Date.now();
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
  const dismiss = (persist = true) => {
    clearTimeout(timer);
    suppress(persist);
    if (dialog.open) dialog.close();
    restore(); // Native close events are queued; expiry cleanup must be synchronous.
  };
  const retire = () => {
    retired = true;
    dismiss(false);
    dialog.remove();
  };
  document.addEventListener("fundraiser:ended", retire);
  dialog.addEventListener("close", () => { suppress(!retired); restore(); });
  dialog.addEventListener("cancel", event => { event.preventDefault(); dismiss(); });
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
  dialog.querySelectorAll("[data-welcome-dismiss]").forEach(button => button.addEventListener("click", () => dismiss()));
  dialog.querySelector(".welcome-cta").addEventListener("click", () => dismiss());

  const stop = () => { interrupted = true; clearTimeout(timer); };
  const interaction = event => {
    if (shown || dialog.contains(event.target)) return;
    if (event.type === "keydown" || event.type === "focusin" ||
      event.target.closest?.('a, button, input, select, textarea, nav, form, [role="button"], [role="dialog"], [contenteditable]')) stop();
  };
  ["keydown", "pointerdown", "focusin"].forEach(type => document.addEventListener(type, interaction, true));
  window.addEventListener("hashchange", stop);
  window.addEventListener("popstate", stop);
  window.addEventListener("pagehide", () => { stop(); if (dialog.open) dismiss(false); });
  window.addEventListener("pageshow", event => { if (event.persisted) { stop(); if (dialog.open) dismiss(false); } });

  const schedule = () => {
    clearTimeout(timer);
    if (hasEnded()) { retire(); return; }
    if (retired || shown || interrupted || !eligible() || isSuppressed() || document.hidden ||
      typeof dialog.showModal !== "function" || performance.getEntriesByType("navigation")[0]?.type === "back_forward") return;
    timer = setTimeout(() => {
      if (hasEnded()) { retire(); return; }
      if (retired || shown || interrupted || !eligible() || isSuppressed() || document.hidden) return;
      if (busy() || !renderProgress()) { stop(); return; }
      previousFocus = document.activeElement;
      try {
        lockScroll();
        dialog.showModal();
        shown = true;
        suppress(); // Never reopen in this session, including browser back.
        dialog.querySelector(".welcome-close").focus({ preventScroll: true });
      } catch { restore(); stop(); }
    }, 2000);
  };
  document.addEventListener("visibilitychange", () => {
    if (hasEnded()) retire();
    else if (document.hidden) clearTimeout(timer);
    else schedule();
  });
  if (hasEnded()) retire();
  else if (document.readyState === "complete") schedule();
  else window.addEventListener("load", schedule, { once: true });
}
