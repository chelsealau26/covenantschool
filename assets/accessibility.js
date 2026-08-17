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

  /* ── Icons ──
     Trigger button: stroke-based wheelchair (Tabler Icons style)
     Panel toggles:  fill-based shapes                              */

  /* Wheelchair: head circle + seat/back path + two wheel circles */
  var ICON_A11Y =
    '<svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"' +
    ' stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    '<circle cx="7" cy="19" r="2"/>' +        /* rear wheel   */
    '<circle cx="17" cy="17" r="2"/>' +       /* front caster */
    '<circle cx="5" cy="6" r="1.5" stroke-width="1.5"/>' +  /* head */
    /* seat-back → seat → arm extending to hand-rim */
    '<path d="M5 7.5V14a1 1 0 0 0 1 1h5.5l2.5 2"/>' +
    /* footrest bar */
    '<path d="M6 14h4"/>' +
    /* push-rim / arm reaching wheel */
    '<path d="M9 12l3.5-4"/>' +
    '</svg>';

  var icons = {
    contrast:  '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3a9 9 0 1 0 0 18A9 9 0 0 0 12 3zm0 16V5a7 7 0 0 1 0 14z"/></svg>',
    grayscale: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3a9 9 0 1 0 0 18A9 9 0 0 0 12 3zm0 2v14a7 7 0 0 1 0-14z"/><line x1="12" y1="3" x2="12" y2="21" stroke="currentColor" stroke-width="1.5"/></svg>',
    links:     '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>',
    dyslexia:  '<svg viewBox="0 0 24 24" aria-hidden="true"><text x="2" y="17" font-size="14" font-weight="700" fill="currentColor" font-family="Arial,sans-serif">Aa</text></svg>',
    noAnim:    '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/><line x1="2" y1="2" x2="22" y2="22" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    guide:     '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="2" y="9" width="20" height="6" rx="2" fill="currentColor" opacity=".15" stroke="none"/><line x1="2" y1="9" x2="22" y2="9" stroke-dasharray="4 2"/><line x1="2" y1="15" x2="22" y2="15" stroke-dasharray="4 2"/></svg>',
  };

  /* ── Build panel ── */
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
  trigger.innerHTML = ICON_A11Y;

  /* ── Reading ruler (separate ID, no collision with button) ── */
  var ruler = document.createElement('div');
  ruler.id = 'a11y-ruler';
  ruler.setAttribute('aria-hidden', 'true');

  document.body.appendChild(trigger);
  document.body.appendChild(panel);
  document.body.appendChild(ruler);

  /* ── Apply text size via CSS zoom (works on px-based pages) ── */
  function applyTextSize() {
    var scale = state.textSize / 100;
    if (scale === 1) {
      document.body.style.zoom = '';
      document.documentElement.style.fontSize = '';
    } else {
      document.body.style.zoom = scale;
      document.documentElement.style.fontSize = state.textSize + '%';
    }
    document.getElementById('a11y-size-val').textContent = state.textSize + '%';
  }

  /* ── Apply all state ── */
  function applyAll() {
    applyTextSize();
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

  /* ── Text size buttons ── */
  document.getElementById('a11y-inc').addEventListener('click', function () {
    if (state.textSize < 150) { state.textSize = Math.min(150, state.textSize + 10); applyAll(); save(); }
  });
  document.getElementById('a11y-dec').addEventListener('click', function () {
    if (state.textSize > 80) { state.textSize = Math.max(80, state.textSize - 10); applyAll(); save(); }
  });

  /* ── Toggle handlers ── */
  [
    ['a11y-btn-contrast',  'highContrast'],
    ['a11y-btn-grayscale', 'grayscale'],
    ['a11y-btn-links',     'links'],
    ['a11y-btn-dyslexia',  'dyslexia'],
    ['a11y-btn-noanim',    'noAnim'],
    ['a11y-btn-guide',     'guide'],
  ].forEach(function (pair) {
    document.getElementById(pair[0]).addEventListener('click', function () {
      state[pair[1]] = !state[pair[1]]; applyAll(); save();
    });
  });

  /* ── Reset ── */
  document.getElementById('a11y-panel-reset').addEventListener('click', function () {
    state = Object.assign({}, DEFAULTS);
    document.documentElement.style.fontSize = '';
    document.body.style.zoom = '';
    applyAll(); save();
  });

  /* ── Reading ruler follows cursor ── */
  document.addEventListener('mousemove', function (e) {
    if (state.guide) ruler.style.top = (e.clientY - 22) + 'px';
  });

  /* ── Boot ── */
  applyAll();

})();
