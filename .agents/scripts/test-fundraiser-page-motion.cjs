const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const html = fs.readFileSync('pages/fall-fundraiser.html', 'utf8');
const script = html.match(/<script id="fundraiser-page-motion">([\s\S]*?)<\/script>/)?.[1];
const css = html.match(/<style id="fundraiser-page-motion-style">([\s\S]*?)<\/style>/)?.[1];
assert.ok(script && css);
assert.ok(!css.includes('scaleY'), 'New motion must not alter the fundraising fill ratio.');
assert.ok(!script.includes('requestAnimationFrame'), 'No additional continuous JavaScript animation loop.');
assert.ok(css.includes('@media(prefers-reduced-motion:reduce)'));
assert.ok(css.includes('body.a11y-no-anim'));
const selectors = [...script.match(/var groups=\[([\s\S]*?)\];/)[1].matchAll(/'([^']+)'/g)].map(m => m[1]);
assert.equal(selectors.length, 5);
assert.ok(selectors.every(selector => !/footer|header|hero/.test(selector)));

function setup({ reduced = false, paused = false, supported = true, fail = false } = {}) {
  const nodes = [];
  const groups = new Map(selectors.map(selector => [selector, Array.from({ length: 7 }, () => {
    const classes = new Set(), styles = new Map();
    const node = {
      classList: { add: key => classes.add(key), remove: key => classes.delete(key), contains: key => classes.has(key) },
      style: { setProperty: (key, value) => styles.set(key, value), removeProperty: key => styles.delete(key) },
      classes, styles,
    };
    nodes.push(node);
    return node;
  })]));
  const root = {
    querySelectorAll: selector => selector === '.fundraiser-motion-in' ?
      nodes.filter(node => node.classes.has(selector.slice(1))) : groups.get(selector),
  };
  const media = { matches: reduced, addEventListener: (_, fn) => { media.change = fn; } };
  let bodyPaused = paused, bodyChange;
  const observers = [];
  class Observer {
    constructor(callback, options) {
      if (fail) throw new Error('Observer unavailable');
      this.callback = callback;
      this.observed = new Set();
      this.disconnected = false;
      assert.equal(options.rootMargin, '0px 0px -28px 0px');
      observers.push(this);
    }
    observe(node) { this.observed.add(node); }
    unobserve(node) { this.observed.delete(node); }
    disconnect() { this.disconnected = true; this.observed.clear(); }
  }
  const window = {
    matchMedia: () => media,
    MutationObserver: class {
      constructor(callback) { bodyChange = callback; }
      observe() {}
    },
  };
  if (supported) window.IntersectionObserver = Observer;
  const document = {
    querySelector: () => root,
    body: { classList: { contains: key => key === 'a11y-no-anim' && bodyPaused } },
  };
  vm.runInNewContext(script, { window, document });
  return {
    nodes, groups, media, observers,
    widget(value) { bodyPaused = value; bodyChange([{ attributeName: 'class' }]); },
  };
}

const page = setup();
assert.equal(page.observers[0].observed.size, 35);
assert.ok(page.nodes.every(node => node.classes.size === 0), 'Content is visible until actual intersection.');
const first = page.nodes[0], observer = page.observers[0];
observer.callback([{ target: first, isIntersecting: false }]);
assert.equal(first.classes.size, 0);
observer.callback([{ target: first, isIntersecting: true }]);
assert.ok(first.classes.has('fundraiser-motion-in'));
assert.ok(!observer.observed.has(first), 'Each card is unobserved after its first entrance.');
assert.equal(page.groups.get(selectors[0])[1].styles.get('--fundraiser-motion-delay'), '62ms');
assert.equal(page.groups.get(selectors[0])[6].styles.get('--fundraiser-motion-delay'), '310ms');

page.media.matches = true;
page.media.change();
assert.ok(observer.disconnected);
assert.equal(first.classes.size, 0, 'Reduced motion immediately resets any active entrance.');
assert.ok(!first.styles.has('--fundraiser-motion-delay'));
observer.callback([{ target: page.nodes[1], isIntersecting: true }]);
assert.equal(page.nodes[1].classes.size, 0, 'Queued callbacks cannot restart motion after it is disabled.');
page.media.matches = false;
page.media.change();
assert.equal(page.observers.length, 2);
observer.callback([{ target: first, isIntersecting: true }]);
assert.equal(first.classes.size, 0, 'A stale observer cannot restart a card after preferences change.');
page.observers[1].callback([{ target: first, isIntersecting: true }]);
assert.ok(first.classes.has('fundraiser-motion-in'));
page.widget(true);
assert.ok(page.observers[1].disconnected);
assert.equal(first.classes.size, 0);
page.widget(false);
assert.equal(page.observers.length, 3);

for (const options of [{ reduced: true }, { paused: true }, { supported: false }, { fail: true }]) {
  const quiet = setup(options);
  assert.equal(quiet.observers.length, 0);
  assert.ok(quiet.nodes.every(node => node.classes.size === 0));
}
console.log('PASS: progressive enhancement, one-time entrances, bounded stagger, live OS/widget controls, stale callbacks and no-observer/error fallbacks.');
