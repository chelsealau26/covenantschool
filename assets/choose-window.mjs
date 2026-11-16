// CHOOSE Act 2027–2028 application window: scheduled switch on the Scholarships page.
// Blocks ship in two versions: <!--choose:soon-->…<!--/choose:soon--> and <!--choose:open-->…<!--/choose:open-->.
// Before OPEN_TIME visitors see "soon" ("Opens January 4"); from OPEN_TIME on they see "open" ("Open now").
// Add &choose=open to a preview link to review the "open" version early.
// To change the date, edit OPEN_TIME and redeploy.

// January 4, 2027, 12:00 a.m. America/Chicago (CST).
export const OPEN_TIME = "2027-01-04T06:00:00Z";

export const isChooseOpen = (now = Date.now()) => now >= Date.parse(OPEN_TIME);
export const showChooseOpen = (url, isPreview, now = Date.now()) =>
  isChooseOpen(now) || (isPreview && url.searchParams.get("choose") === "open");
export const pickChooseVersion = (html, open) =>
  html.replace(open ? /<!--choose:soon-->[\s\S]*?<!--\/choose:soon-->\n?/g : /<!--choose:open-->[\s\S]*?<!--\/choose:open-->\n?/g, "");
