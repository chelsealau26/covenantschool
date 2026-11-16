// CHOOSE Act 2027–2028 application window: scheduled switches on the Scholarships page.
// Blocks ship in up to three versions:
//   <!--choose:soon-->…<!--/choose:soon-->     before OPEN_TIME   ("Opens January 4")
//   <!--choose:open-->…<!--/choose:open-->     OPEN_TIME–CLOSE_TIME ("Open now")
//   <!--choose:closed-->…<!--/choose:closed--> from CLOSE_TIME on ("Closed")
// Add &choose=open or &choose=closed to a preview link to review those versions early.
// To change a date, edit it here and redeploy.

// January 4, 2027, 12:00 a.m. America/Chicago (CST).
export const OPEN_TIME = "2027-01-04T06:00:00Z";
// Applications close at midnight on March 31, 2027: April 1, 12:00 a.m. America/Chicago (CDT).
export const CLOSE_TIME = "2027-04-01T05:00:00Z";

const STATES = ["soon", "open", "closed"];
export const chooseState = (now = Date.now()) =>
  now >= Date.parse(CLOSE_TIME) ? "closed" : now >= Date.parse(OPEN_TIME) ? "open" : "soon";
export const chooseStateFor = (url, isPreview, now = Date.now()) => {
  const asked = isPreview && url.searchParams.get("choose");
  return STATES.includes(asked) ? asked : chooseState(now);
};
export const pickChooseVersion = (html, state) =>
  STATES.filter(s => s !== state).reduce(
    (out, s) => out.replace(new RegExp(`<!--choose:${s}-->[\\s\\S]*?<!--\\/choose:${s}-->\\n?`, "g"), ""), html);
