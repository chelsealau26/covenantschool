/* Dependency-free Chromium comparison for color-only maintenance.
 * Usage: node .agents/scripts/test-fundraiser-palette.cjs [pre-change.html]
 * Without a baseline, checks the palette's static maintenance invariants.
 * The baseline is intercepted in-browser, never added as a public page.
 */
const fs = require('node:fs');
const assert = require('node:assert/strict');
const { spawn } = require('node:child_process');
const os = require('node:os');
const path = require('node:path');
const baseline = process.argv[2];
const current = fs.readFileSync('pages/fall-fundraiser.html', 'utf8');
const previous = baseline ? fs.readFileSync(baseline, 'utf8') : null;
// Assets, copy, scripts, and all non-style markup must remain byte-for-byte.
const withoutStyles = html => html.replace(/<style\b[^>]*>[\s\S]*?<\/style>/g, '');
if (previous) assert.equal(withoutStyles(current), withoutStyles(previous), 'Non-CSS content changed');
const palette = current.match(/<style id="fundraiser-newsletter-palette">([\s\S]*?)<\/style>/)[1];
const brandColors = require('./fundraiser-palette-rules.cjs');
for (const style of current.matchAll(/<style\b([^>]*)>([\s\S]*?)<\/style>/g)) {
  if (style[1].includes('fundraiser-newsletter-palette')) continue;
  for (const rule of style[2].matchAll(/([^{}]+)\{([^{}]*)\}/g)) {
    // Shared header/footer, contrast rules and inline artwork are explicit exceptions.
    if (!rule[1].includes('#main-content') || rule[1].includes('a11y-high-contrast')
      || rule[1].includes('.fixed-header-wrapper')) continue;
    for (const color of rule[2].matchAll(/#[\da-f]{3,8}\b/gi)) {
      assert(!brandColors[color[0].toLowerCase()], `Unapproved brand literal ${color[0]} in ${rule[1].trim()}`);
    }
  }
}
for (const [selector, token] of [
  ['#main-content #sponsors', 'detail-blue'],
  ['#main-content #sponsors .recipe-sponsor', 'detail-blue'],
  ['#main-content #sponsors .sponsor-levels', 'warm-paper'],
  ['#main-content.recipe-page .countdown-unit', 'detail-blue'],
]) {
  const css = [...current.matchAll(/<style\b[^>]*>([\s\S]*?)<\/style>/g)]
    .map(match => match[1]).join('\n').replace(/\/\*[\s\S]*?\*\//g, '');
  const rules = [...css.matchAll(/([^{}]+)\{([^{}]*)\}/g)]
    .filter(rule => rule[1].trim() === selector);
  assert(rules.some(rule => rule[2].includes(`var(--recipe-${token})`)),
    `${selector} must respond to --recipe-${token}`);
}
assert(!/#[\da-f]{3,8}\b|rgba?\(/i.test(palette.slice(palette.indexOf('body:not'))),
  'Normal-mode palette rules must use named tokens, not literal colors');
for (const token of ['ink', 'blue', 'paper', 'yellow', 'red', 'secondary', 'dark']) {
  assert.equal((current.match(new RegExp(`--recipe-${token}\\s*:`, 'g')) || []).length, 1,
    `Define --recipe-${token} once`);
}
if (!baseline) {
  console.log('PASS: fundraiser palette tokens are defined once; normal-mode palette rules use tokens');
  process.exit(0);
}
const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'palette-browser-'));
const chrome = spawn('chromium', ['--headless', '--no-sandbox', '--disable-dev-shm-usage',
  '--remote-debugging-port=9223', `--user-data-dir=${profile}`], { stdio: 'ignore' });
