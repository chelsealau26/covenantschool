/* Palette guard + real Chromium token mutation checks.
 * Usage: node .agents/scripts/test-fundraiser-palette.cjs [pre-change.html|--static]
 * Optional baseline adds computed appearance comparisons; never a public page.
 * The baseline is intercepted in-browser, never added as a public page.
 */
const fs = require('node:fs');
const assert = require('node:assert/strict');
const { spawn } = require('node:child_process');
const os = require('node:os');
const path = require('node:path');
const baseline = process.argv[2] === '--static' ? null : process.argv[2];
const current = fs.readFileSync('pages/fall-fundraiser.html', 'utf8');
const previous = baseline ? fs.readFileSync(baseline, 'utf8') : null;
// Assets, copy, scripts, and all non-style markup must remain byte-for-byte.
const withoutStyles = html => html.replace(/<style\b[^>]*>[\s\S]*?<\/style>/g, '');
if (previous) assert.equal(withoutStyles(current), withoutStyles(previous), 'Non-CSS content changed');
const { checkPalette, checkAnnouncementMarkup } = require('./fundraiser-palette-rules.cjs');
assert.deepEqual(checkPalette(current), [], 'Unapproved CSS literals (use central palette tokens)');
for (const entry of fs.readdirSync('pages', { recursive: true })) {
  if (entry.endsWith('.html')) assert.deepEqual(
    checkAnnouncementMarkup(fs.readFileSync(path.join('pages', entry), 'utf8')), [],
    `${entry}: unapproved inline announcement colors`);
}
require('./test-fundraiser-palette-fixtures.cjs')(current);
console.log('PASS: palette definitions, literal rejection and exception fixtures');
if (process.argv.includes('--static')) {
  process.exit(0);
}
const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'palette-browser-'));
const chrome = spawn('chromium', ['--headless', '--no-sandbox', '--disable-dev-shm-usage',
  '--remote-debugging-port=0', `--user-data-dir=${profile}`], { stdio: 'ignore' });
let ws;
let launchError;
chrome.on('error', error => { launchError = error; });
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
const timeout = setTimeout(() => { console.error('Palette browser timed out'); chrome.kill(); process.exit(1); }, 180000);
(async () => {
  let targets;
  for (let i = 0; i < 100; i++) {
    if (launchError) throw launchError;
    try {
      const port = fs.readFileSync(path.join(profile, 'DevToolsActivePort'), 'utf8').split('\n')[0];
      targets = await (await fetch(`http://127.0.0.1:${port}/json`)).json(); break;
    }
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
        // Chromium serializes relative RGB as color(srgb); canonicalize only
        // that equivalent representation for pre/post computed comparisons.
        return properties.map(p => s[p].replace(/color\\(srgb ([\\d.]+) ([\\d.]+) ([\\d.]+) \\/ ([\\d.]+)\\)/g,
          (_,r,g,b,a) => 'rgba(' + [r,g,b].map(v=>Math.round(v*255)).join(', ') + ', ' + a + ')'));
      }), ...['x','y','width','height'].map(k => Math.round(el.getBoundingClientRect()[k] * 100) / 100)]);
  })()`);
  };
  const output = 'generated-artifacts/palette-comparison';
  fs.mkdirSync(output, { recursive: true });
  for (const width of [1440, 390]) {
    await send('Emulation.setDeviceMetricsOverride', { width, height: 900, deviceScaleFactor: 1, mobile: false });
    const results = [];
    for (const [label, html] of (baseline ? [['before', previous], ['after', current]] : [['after', current]])) {
      source = html;
      const baseUrl = process.env.BASE_URL || `https://${process.env.REPLIT_DEV_DOMAIN}`;
      await send('Page.navigate', { url: `${baseUrl}/fall-fundraiser` });
      for (let i = 0; i < 100; i++) {
        if (await evaluate(`document.readyState === 'complete' && !!document.querySelector('.recipe-goal')`)) break;
        await sleep(100);
      }
      await evaluate('document.fonts.ready.then(() => true)');
      assert(await evaluate(`!!document.querySelector('.recipe-goal')`), 'Fundraiser page did not load');
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
      if (label === 'after') {
        const mutationErrors = await evaluate(`(${require('./fundraiser-token-probes.cjs').toString()})()`);
        assert.deepEqual(mutationErrors, [], width + 'px: token mutations must change computed component colors');
        console.log(width + 'px: representative components and sponsor gingham respond to token edits');
      }
      if (!baseline) continue;
      const shot = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true,
        clip: { x: 0, y: 0, width, height: await evaluate('document.documentElement.scrollHeight'), scale: 1 } });
      fs.writeFileSync(`${output}/${label}-${width}.png`, Buffer.from(shot.data, 'base64'));
    }
    if (!baseline) continue;
    const differences = [];
    for (const state of Object.keys(results[0])) {
      assert.equal(results[0][state].length, results[1][state].length, 'Element count changed');
      results[0][state].forEach((value, index) => {
        if (JSON.stringify(value) !== JSON.stringify(results[1][state][index])) {
          differences.push({ state, index, before: value, after: results[1][state][index] });
        }
      });
    }
    fs.writeFileSync(`${output}/differences-${width}.json`, JSON.stringify(differences, null, 2));
    assert.equal(differences.length, 0, `${width}px: computed appearance differs; see differences-${width}.json`);
    console.log(`${width}px: all elements, pseudo-elements, layout, dialog and high-contrast styles unchanged`);
  }
})().catch(error => { console.error(error); process.exitCode = 1; })
  .finally(() => {
    clearTimeout(timeout);
    if (ws) ws.close();
    chrome.kill();
    chrome.once('exit', () => fs.rmSync(profile, { recursive: true, force: true }));
  });
