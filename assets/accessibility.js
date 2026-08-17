/* ============================================================
   Covenant School — Accessibility Widget
   ============================================================ */
(function () {
  'use strict';

  /* ── Load Lexend font for dyslexia mode ── */
  var lexendLink = document.createElement('link');
  lexendLink.rel  = 'stylesheet';
  lexendLink.href = 'https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;500;600;700&display=swap';
  document.head.appendChild(lexendLink);

  /* ── State ── */
  var DEFAULTS = { textSize: 100, highContrast: false, grayscale: false,
                   links: false, dyslexia: false, noAnim: false, guide: false };
  var state = Object.assign({}, DEFAULTS);
  try {
    var saved = JSON.parse(localStorage.getItem('ccs_a11y') || 'null');
    if (saved) state = Object.assign({}, DEFAULTS, saved);
  } catch (e) {}

  function save() {
    try { localStorage.setItem('ccs_a11y', JSON.stringify(state)); } catch (e) {}
  }

  /* ── Icons ── */
  var ICON_A11Y = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a2 2 0 1 1 0 4 2 2 0 0 1 0-4zm8.5 5.5l-5-.5-1.5-.5h-4l-1.5.5-5 .5a1 1 0 0 0 0 2l4-.4V12l-2.5 6.5a1 1 0 1 0 1.87.72L9 14h6l1.13 5.22a1 1 0 1 0 1.87-.72L15.5 12V9.1l4 .4a1 1 0 0 0 0-2z"/></svg>';

  var icons = {
    contrast:  '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3a9 9 0 1 0 0 18A9 9 0 0 0 12 3zm0 16V5a7 7 0 0 1 0 14z"/></svg>',
    grayscale: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="8" stroke="currentColor" stroke-width="2" fill="none"/><path d="M12 4v16M8.5 6.5l7 11M6.5 8.5l11 7" stroke="currentColor" stroke-width="1.2" opacity=".5"/></svg>',
    links:     '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>',
    dyslexia:  '<svg viewBox="0 0 24 24" aria-hidden="true"><text x="2" y="17" font-size="14" font-weight="700" fill="currentColor" font-family="Arial">Aa</text></svg>',
    noAnim:    '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" fill="currentColor"/><line x1="2" y1="2" x2="22" y2="22" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    guide:     '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="9" width="20" height="6" rx="2" fill="currentColor" opacity=".2"/><line x1="2" y1="9" x2="22" y2="9" stroke-dasharray="3 2"/><line x1="2" y1="15" x2="22" y2="15" stroke-dasharray="3 2"/></svg>',
  };

  /* ── Build panel HTML ── */
  var panel = document.createElement('div');
  panel.id = 'a11y-panel';
  panel.setAttribute('role', 'dialog');
  panel.setAttribute('aria-modal', 'true');
  panel.setAttribute('aria-label', 'Accessibility Options');
  panel.innerHTML =
    '<div id="a11y-panel-header">' +
      '<span>Accessibility Options</span>' +
      '<button id="a11y-panel-reset" aria-label="Reset all accessibility settings">Reset</button>' +
    '</div>' +
    '<div id="a11y-textsize-row">' +
      '<label>Text size</label>' +
      '<button class="a11y-size-btn" id="a11y-dec" aria-label="Decrease text size">A−</button>' +
      '<span id="a11y-size-val" aria-live="polite">100%</span>' +
      '<button class="a11y-size-btn" id="a11y-inc" aria-label="Increase text size">A+</button>' +
    '</div>' +
    '<div id="a11y-grid">' +
      '<button class="a11y-toggle" id="a11y-btn-contrast"  aria-pressed="false">' + icons.contrast  + 'High<br>Contrast</button>' +
      '<button class="a11y-toggle" id="a11y-btn-grayscale" aria-pressed="false">' + icons.grayscale + 'Grayscale</button>' +
      '<button class="a11y-toggle" id="a11y-btn-links"     aria-pressed="false">' + icons.links     + 'Highlight<br>Links</button>' +
      '<button class="a11y-toggle" id="a11y-btn-dyslexia"  aria-pressed="false">' + icons.dyslexia  + 'Readable<br>Font</button>' +
      '<button class="a11y-toggle" id="a11y-btn-noanim"    aria-pressed="false">' + icons.noAnim    + 'Pause<br>Motion</button>' +
      '<button class="a11y-toggle" id="a11y-btn-guide"     aria-pressed="false">' + icons.guide     + 'Reading<br>Guide</button>' +
    '</div>';

  /* ── Trigger button ── */
  var trigger = document.createElement('button');
  trigger.id = 'a11y-btn';
  trigger.setAttribute('aria-label', 'Accessibility options');
  trigger.setAttribute('aria-expanded', 'false');
  trigger.setAttribute('aria-controls', 'a11y-panel');
  trigger.innerHTML = ICON_A11Y + '<span>Accessibility</span>';

  /* ── Reading ruler (separate div, no ID collision) ── */
  var ruler = document.createElement('div');
  ruler.id = 'a11y-ruler';
  ruler.setAttribute('aria-hidden', 'true');

  document.body.appendChild(trigger);
  document.body.appendChild(panel);
  document.body.appendChild(ruler);

  /* ── Apply state ── */
  function applyAll() {
    document.documentElement.style.fontSize = state.textSize + '%';
    document.getElementById('a11y-size-val').textContent = state.textSize + '%';

    setToggle('highContrast', 'a11y-high-contrast', 'a11y-btn-contrast');
    setToggle('grayscale',    'a11y-grayscale',      'a11y-btn-grayscale');
    setToggle('links',        'a11y-links',          'a11y-btn-links');
    setToggle('dyslexia',     'a11y-dyslexia',       'a11y-btn-dyslexia');
    setToggle('noAnim',       'a11y-no-anim',        'a11y-btn-noanim');

    ruler.style.display = state.guide ? 'block' : 'none';
    var gbtn = document.getElementById('a11y-btn-guide');
    if (gbtn) {
      gbtn.classList.toggle('active', state.guide);
      gbtn.setAttribute('aria-pressed', state.guide ? 'true' : 'false');
    }
  }

  function setToggle(key, bodyClass, btnId) {
    document.body.classList.toggle(bodyClass, state[key]);
    var btn = document.getElementById(btnId);
    if (btn) {
      btn.classList.toggle('active', state[key]);
      btn.setAttribute('aria-pressed', state[key] ? 'true' : 'false');
    }
  }

  /* ── Open / close ── */
  var panelOpen = false;
  function openPanel()  { panel.classList.add('open');    trigger.setAttribute('aria-expanded', 'true');  panelOpen = true; }
  function closePanel() { panel.classList.remove('open'); trigger.setAttribute('aria-expanded', 'false'); panelOpen = false; }

  trigger.addEventListener('click', function (e) { e.stopPropagation(); panelOpen ? closePanel() : openPanel(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && panelOpen) closePanel(); });
  document.addEventListener('click',   function (e) { if (panelOpen && !panel.contains(e.target) && e.target !== trigger) closePanel(); });

  /* ── Text size ── */
  document.getElementById('a11y-inc').addEventListener('click', function () {
    state.textSize = Math.min(150, state.textSize + 10); applyAll(); save();
  });
  document.getElementById('a11y-dec').addEventListener('click', function () {
    state.textSize = Math.max(80, state.textSize - 10); applyAll(); save();
  });

  /* ── Toggle handlers ── */
  [
    ['a11y-btn-contrast',  'highContrast'],
    ['a11y-btn-grayscale', 'grayscale'],
    ['a11y-btn-links',     'links'],
    ['a11y-btn-dyslexia',  'dyslexia'],
    ['a11y-btn-noanim',    'noAnim'],
  ].forEach(function (pair) {
    document.getElementById(pair[0]).addEventListener('click', function () {
      state[pair[1]] = !state[pair[1]]; applyAll(); save();
    });
  });

  document.getElementById('a11y-btn-guide').addEventListener('click', function () {
    state.guide = !state.guide; applyAll(); save();
  });

  /* ── Reset ── */
  document.getElementById('a11y-panel-reset').addEventListener('click', function () {
    state = Object.assign({}, DEFAULTS);
    document.documentElement.style.fontSize = '';
    applyAll(); save();
  });

  /* ── Reading ruler follows cursor ── */
  document.addEventListener('mousemove', function (e) {
    if (state.guide) ruler.style.top = (e.clientY - 22) + 'px';
  });

  applyAll();
})();
