const postcss = require('postcss');
const fs = require('node:fs');
const path = require('node:path');
const { createHash } = require('node:crypto');
const { colors } = require('./fundraiser-color-parser.cjs');
const shared = require('./fundraiser-shared-css.json');
const approvedColors = require('./fundraiser-approved-colors.cjs');
const paletteId = 'fundraiser-newsletter-palette';
const paletteSelector = '#main-content.recipe-page, body.fundraiser-route .header-widget a.fundraiser-register';
const normalize = s => s.replace(/\s+/g, ' ').trim();
const fingerprint = rule => createHash('sha256').update(normalize(rule.toString())).digest('hex');
const metallic = new Map([
  ['#main-content #prizes .grand-prize-list li:nth-child(1)', 'linear-gradient(135deg,#fff0a8 0%,#f6cf68 25%,#fff5c7 43%,#e3b452 70%,#ffe6a0 100%)'],
  ['#main-content #prizes .grand-prize-list li:nth-child(2)', 'linear-gradient(135deg,#f7f9fc 0%,#cad3df 25%,var(--recipe-white) 43%,#bbc7d7 70%,#e5eaf1 100%)'],
  ['#main-content #prizes .grand-prize-list li:nth-child(3)', 'linear-gradient(135deg,#ffe3c5 0%,#e9b890 25%,#fff0db 43%,#d5a07e 70%,#f5ceb0 100%)'],
]);

// Shared site CSS is allowed by exact rule fingerprint, NOT by style ID or by
// finding "header" in a selector. Editing it requires deliberate review of this
// manifest. A new fundraiser selector in an old/shared style block still fails.
const sharedRules = new Set(shared.rules);
function allowance(decl, styleId) {
  const rule = decl.parent;
  const selector = rule.selector || '';
  if (styleId === paletteId && normalize(selector) === paletteSelector &&
      /^--recipe-[\w-]+$/.test(decl.prop)) return 'central palette';
  if (styleId === 'fundraiser-announcement' && selector === '.fundraiser-announcement' &&
      /^--announcement-[\w-]+$/.test(decl.prop)) return 'central palette';
  // Imported Register anchors keep these original inline declarations; neither
  // descendants nor new/important colors receive this shared-markup exception.
  if (styleId === 'register-anchor' && !decl.important &&
      ((decl.prop === 'color' && decl.value === '#ffffff') ||
       (decl.prop === 'border-color' && decl.value === '#333333'))) return 'shared Register markup';
  // Split using the CSS parser, not commas inside :is()/:not().
  if (selector && postcss.list.comma(selector).every(s =>
      /^(?:#main-content\s+)?body\.a11y-high-contrast(?:[.#\s:]|$)/.test(s.trim()))) return 'high contrast';
  if (decl.prop === 'background-image' && metallic.get(selector) === decl.value) return 'metallic artwork';
  if (sharedRules.has(fingerprint(rule))) return 'shared site';
  return null;
}

function checkCss(css, styleId, errors, definitions) {
  const root = postcss.parse(css);
  root.walkDecls(decl => {
    const allowed = allowance(decl, styleId);
    if (allowed === 'central palette') {
      if (!approvedColors.has(decl.value)) errors.push(`Unapproved palette value ${decl.prop}: ${decl.value}`);
      if (definitions.has(decl.prop)) errors.push(`Duplicate palette definition ${decl.prop}`);
      definitions.add(decl.prop);
    } else if (/^--(?:recipe|announcement)-/.test(decl.prop) && allowed !== 'high contrast') {
      errors.push(`Define ${decl.prop} only in the central palette`);
    }
    const found = colors(decl.value);
    if (found.length && !allowed) errors.push(
      `${decl.parent.selector || decl.parent.name || 'inline style'}: ${decl.prop}: ${found.map(c => c.value).join(', ')}`);
  });
}

function checkPalette(html, announcement = fs.readFileSync(path.join(__dirname, '../../assets/fundraiser-announcement.css'), 'utf8')) {
  const errors = [], definitions = new Set();
  for (const style of html.matchAll(/<style\b([^>]*)>([\s\S]*?)<\/style>/gi)) {
    const id = style[1].match(/\bid=["']([^"']+)["']/i)?.[1];
    checkCss(style[2], id, errors, definitions);
  }
  // Authentic SVG presentation attributes and URL/data artwork are deliberately
  // outside the brand guard. CSS style attributes inside the fundraiser are not.
  const main = html.match(/<main\b[^>]*id=["']main-content["'][^>]*>[\s\S]*?<\/main>/i)?.[0] || '';
  for (const attr of main.matchAll(/\bstyle=(["'])([\s\S]*?)\1/gi)) {
    checkCss(`inline{${attr[2].replace(/&quot;/g, '"').replace(/&#39;/g, "'")}}`,
      '', errors, definitions);
  }
  for (const anchor of html.matchAll(/<a\b[^>]*\bclass=(["'])[^"']*\bfundraiser-register\b[^"']*\1[^>]*>[\s\S]*?<\/a>/gi)) {
    for (const [index, tag] of [...anchor[0].matchAll(/<[^>]+>/g)].entries()) {
      for (const attr of tag[0].matchAll(/\bstyle=(["'])([\s\S]*?)\1/gi)) {
        checkCss(`inline{${attr[2].replace(/&quot;/g, '"').replace(/&#39;/g, "'")}}`,
          index === 0 ? 'register-anchor' : '', errors, definitions);
      }
    }
  }
  checkCss(announcement, 'fundraiser-announcement', errors, definitions);
  for (const token of ['ink', 'blue', 'paper', 'yellow', 'red', 'secondary', 'dark']) {
    if (!definitions.has(`--recipe-${token}`)) errors.push(`Missing palette token --recipe-${token}`);
  }
  return errors;
}
function checkAnnouncementMarkup(html) {
  const errors = [];
  for (const announcement of html.matchAll(/<aside\b[^>]*\bclass=(["'])[^"']*\bfundraiser-announcement\b[^"']*\1[^>]*>[\s\S]*?<\/aside>/gi)) {
    for (const attr of announcement[0].matchAll(/\bstyle=(["'])([\s\S]*?)\1/gi)) {
      checkCss(`inline{${attr[2].replace(/&quot;/g, '"').replace(/&#39;/g, "'")}}`,
        '', errors, new Set());
    }
  }
  return errors;
}
module.exports = { checkPalette, checkAnnouncementMarkup, colors, fingerprint };
