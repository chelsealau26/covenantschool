// Education Freedom Tax Credit page: scheduled launch.
// Before LAUNCH_TIME the page returns 404 and every link/callout to it is stripped,
// unless the request carries ?preview=PREVIEW_KEY (for client review).
// To launch early or late, change LAUNCH_TIME and redeploy.

// December 1, 2026, 12:00 a.m. America/Chicago (CST).
export const LAUNCH_TIME = "2026-12-01T06:00:00Z";
// Not a secret (this repo is public); it only keeps the draft out of casual view and search engines.
export const PREVIEW_KEY = "JBYlnxBB-i0b";

export const isLaunched = (now = Date.now()) => now >= Date.parse(LAUNCH_TIME);
export const isPreview = url => url.searchParams.get("preview") === PREVIEW_KEY;
export const isEftcPath = path => /^\/(?:pages\/)?federal-tax-credit(?:\.html)?\/?$/i.test(path);

export const hideEftc = html =>
  html.replace(/<section class="eftc eftc-callout"[\s\S]*?<\/section>\s*/g, "")
    .replace(/\s*<li>\s*<a class="website-nav-link" rel="tab" href="\/federal-tax-credit" >Federal Tax Credit<\/a>\s*<\/li>/g, "")
    .replace(/<p style="line-height: 2;"><span style="color: rgba\(255, 255, 255, 0\.7\); font-size: 15px;"><a href="\/federal-tax-credit">Federal Tax Credit<\/a><\/span><\/p>/g, "")
    .replace(/\n?<li class="eftc-privacy">[\s\S]*?<\/li>/g, "");

export const hideEftcSitemap = xml =>
  xml.replace(/\s*<url><loc>https:\/\/covenantschool\.com\/federal-tax-credit<\/loc>[\s\S]*?<\/url>/g, "");

export const NOT_FOUND_PAGE = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Page not found | Covenant Christian School</title></head><body><main><h1>Page not found</h1><a href="/">Return to the school website</a></main></body></html>';

// Tax-credit blocks ship in two versions: <!--eftc:soon-->…<!--/eftc:soon--> and <!--eftc:live-->…<!--/eftc:live-->.
// Before launch visitors see "soon"; after launch (or on a preview link) they see "live".
// Add &soon=1 to a preview link to review the "coming soon" version.
export const showLiveCredit = (url, now = Date.now()) =>
  isLaunched(now) || (isPreview(url) && url.searchParams.get("soon") !== "1");
export const pickCreditVersion = (html, live) =>
  html.replace(live ? /<!--eftc:soon-->[\s\S]*?<!--\/eftc:soon-->\n?/g : /<!--eftc:live-->[\s\S]*?<!--\/eftc:live-->\n?/g, "");

// Redesigned pages awaiting approval: served in place of the current page only on a preview link.
// "/page": "/redesign/page" entries preview a redesign at its normal URL (homepage = "").
export const REDESIGNS = { "": "/redesign/home", "/index": "/redesign/home", "/brand-guide": "/redesign/brand-guide", "/mission-values": "/redesign/mission-values", "/employment-openings": "/redesign/employment-openings" };
export const redesignFor = path => REDESIGNS[path.replace(/\.html$|\/$/i, "").toLowerCase()];
export const isRedesignPath = path => /^\/(?:pages\/)?redesign(?:\/|$)/i.test(path);
