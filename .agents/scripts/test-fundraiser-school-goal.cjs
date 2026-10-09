const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const html = fs.readFileSync('pages/fall-fundraiser.html', 'utf8');
const script = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)]
  .find(match => match[1].includes('function validateProgress'))[1];
const config = JSON.parse(html.match(/id="fundraiser-school-progress">([\s\S]*?)<\/script>/)[1]);
assert.equal(config.goal, 80000);
assert.equal(config.raised, null);

function setup({ reduced = false, supplied = config } = {}) {
  class Node {
    constructor() { this.attrs = {}; this.style = {}; this.hidden = false; this.textContent = ''; }
    setAttribute(k, v) { this.attrs[k] = v; }
    removeAttribute(k) { delete this.attrs[k]; }
  }
  const illustration = new Node(), liquid = new Node(), amount = new Node();
  const total = new Node(), updated = new Node();
  const marks = Array.from({ length: 5 }, () => new Node());
  illustration.querySelector = selector => selector === '.goal-amount' ? amount : liquid;
  illustration.querySelectorAll = () => marks;
  let disabledByWidget = false, onBodyChange, onIntersect;
  const media = { matches: reduced, addEventListener: (_, callback) => media.change = callback };
  const frames = new Map();
  let id = 0;
  const errors = [];
  const window = { matchMedia: () => media };
  const context = {
    window, Intl, Date, Number, Object,
    document: {
      body: { classList: { contains: () => disabledByWidget } },
      querySelector: selector => {
        if (selector.includes('data-measuring-glass')) return illustration;
        if (selector.includes('data-school-goal-total')) return total;
        if (selector.includes('data-school-goal-date')) return updated;
      },
      getElementById: () => ({ textContent: JSON.stringify(supplied) }),
    },
    requestAnimationFrame: callback => { frames.set(++id, callback); return id; },
    cancelAnimationFrame: key => frames.delete(key),
    MutationObserver: class {
      constructor(callback) { onBodyChange = callback; }
      observe() {}
    },
    IntersectionObserver: class {
      constructor(callback) { onIntersect = callback; }
      observe() {}
      disconnect() {}
    },
    console: { error: (...args) => errors.push(args) },
  };
  vm.runInNewContext(script, context);
  function frame(time) {
    const pending = [...frames.values()];
    frames.clear();
    pending.forEach(callback => callback(time));
  }
  return {
    api: window.FundraiserSchoolGoal, illustration, liquid, amount, marks, total, updated,
    media, frames, errors, frame,
    enter: () => onIntersect([{ isIntersecting: true }]),
    widget: value => { disabledByWidget = value; onBodyChange(); },
  };
}

const page = setup();
assert.equal(page.amount.textContent, '$80,000');
assert.equal(page.total.textContent, 'Awaiting the first total');
assert.equal(page.illustration.attrs.role, 'img');
assert.equal(page.illustration.attrs['aria-valuenow'], undefined);
assert.equal(page.api.getFill(), 0);
assert.equal(page.frames.size, 0);
assert.deepEqual(page.marks.map(m => m.textContent), ['$80,000', '$60,000', '$40,000', '$20,000', '$0']);
page.enter();
page.api.update({ goal: 80000, raised: 20000, updatedAt: '2026-10-15' });
assert.equal(page.total.textContent, '$20,000 raised · 25% of our goal');
assert.equal(page.updated.textContent, 'Updated October 15, 2026');
assert.equal(page.illustration.attrs['aria-valuenow'], '20000');
page.frame(0); page.frame(2100);
assert(page.api.getFill() > 0 && page.api.getFill() < 0.25);
page.frame(4200);
assert.equal(page.api.getFill(), 0.25);
page.api.update({ goal: 80000, raised: 40000 });
page.frame(5000);
page.api.update({ goal: 80000, raised: 60000 });
assert.equal(page.frames.size, 1, 'Updating cancels the prior animation');
page.frame(6000); page.frame(10200);
assert.equal(page.api.getFill(), 0.75);
page.api.update({ goal: 80000, raised: 80000 });
page.media.matches = true; page.media.change();
assert.equal(page.api.getFill(), 1);
assert.equal(page.frames.size, 0);
page.api.update({ goal: 80000, raised: 100000 });
assert.equal(page.api.getFill(), 1);
assert.equal(page.total.textContent, '$100,000 raised · 125% of our goal');
assert.equal(page.illustration.attrs['aria-valuenow'], '80000');
page.api.update({ goal: 80000, raised: 0 });
assert.equal(page.total.textContent, '$0 raised · 0% of our goal');
assert.equal(page.illustration.attrs.role, 'progressbar');
assert.equal(page.api.getFill(), 0);
page.api.update({ goal: 80000, raised: 1 });
assert.equal(page.total.textContent, '$1 raised · <1% of our goal');
assert.equal(page.api.getFill(), 1 / 80000);
page.api.update({ goal: 100000, raised: 50000 });
assert.equal(page.amount.textContent, '$100,000');
assert.equal(page.api.getFill(), 0.5);
assert.equal(page.marks[1].textContent, '$75,000');
for (const invalid of [
  null, [], { goal: 0, raised: 0 }, { goal: 80000, raised: -1 },
  { goal: 80000, raised: '100' }, { goal: 80000 },
  { goal: Infinity, raised: 0 }, { goal: 80000, raised: NaN },
  { goal: 80000, raised: 1, updatedAt: '2026-02-29' },
  { goal: 80000, raised: null, updatedAt: '2026-10-15' },
  { goal: 80000, raised: 1, surprise: true },
]) assert.throws(() => page.api.update(invalid));
assert.equal(page.api.getState().raised, 50000, 'Bad data leaves confirmed progress intact');
page.api.update({ goal: 80000, raised: null });
assert.equal(page.api.getFill(), 0);
assert.equal(page.illustration.attrs['aria-valuenow'], undefined);
assert.equal(page.updated.hidden, true);
const reducedPage = setup({ reduced: true, supplied: { goal: 80000, raised: 20000 } });
assert.equal(reducedPage.api.getFill(), 0.25);
assert.equal(reducedPage.frames.size, 0);
const widgetPage = setup({ supplied: { goal: 80000, raised: 40000 } });
widgetPage.enter(); widgetPage.widget(true);
assert.equal(widgetPage.api.getFill(), 0.5);
assert.equal(widgetPage.frames.size, 0);
const badPage = setup({ supplied: { goal: 80000, raised: -1 } });
assert.equal(badPage.total.textContent, 'Fundraising total unavailable');
assert.equal(badPage.total.attrs.role, 'alert');
assert.equal(badPage.errors.length, 1);
assert.equal(page.errors.length, 0);
console.log('School goal: unknown/zero totals, proportional animation, updates, dates, changing goal, above-goal clamping, accessibility, reduced motion and invalid-data checks passed.');
