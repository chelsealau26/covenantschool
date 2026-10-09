// November 9, 2026, 3:00 p.m. America/Chicago (CST).
export const END_TIME = "2026-11-09T21:00:00Z";
export const hasEnded = (now = Date.now()) => now >= Date.parse(END_TIME);
export const isFundraiserPath = path =>
  /^\/(?:pages\/)?fall-fundraiser(?:\.html)?\/?$/i.test(path);
export const removeBanner = html =>
  html.replace(/<aside\b[^>]*class="fundraiser-announcement"[\s\S]*?<\/aside>/g, "")
    .replace(/<p class="fundraiser-footer-link"[^>]*>[\s\S]*?<\/p>/g, "");
export const removeSitemapEntry = xml =>
  xml.replace(/<url>\s*<loc>https:\/\/covenantschool\.com\/fall-fundraiser<\/loc>[\s\S]*?<\/url>/g, "");
export const CLOSED_PAGE = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Fundraiser ended | Covenant Christian School</title></head><body><main><h1>This fundraiser has ended.</h1><p>Thank you for supporting Covenant Christian School.</p><a href="/">Return to the school website</a></main></body></html>';

// Also retire the banner in tabs left open when the deadline passes.
if (typeof window !== "undefined") {
  function checkDeadline() {
    if (hasEnded()) {
      document.querySelectorAll(".fundraiser-announcement, .fundraiser-footer-link").forEach(node => node.remove());
      if (isFundraiserPath(location.pathname)) location.replace("/");
      return;
    }
    setTimeout(checkDeadline, Math.min(86400000, Date.parse(END_TIME) - Date.now()));
  }
  checkDeadline();
  document.addEventListener("visibilitychange", () => {
    if (!document.hidden && hasEnded()) checkDeadline();
  });
}
