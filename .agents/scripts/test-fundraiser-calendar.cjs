const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const html = fs.readFileSync('pages/fall-fundraiser.html', 'utf8');
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
const script = scripts.find(match => match[1].includes("var dialog=document.getElementById('calendar-event-dialog')"))?.[1];
assert.ok(script, 'Calendar lightbox controller exists.');
const start = html.indexOf('<section class="recipe-section paper" id="dates">');
const end = html.indexOf('<dialog class="calendar-event-dialog"', start);
assert.ok(start >= 0 && end > start);
const calendar = html.slice(start, end);
const expectedKeys = ['kickoff', 'shirts', 'sponsor', 'weekly', 'grand', 'familyday'];

class Node {
  constructor(attrs = {}) {
    this.attrs = attrs;
    this.listeners = {};
    this.isConnected = true;
    this.textContent = '';
    const styles = new Map();
    this.style = {
      getPropertyValue: key => styles.get(key)?.value || '',
      getPropertyPriority: key => styles.get(key)?.priority || '',
      setProperty: (key, value, priority = '') => styles.set(key, { value, priority }),
      removeProperty: key => styles.delete(key),
    };
  }
  getAttribute(key) { return this.attrs[key]; }
  addEventListener(type, fn) { (this.listeners[type] ||= []).push(fn); }
  emit(type, event = {}) { (this.listeners[type] || []).forEach(fn => fn(event)); }
  focus() { focused = this; }
}
let focused;
const buttons = [...calendar.matchAll(/<button\b[^>]*data-event-key="[^"]+"[^>]*>/g)].map(match => {
  const attrs = Object.fromEntries([...match[0].matchAll(/([\w-]+)="([^"]*)"/g)].map(m => [m[1], m[2]]));
  assert.equal(attrs.type, 'button');
  assert.equal(attrs['aria-haspopup'], 'dialog');
  assert.equal(attrs['aria-controls'], 'calendar-event-dialog');
  return new Node(attrs);
});
assert.deepEqual(buttons.map(b => b.attrs['data-event-key']), expectedKeys);
const body = new Node(), root = new Node(), close = new Node();
const date = new Node(), title = new Node(), content = new Node(), shirt = new Node();
body.style.setProperty('overflow', 'auto', 'important');
content.replaceChildren = child => { content.child = child; };
content.querySelector = () => content.child?.key === 'shirts' ? shirt : null;
const dialog = new Node();
dialog.open = false;
dialog.querySelector = () => close;
dialog.showModal = () => { dialog.open = true; };
dialog.close = () => { dialog.open = false; dialog.emit('close'); };
dialog.getBoundingClientRect = () => ({ left: 100, top: 100, right: 600, bottom: 600 });
const ids = {
  'calendar-event-dialog': dialog, 'calendar-dialog-date': date,
  'calendar-dialog-title': title, 'calendar-dialog-content': content,
};
for (const key of expectedKeys) {
  assert.ok(html.includes(`<template id="calendar-detail-${key}">`));
  ids[`calendar-detail-${key}`] = { content: { cloneNode: () => ({ key }) } };
}
const window = {
  scrollY: 900, location: { hash: '' },
  scrollTo(x, y) { this.restoredScroll = [x, y]; },
};
const document = {
  body, documentElement: root,
  getElementById: id => ids[id],
  querySelectorAll(selector) {
    assert.equal(selector, '#dates .calendar-entry-button[data-event-key]');
    return buttons;
  },
  querySelector: () => ({ getAttribute: () => 'original-fundraiser-shirt-logo' }),
};
vm.runInNewContext(script, { document, window });
for (const button of buttons) {
  button.emit('click');
  assert.equal(dialog.open, true);
  assert.equal(title.textContent, button.attrs['data-event-title']);
  assert.equal(date.textContent, button.attrs['data-event-date']);
  assert.equal(content.child.key, button.attrs['data-event-key']);
  assert.equal(focused, close);
  assert.equal(body.style.getPropertyValue('overflow'), 'hidden');
  if (button.attrs['data-event-key'] === 'shirts') {
    assert.equal(shirt.src, 'original-fundraiser-shirt-logo');
  }
  close.emit('click');
  assert.equal(dialog.open, false);
  assert.equal(focused, button);
  assert.equal(content.child, undefined);
  assert.equal(body.style.getPropertyValue('overflow'), 'auto');
  assert.equal(body.style.getPropertyPriority('overflow'), 'important');
  assert.equal(root.style.getPropertyValue('overflow'), '');
  assert.deepEqual(window.restoredScroll, [0, 900]);
}
buttons[0].emit('click');
dialog.emit('click', { target: dialog, clientX: 200, clientY: 200 });
assert.equal(dialog.open, true, 'Clicking inside does not close the lightbox.');
dialog.emit('click', { target: dialog, clientX: 50, clientY: 50 });
assert.equal(dialog.open, false, 'Clicking the backdrop closes the lightbox.');
buttons[2].emit('click');
let prevented = false;
dialog.emit('click', {
  target: { closest: () => ({ getAttribute: () => '#sponsors' }) },
  preventDefault() { prevented = true; },
});
assert.equal(dialog.open, false);
assert.equal(window.location.hash, '#sponsors');
assert.equal(prevented, true);
console.log('PASS: all six calendar lightboxes, original content mappings, X/backdrop close, focus/scroll restoration, shirt artwork and sponsor anchor.');
