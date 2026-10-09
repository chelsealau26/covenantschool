const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const html = fs.readFileSync('pages/fall-fundraiser.html', 'utf8');
const section = html.slice(html.indexOf('id="sponsors"'), html.indexOf('id="faq"'));
const script = [...section.matchAll(/<script>([\s\S]*?)<\/script>/g)]
  .find(match => match[1].includes('function initSponsorTicker'))[1];

class Element {
  constructor() {
    this.attributes = {};
    this.listeners = {};
    this.children = [];
    this.classes = new Set();
    this.classList = {
      add: (...names) => names.forEach(name => this.classes.add(name)),
      remove: (...names) => names.forEach(name => this.classes.delete(name)),
      contains: name => this.classes.has(name),
      toggle: (name, value) => value ? this.classes.add(name) : this.classes.delete(name),
    };
    this.style = {
      setProperty: (name, value) => this.style[name] = value,
      removeProperty: name => delete this.style[name],
    };
  }
  setAttribute(name, value) { this.attributes[name] = value; }
  addEventListener(name, handler) { this.listeners[name] = handler; }
  fire(name, event = {}) { this.listeners[name]?.(event); }
  appendChild(child) { child.parentNode = this; this.children.push(child); }
  removeChild(child) {
    this.children = this.children.filter(node => node !== child);
    child.parentNode = null;
  }
  cloneNode() {
    const clone = new Element();
    clone.links = Array.from({ length: 5 }, () => new Element());
    clone.querySelectorAll = selector => selector === 'a' ? clone.links : [];
    return clone;
  }
}

const root = new Element(), track = new Element(), canonical = new Element();
const control = new Element(), body = new Element(), doc = new Element();
canonical.width = 970;
canonical.getBoundingClientRect = () => ({ width: canonical.width });
track.appendChild(canonical);
track.querySelector = () => canonical;
root.querySelector = selector => ({
  '.sponsor-ticker-track': track,
  '.sponsor-ticker-control': control,
})[selector];
root.contains = node => node === control;
doc.body = body;
doc.hidden = false;
doc.querySelector = () => root;
const motion = { matches: false, addEventListener: (_, handler) => motion.change = handler };
let bodyChanged;
const win = {
  matchMedia: () => motion,
  addEventListener: () => {},
  MutationObserver: class {
    constructor(handler) { bodyChanged = handler; }
    observe() {}
  },
};
vm.runInNewContext(script, { window: win, document: doc });
const api = win.FundraiserSponsorTicker.controller;
assert(root.classList.contains('sponsor-ticker-ready'));
assert.equal(control.hidden, false);
assert.equal(track.children.length, 2);
assert.equal(api.clone.attributes['aria-hidden'], 'true');
assert.equal(api.clone.attributes.inert, undefined);
assert(api.clone.links.every(link => link.attributes.tabindex === '-1'));
assert.equal(track.style['--sponsor-ticker-duration'], '30.3125s');
control.fire('click');
assert.equal(track.style.animationPlayState, 'paused');
assert.equal(control.attributes['aria-pressed'], 'true');
control.fire('click');
assert.equal(track.style.animationPlayState, '');
root.fire('mouseenter');
assert.equal(track.style.animationPlayState, 'paused');
root.fire('mouseleave');
assert.equal(track.style.animationPlayState, '');
root.fire('focusin');
assert.equal(track.style.animationPlayState, 'paused');
root.fire('focusout', { relatedTarget: null });
assert.equal(track.style.animationPlayState, '');
doc.hidden = true; doc.fire('visibilitychange');
assert.equal(track.style.animationPlayState, 'paused');
doc.hidden = false; doc.fire('visibilitychange');
assert.equal(track.style.animationPlayState, '');
motion.matches = true; motion.change();
assert.equal(control.hidden, true);
assert.equal(track.children.length, 1);
assert.equal(api.clone, null);
motion.matches = false; motion.change();
assert.equal(track.children.length, 2);
body.classList.add('a11y-no-anim'); bodyChanged();
assert.equal(control.hidden, true);
assert.equal(track.children.length, 1);
body.classList.remove('a11y-no-anim'); bodyChanged();
assert.equal(track.children.length, 2);
canonical.width = 2000; api.refreshSpeed();
assert.equal(track.style['--sponsor-ticker-duration'], '62.5s');
console.log('Sponsor ticker: pause/resume, hover, keyboard, visibility, reduced motion, accessibility setting, clone links and duration passed.');
