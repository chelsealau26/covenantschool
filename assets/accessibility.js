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

  /* ── HTML ── */
  var ICON_A11Y = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M12 2a2 2 0 1 1 0 4 2 2 0 0 1 0-4zm8.5 5.5l-5-.5-1.5-.5h-4l-1.5.5-5 .5a1 1 0 0 0 0 2l4-.4V12l-2.5 6.5a1 1 0 1 0 1.87.72L9 14h6l1.13 5.22a1 1 0 1 0 1.87-.72L15.5 12V9.1l4 .4a1 1 0 0 0 0-2z"/></svg>';

  var icons = {
    contrast: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3a9 9 0 1 0 0 18A9 9 0 0 0 12 3zm0 16V5a7 7 0 0 1 0 14z"/></svg>',
    grayscale: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2" fill="none"/><path d="M12 3v18" stroke="currentColor" stroke-width="2"/></svg>',
    links:    '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>',
    dyslexia: '<svg viewBox="0 0 24 24" aria-hidden="true"><text x="2" y="18" font-size="16" font-weight="bold" fill="currentColor">Aa</text></svg>',
    noAnim:   '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/><line x1="2" y1="2" x2="22" y2="22" stroke="currentColor" stroke-width="2"/></svg>',
    guide:    '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="2" y="10" width="20" height="4" rx="1"/><line x1="2" y1="7" x2="22" y2="7" stroke="currentColor" stroke-width="1.5" stroke-dasharray="3,2"/><line x1="2" y1="17" x2="22" y2="17" stroke="currentColor" stroke-width="1.5" stroke-dasharray="3,2"/></svg>',
  };

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
    '<div id="a11y-controls">' +
      '<div id="a11y-textsize-row">' +
        '<label for="a11y-inc">Text size</label>' +
        '<button class="a11y-size-btn" id="a11y-dec" aria-label="Decrease text size">A−</button>' +
        '<span id="a11y-size-val" aria-live="polite">100%</span>' +
        '<button class="a11y-size-btn" id="a11y-inc" aria-label="Increase text size">A+</button>' +
      '</div>' +
      '<button class="a11y-toggle" id="a11y-contrast"  aria-pressed="false">' + icons.contrast  + 'High<br>Contrast</button>' +
      '<button class="a11y-toggle" id="a11y-grayscale" aria-pressed="false">' + icons.grayscale + 'Grayscale</button>' +
      '<button class="a11y-toggle" id="a11y-links"     aria-pressed="false">' + icons.links     + 'Highlight<br>Links</button>' +
      '<button class="a11y-toggle" id="a11y-dyslexia"  aria-pressed="false">' + icons.dyslexia  + 'Readable<br>Font</button>' +
      '<button class="a11y-toggle" id="a11y-no-anim"   aria-pressed="false">' + icons.noAnim    + 'Pause<br>Motion</button>' +
      '<button class="a11y-toggle" id="a11y-guide"     aria-pressed="false">' + icons.guide     + 'Reading<br>Guide</button>' +
    '</div>';

  var trigger = document.createElement('button');
  trigger.id = 'a11y-btn';
  trigger.setAttribute('aria-label', 'Accessibility options');
  trigger.setAttribute('aria-expanded', 'false');
  trigger.setAttribute('aria-controls', 'a11y-panel');
  trigger.innerHTML = ICON_A11Y + '<span>Accessibility</span>';

  var guide = document.createElement('div');
  guide.id = 'a11y-guide';
  guide.setAttribute('aria-hidden', 'true');

  document.body.appendChild(trigger);
  document.body.appendChild(panel);
  document.body.appendChild(guide);

  /* ── Apply / render state ── */
  function applyAll() {
    /* text size */
    document.documentElement.style.fontSize = state.textSize + '%';
    document.getElementById('a11y-size-val').textContent = state.textSize + '%';

    /* toggles */
    applyToggle('highContrast', 'a11y-high-contrast', 'a11y-contrast');
    applyToggle('grayscale',    'a11y-grayscale',      'a11y-grayscale');
    applyToggle('links',        'a11y-links',          'a11y-links');
    applyToggle('dyslexia',     'a11y-dyslexia',       'a11y-dyslexia');
    applyToggle('noAnim',       'a11y-no-anim',        'a11y-no-anim');

    /* reading guide */
    guide.style.display = state.guide ? 'block' : 'none';
    var guideBtn = document.getElementById('a11y-guide');
    /* note: #a11y-guide is the ruler div; the button id is 'a11y-guide' in controls */
    var guideBtnEl = document.querySelector('#a11y-controls #a11y-guide');
    if (guideBtnEl) {
      guideBtnEl.classList.toggle('active', state.guide);
      guideBtnEl.setAttribute('aria-pressed', state.guide ? 'true' : 'false');
    }
  }

  function applyToggle(key, bodyClass, btnId) {
    document.body.classList.toggle(bodyClass, state[key]);
    var btn = document.getElementById(btnId);
    if (btn && btn.closest('#a11y-controls')) {
      btn.classList.toggle('active', state[key]);
      btn.setAttribute('aria-pressed', state[key] ? 'true' : 'false');
    }
  }

  /* ── Panel open/close ── */
  var panelOpen = false;
  function openPanel()  { panel.classList.add('open');    trigger.setAttribute('aria-expanded', 'true');  panelOpen = true; }
  function closePanel() { panel.classList.remove('open'); trigger.setAttribute('aria-expanded', 'false'); panelOpen = false; }

  trigger.addEventListener('click', function (e) {
    e.stopPropagation();
    panelOpen ? closePanel() : openPanel();
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && panelOpen) closePanel();
  });
  document.addEventListener('click', function (e) {
    if (panelOpen && !panel.contains(e.target) && e.target !== trigger) closePanel();
  });

  /* ── Text size ── */
  document.getElementById('a11y-inc').addEventListener('click', function () {
    if (state.textSize >= 150) return;
    state.textSize = Math.min(150, state.textSize + 10);
    applyAll(); save();
  });
  document.getElementById('a11y-dec').addEventListener('click', function () {
    if (state.textSize <= 80) return;
    state.textSize = Math.max(80, state.textSize - 10);
    applyAll(); save();
  });

  /* ── Toggle handlers ── */
  function makeToggle(btnId, key) {
    var el = document.getElementById(btnId);
    if (el && el.closest('#a11y-controls')) {
      el.addEventListener('click', function () {
        state[key] = !state[key];
        applyAll(); save();
      });
    }
  }
  makeToggle('a11y-contrast',  'highContrast');
  makeToggle('a11y-grayscale', 'grayscale');
  makeToggle('a11y-links',     'links');
  makeToggle('a11y-dyslexia',  'dyslexia');
  makeToggle('a11y-no-anim',   'noAnim');

  /* Guide button — use query selector to avoid ID collision with the ruler div */
  var guideBtnCtrl = document.querySelector('#a11y-controls button:last-child');
  if (guideBtnCtrl) {
    guideBtnCtrl.addEventListener('click', function () {
      state.guide = !state.guide;
      guide.style.display = state.guide ? 'block' : 'none';
      guideBtnCtrl.classList.toggle('active', state.guide);
      guideBtnCtrl.setAttribute('aria-pressed', state.guide ? 'true' : 'false');
      save();
    });
  }

  /* ── Reset ── */
  document.getElementById('a11y-panel-reset').addEventListener('click', function () {
    state = Object.assign({}, DEFAULTS);
    document.documentElement.style.fontSize = '';
    guide.style.display = 'none';
    applyAll(); save();
  });

  /* ── Reading guide follows mouse ── */
  document.addEventListener('mousemove', function (e) {
    if (state.guide) guide.style.top = (e.clientY - 20) + 'px';
  });

  /* ── Apply saved state on load ── */
  applyAll();

})();
