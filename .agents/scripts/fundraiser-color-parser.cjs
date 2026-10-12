// Parse CSS values rather than matching known brand hexes. Strings and URLs are
// artwork/content, not CSS colors; var() fallbacks and nested functions are checked.
const parse = require('postcss-value-parser');
const names = require('color-name');
const functions = /^(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch|color|device-cmyk)$/i;
const systemColors = /^(?:accentcolor|accentcolortext|activetext|buttonborder|buttonface|buttontext|canvas|canvastext|field|fieldtext|graytext|highlight|highlighttext|linktext|mark|marktext|selecteditem|selecteditemtext|visitedtext)$/i;
const unescape = value => value.replace(/\\([\da-f]{1,6})\s?|\\([^\n\r])/gi,
  (_, hex, char) => hex ? String.fromCodePoint(Math.min(parseInt(hex, 16) || 0xfffd, 0x10ffff)) : char);

function colors(value) {
  const result = [];
  parse(unescape(value)).walk(node => {
    const name = node.value.toLowerCase();
    if (node.type === 'function') {
      if (name === 'url') return false;
      // Relative color functions derive channels from a token, not literals.
      if (functions.test(name) &&
          !/^\s*from\s+var\(--recipe-[\w-]+\)\s+[rgbhslabcxyz]+\s/i.test(parse.stringify(node.nodes))) {
        result.push({ value: parse.stringify(node), start: node.sourceIndex,
          end: node.sourceIndex + parse.stringify(node).length });
        return false;
      }
    }
    if (node.type === 'word' && (/^#[\da-f]{3,8}$/i.test(name) ||
        Object.hasOwn(names, name) || systemColors.test(name))) {
      result.push({ value: node.value, start: node.sourceIndex,
        end: node.sourceIndex + node.value.length });
    }
  });
  return result;
}
module.exports = { colors };
