const assert = require('node:assert/strict');
const fs = require('node:fs');

const fundraiser = fs.readFileSync('pages/fall-fundraiser.html', 'utf8');
const homepage = fs.readFileSync('pages/index.html', 'utf8');
function footer(html) {
  const start = html.indexOf('<footer class="page-footer');
  assert.ok(start >= 0, 'Shared footer is present.');
  const end = html.indexOf('</footer>', start);
  assert.ok(end > start);
  return html.slice(start, end + '</footer>'.length);
}
assert.equal(
  footer(fundraiser), footer(homepage),
  'The fundraiser footer must match the main website, including its original logo.'
);
assert.ok(!fundraiser.includes('var footerLogo='));
assert.ok(!fundraiser.includes('footerImage.setAttribute'));
assert.ok(
  !fundraiser.includes('body:has(#main-content.recipe-page) .page-footer'),
  'Do not change the shared footer typography or colors only on this page.'
);
assert.ok(
  fundraiser.slice(0, fundraiser.indexOf('<main id="main-content"')).includes('src="/assets/fundraiser-header-logo-transparent.png"'),
  'Render the approved transparent fundraiser header logo in the initial HTML.'
);
console.log('PASS: exact shared footer markup/logo, no fundraiser-only footer overrides, header branding retained.');
