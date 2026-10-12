const assert = require('node:assert/strict');
const { checkPalette, checkAnnouncementMarkup } = require('./fundraiser-palette-rules.cjs');
module.exports = html => {
  const append = css => html + `<style>${css}</style>`;
  const badValues = [
    '#abc', '#abcd', '#123456', '#12345678', '#ABCDEF', '#1d3a5f',
    'rgb(7,8,9)', 'rgba(7,8,9,.4)', 'rgb(7 8 9 / 40%)',
    'hsl(120,50%,50%)', 'hsla(120,50%,50%,.4)', 'hsl(120 50% 50% / .4)',
    'hwb(120 10% 20%)', 'lab(50% 10 20)', 'lch(50% 10 20)',
    'oklab(.5 .1 .1)', 'oklch(.5 .1 40)', 'color(display-p3 1 0 0)',
    'rebeccapurple', 'RED', 'CanvasText', 'var(--recipe-ink, #abc)',
    'r\\65 d', 'r\\67 b(7 8 9)',
    'color-mix(in srgb, var(--recipe-ink), red)',
    'light-dark(var(--recipe-paper), #123456)',
  ];
  for (const value of badValues) {
    assert(checkPalette(append(`.new-fundraiser-component{color:${value}}`)).length,
      `Guard permitted ${value}`);
  }
  for (const css of [
    '@media(max-width:600px){#main-content .new{border:1px solid #abc}}',
    '@supports(display:grid){.recipe-new{box-shadow:0 0 2px rgb(1 2 3)}}',
    '@keyframes new-animation{50%{background:linear-gradient(red,blue)}}',
    '#main-content{--unrelated-custom-color:#abc}',
    '#main-content{--recipe-ink:var(--recipe-blue)}',
    'body:not(.a11y-high-contrast) #main-content{color:#abc}',
    'body.a11y-high-contrast #main-content, .normal{color:#abc}',
    '#main-content .fixed-header-wrapper{color:#abc}',
    '#main-content #prizes .grand-prize-list li:nth-child(1){color:#abc}',
    '#main-content #prizes .grand-prize-list li:nth-child(1){background-image:linear-gradient(red,blue)}',
  ]) assert(checkPalette(append(css)).length, `Guard permitted ${css}`);
  assert(checkPalette(html.replace('<main id="main-content"', '<main style="color:#abc" id="main-content"')
    .replace('tabindex="-1">', 'tabindex="-1"><p style="color:#abc">test</p>')).length, 'Inline styles escaped guard');
  assert(checkPalette(html.replace('id="global-styles">', 'id="global-styles">.recipe-new{color:#abc}')).length,
    'Shared stylesheet ID must not exempt new rules');
  assert(checkPalette(html.replace('id="fundraiser-newsletter-palette">', 'id="fundraiser-newsletter-palette">.new{color:#abc}')).length,
    'Palette stylesheet ID must not exempt component literals');
  const registerMutation = html.replace(/(<a\b[^>]*class="fundraiser-register[^>]*>[\s\S]*?<span)\b/, '$1 style="color:#ff00ff!important"');
  assert.notEqual(registerMutation, html, 'Register fixture did not find a label');
  assert(checkPalette(registerMutation).some(error => error.includes('#ff00ff')), 'Register label inline color escaped guard');
  assert(checkPalette(html.replace('color:#ffffff;font-family:', 'color:#ff00ff!important;font-family:'))
    .some(error => error.includes('#ff00ff')), 'Register anchor inline color escaped guard');
  const announcement = require('node:fs').readFileSync('assets/fundraiser-announcement.css', 'utf8');
  assert(checkPalette(html.replace('--recipe-ink:#1d3a5f;', '--recipe-ink:#ff00ff;')).length,
    'Off-brand replacement palette value escaped guard');
  assert(checkPalette(html.replace('--recipe-ink:#1d3a5f;', '--recipe-ink:#1d3a5f;--recipe-new:#ff00ff;')).length,
    'Off-brand new palette value escaped guard');
  assert(checkPalette(html, announcement.replace('--announcement-ink:#1d3a5f;', '--announcement-ink:#ff00ff;')).length,
    'Off-brand announcement palette value escaped guard');
  assert(checkPalette(html, announcement.replace('--announcement-ink:#1d3a5f;', '--announcement-ink:#1d3a5f;--announcement-new:#ff00ff;')).length,
    'Off-brand new announcement palette value escaped guard');
  const homepage = require('node:fs').readFileSync('pages/index.html', 'utf8');
  const mutatedHome = homepage.replace('<strong>Recipe for Success</strong>', '<strong style="color:#ff00ff!important">Recipe for Success</strong>');
  assert.notEqual(homepage, mutatedHome, 'Announcement fixture did not find markup');
  assert(checkAnnouncementMarkup(mutatedHome).length, 'Homepage announcement inline color escaped guard');
  for (const color of ['#ff00ff', 'rgb(255 0 255)', 'hsl(300 100% 50%)']) {
    assert(checkPalette(html, announcement + `.fundraiser-announcement-copy span{color:${color}!important}`)
      .some(error => error.includes(color)), `Announcement color escaped guard: ${color}`);
  }
  for (const css of [
    '.recipe-new{color:var(--recipe-ink);background:transparent;border-color:currentColor}',
    '.recipe-new{background:linear-gradient(var(--recipe-ink),var(--recipe-blue));content:"#abc red rgb(1,2,3)"}',
    '.recipe-new{background-image:url("data:image/svg+xml,<svg fill=\\\'#abc\\\'></svg>")}',
    'body.a11y-high-contrast #main-content{color:#abc}',
  ]) assert.deepEqual(checkPalette(append(css)), [], `Valid exception failed: ${css}`);
};