let ws;
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
(async () => {
  let targets;
  for (let i = 0; i < 100; i++) {
    try { targets = await (await fetch('http://127.0.0.1:9223/json')).json(); break; }
    catch { await sleep(100); }
  }
  assert(targets, 'Chromium did not start');
  ws = new WebSocket(targets.find(t => t.type === 'page').webSocketDebuggerUrl);
  await new Promise(resolve => ws.addEventListener('open', resolve, { once: true }));
  let id = 0, source;
  const pending = new Map();
  const send = (method, params = {}) => new Promise((resolve, reject) => {
    pending.set(++id, { resolve, reject });
    ws.send(JSON.stringify({ id, method, params }));
  });
  ws.addEventListener('message', async event => {
    const data = JSON.parse(event.data);
    if (data.id) {
      const callback = pending.get(data.id);
      pending.delete(data.id);
      data.error ? callback.reject(data.error) : callback.resolve(data.result);
    } else if (data.method === 'Fetch.requestPaused') {
      await send('Fetch.fulfillRequest', { requestId: data.params.requestId,
        responseCode: 200, responseHeaders: [{ name: 'Content-Type', value: 'text/html' }],
        body: Buffer.from(source).toString('base64') });
    }
  });
  const evaluate = async expression => {
    const result = await send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
    assert(!result.exceptionDetails, JSON.stringify(result.exceptionDetails));
    return result.result.value;
  };
  await send('Page.enable');
  await send('Fetch.enable', { patterns: [{ urlPattern: '*fall-fundraiser*', resourceType: 'Document' }] });
  await send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-reduced-motion', value: 'reduce' }] });
  await send('Page.addScriptToEvaluateOnNewDocument', { source: `
    const RealDate = Date;
    window.Date = class extends RealDate {
      constructor(...args) { super(...(args.length ? args : ['2026-10-09T12:00:00Z'])); }
      static now() { return new RealDate('2026-10-09T12:00:00Z').getTime(); }
    };
  ` });
  const snapshot = async () => {
    await sleep(300);
    await evaluate('new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))');
    return evaluate(`(() => {
    document.body.getBoundingClientRect();
    const properties = ['color','backgroundColor','backgroundImage','borderTopColor','borderRightColor',
      'borderBottomColor','borderLeftColor','outlineColor','boxShadow','textShadow','fill','stroke',
      'fontFamily','fontSize','fontWeight','lineHeight','display','padding','margin','borderRadius'];
    return [...document.body.querySelectorAll('*')].filter(el => !['SCRIPT','STYLE'].includes(el.tagName))
      .map(el => [el.tagName, el.id, ...['', '::before', '::after'].map(pseudo => {
        const s = getComputedStyle(el, pseudo || null);
        return properties.map(p => s[p]);
      }), ...['x','y','width','height'].map(k => Math.round(el.getBoundingClientRect()[k] * 100) / 100)]);
  })()`);
  };
  fs.mkdirSync('.agents/outputs/palette-comparison', { recursive: true });
  for (const width of [1440, 390]) {
    await send('Emulation.setDeviceMetricsOverride', { width, height: 900, deviceScaleFactor: 1, mobile: false });
    const results = [];
    for (const [label, html] of [['before', previous], ['after', current]]) {
      source = html;
      await send('Page.navigate', { url: `https://${process.env.REPLIT_DEV_DOMAIN}/fall-fundraiser` });
      for (let i = 0; i < 100; i++) {
        if (await evaluate(`document.readyState === 'complete' && !!document.querySelector('.recipe-goal')`)) break;
        await sleep(100);
      }
      await evaluate('document.fonts.ready.then(() => true)');
      await evaluate(`Promise.all([...document.images].map(img => img.decode().catch(() => {}))).then(() => true)`);
      await evaluate(`(() => {
        const style = document.createElement('style');
        style.textContent = '*,*::before,*::after{animation:none!important;transition:none!important}';
        document.head.appendChild(style);
      })()`);
      await sleep(1500);
      const states = {};
      states.normal = await snapshot();
      await evaluate(`document.querySelector('.calendar-entry-button').click()`);
      states.dialog = await snapshot();
      await evaluate(`document.querySelector('.calendar-dialog-close').click(); document.body.classList.add('a11y-high-contrast')`);
      states.contrast = await snapshot();
      results.push(states);
      await evaluate(`document.body.classList.remove('a11y-high-contrast')`);
      await sleep(300);
      const shot = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true,
        clip: { x: 0, y: 0, width, height: await evaluate('document.documentElement.scrollHeight'), scale: 1 } });
      fs.writeFileSync(`.agents/outputs/palette-comparison/${label}-${width}.png`, Buffer.from(shot.data, 'base64'));
    }
    const differences = [];
    for (const state of Object.keys(results[0])) {
      results[0][state].forEach((value, index) => {
        if (JSON.stringify(value) !== JSON.stringify(results[1][state][index])) {
          differences.push({ state, index, before: value, after: results[1][state][index] });
        }
      });
    }
    fs.writeFileSync(`.agents/outputs/palette-comparison/differences-${width}.json`, JSON.stringify(differences, null, 2));
    assert.equal(differences.length, 0, `${width}px: computed appearance differs; see differences-${width}.json`);
    console.log(`${width}px: all elements, pseudo-elements, layout, dialog and high-contrast styles unchanged`);
  }
})().catch(error => { console.error(error); process.exitCode = 1; })
  .finally(() => { if (ws) ws.close(); chrome.kill(); });
