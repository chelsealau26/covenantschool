// Runs inside Chromium. Edit the actual central definition rule: setting the
// token on an element would not recompute dependent custom properties inherited
// from an ancestor and could give a misleading result.
module.exports = function probeTokens() {
  const errors = [];
  const sheet = document.getElementById('fundraiser-newsletter-palette').sheet;
  const palette = [...sheet.cssRules].find(rule => rule.style?.getPropertyValue('--recipe-ink')).style;
  const probes = [
    ['ink', '.recipe-title', 'color'],
    ['pale-sky', '.recipe-tape', 'backgroundColor'],
    ['paper', '.recipe-hero-in', 'backgroundColor'],
    ['white', '#sponsors', 'backgroundColor'],
    ['detail-blue', '#sponsors .recipe-sponsor', 'backgroundImage', '::before'],
    ['detail-blue', '#sponsors .sponsor-deadline-note', 'backgroundImage', '::before'],
    ['blue', '.countdown-unit', 'borderRightColor'],
    ['warm-paper', '#sponsors .sponsor-levels', 'backgroundColor'],
    ['paper', '.calendar-event-dialog', 'backgroundColor'],
    ['calendar-line', '#dates .date-recipe', 'borderTopColor'],
    ['secondary', '.header-widget a.fundraiser-register', 'backgroundColor'],
    ['white', '.header-widget a.fundraiser-register span', 'color'],
  ];
  const footer = document.querySelector('.page-footer');
  const footerBefore = getComputedStyle(footer).backgroundColor;
  for (const [token, selector, property, pseudo] of probes) {
    const element = document.querySelector(selector);
    if (!element) { errors.push(`Missing probe ${selector}`); continue; }
    const name = '--recipe-' + token, original = palette.getPropertyValue(name);
    if (!original) { errors.push(`Missing token ${name}`); continue; }
    const read = () => getComputedStyle(element, pseudo || null)[property];
    const before = read();
    try {
      palette.setProperty(name, 'rgb(137, 29, 173)');
      const after = read();
      if (before === after || after === 'none') errors.push(`${name} did not reach ${selector} ${pseudo || ''} ${property}`);
      if (!/137|0\.537/.test(after)) errors.push(`${name} did not produce expected probe color: ${after}`);
    } finally { palette.setProperty(name, original); }
    if (read() !== before) errors.push(`${name} did not restore ${selector}`);
  }
  if (getComputedStyle(footer).backgroundColor !== footerBefore) errors.push('Palette changed shared footer');
  return errors;
};
