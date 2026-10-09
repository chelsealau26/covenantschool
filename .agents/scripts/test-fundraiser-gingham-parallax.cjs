const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

const html = fs.readFileSync('pages/fall-fundraiser.html', 'utf8');
const start = html.indexOf('<script id="fundraiser-gingham-parallax">');
assert.ok(start !== -1);
const codeStart = html.indexOf('>', start) + 1;
const code = html.slice(codeStart, html.indexOf('</script>', codeStart));
const frames = [];
const listeners = {};
const values = [];
const classes = new Set();
let observeClassChanges;
let motionChanged;
const motion = {
  matches: false,
  addEventListener(type, fn) {
    assert.equal(type, 'change');
    motionChanged = fn;
  },
};
let bounds = { top: 112, bottom: 732 };
const hero = {
  getBoundingClientRect: () => bounds,
  style: { setProperty: (key, value) => {
    assert.equal(key, '--gingham-scroll-offset');
    values.push(value);
  } },
};
const window = {
  scrollY: 0,
  innerHeight: 900,
  matchMedia(query) {
    assert.equal(query, '(prefers-reduced-motion: reduce)');
    return motion;
  },
  requestAnimationFrame(fn) { frames.push(fn); },
  addEventListener(type, fn, options) { listeners[type] = { fn, options }; },
};
const document = {
  querySelector(selector) {
    assert.equal(selector, '#main-content.recipe-page .recipe-hero');
    return hero;
  },
  body: { classList: { contains: name => classes.has(name) } },
};
class MutationObserver {
  constructor(fn) { observeClassChanges = fn; }
  observe(target, options) {
    assert.equal(target, document.body);
    assert.equal(options.attributes, true);
    assert.equal(options.attributeFilter.join(','), 'class');
  }
}
vm.runInNewContext(code, { window, document, MutationObserver });
const flush = () => { while (frames.length) frames.shift()(); };
flush();
assert.equal(values.at(-1), '0.00px');
assert.equal(listeners.scroll.options.passive, true);

window.scrollY = 100;
bounds = { top: 12, bottom: 632 };
for (let i = 0; i < 10; i++) listeners.scroll.fn();
assert.equal(frames.length, 1, 'Batch rapid scroll events into one animation frame.');
flush();
assert.equal(values.at(-1), '18.00px');
assert.ok(!hero.style.transform, 'Do not move the content or mascot.');

window.scrollY = 800;
bounds = { top: -688, bottom: -68 };
const oldCount = values.length;
listeners.scroll.fn();
flush();
assert.equal(values.length, oldCount, 'Skip offscreen background work.');

motion.matches = true;
motionChanged();
flush();
assert.equal(values.at(-1), '0.00px', 'Reset for OS reduced-motion preferences.');
motion.matches = false;
bounds = { top: -88, bottom: 532 };
window.scrollY = 200;
motionChanged();
flush();
assert.equal(values.at(-1), '36.00px');
classes.add('a11y-no-anim');
observeClassChanges();
flush();
assert.equal(values.at(-1), '0.00px', 'Respect the site animation-off toggle.');
classes.delete('a11y-no-anim');
observeClassChanges();
flush();
assert.equal(values.at(-1), '36.00px');
window.scrollY = 0;
listeners.pageshow.fn();
flush();
assert.equal(values.at(-1), '0.00px');
console.log('PASS: gingham scroll parallax, frame batching, offscreen skipping and both reduced-motion controls.');
