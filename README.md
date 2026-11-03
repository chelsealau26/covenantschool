# covenantschool

## Static hosting

Run `python3 scripts/build-static.py` and publish the generated `dist/`
directory. It contains the HTML pages plus the `assets/` and `pdfs/`
directories. Publishing `pages/` alone omits the fundraiser's local logos,
illustrations and downloads.

Wrangler runs this build automatically. For a dashboard-configured static
hosting project, use the same build command and `dist` output directory.
The Replit preview continues to use `python server.py`.


## Fundraiser palette checks

Run `npm ci`, then `npm test` with the preview server running. The registered
`fundraiser-palette` validation runs the same command. It rejects CSS color
literals outside the central palette and tests real token edits in Chromium at
1440px and 390px. `BASE_URL` can override the preview address.

For a quick parser/fixture check without a server, run `npm run test:palette:static`.
For color-only maintenance, save the pre-edit HTML outside the public site and run
`node .agents/scripts/test-fundraiser-palette.cjs /tmp/pre-edit.html`. This also
compares all computed element/pseudo-element styles, layout, open calendar and
high-contrast states. Outputs go to ignored `generated-artifacts/`.

Keep literal definitions in `fundraiser-newsletter-palette`, not in component
rules (including inline CSS, media queries and keyframes). Authentic artwork
URLs/SVG presentation attributes, the three approved metallic prize gradients,
positive high-contrast selectors and exact approved shared-site rules are
exceptions. Shared rule fingerprints in
`.agents/scripts/fundraiser-shared-css.json` must only change after deliberate
review; do not refresh them to silence a fundraiser color failure.
The guard also checks Register-button inline styles (including their labels)
and `assets/fundraiser-announcement.css`. The announcement has a scoped
`--announcement-*` palette because it appears on pages without fundraiser-page
tokens. Only the imported Register anchors' original non-important white text
and gray border literals are grandfathered; new inline colors are rejected.
Announcement inline markup is checked across every HTML page. Palette definition
values must also be present in `.agents/scripts/fundraiser-approved-colors.cjs`;
do not auto-refresh that reviewed list from the page when validation fails.

## Automatic fundraiser retirement

The cutoff is November 9, 2026 at 3 p.m. Central (21:00 UTC), defined in
`assets/fundraiser-lifecycle.mjs`. The Python server and Cloudflare Worker
check it on every request: after the cutoff the banner is removed, the
fundraiser URL returns HTTP 410 with `noindex`, and its sitemap entry is
removed. Open browser tabs also retire the banner.

Deploy through Wrangler (which includes `worker.mjs`) or run the Python
server. Uploading only `dist/` to a purely static host provides the browser
fallback but **cannot enforce the server-side 410 or sitemap removal**.
The automation must be deployed before the deadline; no further deployment
is needed at the cutoff.

## Homepage fundraiser welcome

### Optional popup analytics

The welcome popup calls an existing `window.umami.track` only when available;
it does not install a tracker, send personal data, queue events for later, or
wait for analytics before opening, closing, or following the CTA.

| Event | Meaning |
| --- | --- |
| `fundraiser_popup_impression` | Successfully displayed popup |
| `fundraiser_popup_dismiss` | Explicit close, Continue to website, or Escape |
| `fundraiser_popup_click` | Explore the fundraiser link activated (not a confirmed destination pageview) |

Each event has `device: desktop` or `mobile`, captured at display using the
popup's 767px breakpoint. Dismissals also have `method: close`, `continue`, or
`escape`. CTA clicks are not counted as dismissals. Expiry, page navigation
cleanup and suppressed displays are not dismissal/impression events.
One displayed popup produces at most one outcome event.

Access to Replit analytics was verified during implementation, but this project
had no Replit publication at that time. To collect on a supported Replit
publication, enable analytics in Publishing settings and publish or republish.
The Cloudflare Worker/static export does **not** receive Replit's injected
tracker; on those hosts these calls remain no-ops unless a compatible tracker
is separately configured. Existing Google consent bootstrap code is not proof
of an installed analytics collector. No second tracker was added.

Counts are best-effort: blockers, a late-loading tracker, or navigation may
prevent delivery. Compare clicks with impressions by device to assess popup
engagement; do not describe clicks as completed registrations or donations.

The homepage offers a compact desktop dialog and a full-screen mobile dialog.
It opens half a second after the page markup is ready, without waiting for all
images and external assets to finish loading.
It appears on every visit to the homepage: arriving from another page, a typed
URL, a normal or hard refresh, and Back/Forward (including pages restored from
the browser's back/forward cache). Dismissing it only prevents it from reopening
during the same page view; nothing is remembered between visits, and any
suppression keys saved by earlier versions are cleared. It never bypasses
campaign expiry, hash exclusions, or active keyboard/menu/dialog safeguards.
There is no personal information collection. Existing banner/footer links remain usable without JS.

Update school-confirmed progress in `assets/fundraiser-progress.json`, then
rebuild and publish through the normal process. The Python preview and static
build inject this one source into both the homepage welcome and fundraiser jug.
Generated HTML is not a second source to maintain. The popup uses the same
campaign cutoff as the banner and is retired by the server and in open tabs.

## Accessibility and SEO

Every page loads `assets/site-a11y.css` last. It holds the site-wide WCAG 2.2 AA
fixes: navy text on gold buttons, a deeper gold (`.ccs-gold-text`) for gold text
on light backgrounds, darker gray buttons, a visible keyboard focus ring,
reduced-motion support, the `.sr-only` utility and the privacy policy's
document styling. The fundraiser page keeps its own tested focus, motion and
Register-button colors; the shared rules are scoped so they don't change it.

Page structure: the site header parts are wrapped in
`<header class="ccs-site-header">` (one banner landmark) and page content in
`<main id="main-content">`, which is also the skip link's target. Rules that
position header parts with `>` must account for the wrapper (see
`assets/mobile-header.css`). Footer section headings use `aria-level="2"` on
every page so the shared footer stays identical site-wide.

Images: describe only what is visible in the photo. Stock photos beside a heading
that already says the same thing use `alt=""` so screen readers skip them.

SEO: each page has its own title (60 characters or fewer) and description
(about 155 characters or fewer), matching Open Graph/Twitter tags and
WebPage + BreadcrumbList structured data. `pages/sitemap.xml` lists all public
pages; the privacy policy stays `noindex`. After deploying, submit the sitemap
in Google Search Console.

## Federal Tax Credit page (scheduled launch)

`/federal-tax-credit` (AOSF pledge widget) goes live automatically on
December 1, 2026 at 12:00 a.m. Central (`LAUNCH_TIME` in
`assets/eftc-launch.mjs`). Before then the Cloudflare Worker returns 404 for
the page and strips its menu/footer links, the Ways to Give and Scholarship
callouts, the privacy-policy line and the sitemap entry. Adding
`?preview=<PREVIEW_KEY>` to any URL shows the launched version for review
(marked `noindex`). To change the date, edit `LAUNCH_TIME` and redeploy.

Note: this Cloudflare project currently deploys every pushed branch to
production, so a pushed branch is a live change.

## Redesigned giving pages (preview until approved)

`scripts/build-giving-pages.py` builds `pages/redesign/ways-to-give.html`,
`pages/redesign/scholarship-opportunities.html` and `pages/federal-tax-credit.html`
(styles: `assets/giving.css`, motion: `assets/giving.js`). The worker serves the
redesigns at their normal URLs only with `?preview=<PREVIEW_KEY>`; `/redesign/*`
is otherwise 404. To publish, copy the redesign files over the files in `pages/`.

Tax-credit blocks have `<!--eftc:soon-->` and `<!--eftc:live-->` versions; the
worker shows "soon" before the launch time and "live" after (preview links show
"live"; add `&soon=1` to see "soon").

## Refreshed design (preview only, awaiting client approval)
- Preview links: `https://covenantschool.com/?preview=JBYlnxBB-i0b` (homepage) and `/brand-guide?preview=JBYlnxBB-i0b` (brand guide).
- Sitewide styles for the refresh live in `assets/preview.css`; `worker.mjs` adds it only on preview links. Preview-only pages live in `pages/redesign/` and are mapped in `REDESIGNS` (`assets/eftc-launch.mjs`).
- Opening any preview link sets a `ccs_preview` cookie (14 days), so every page clicked afterward stays on the preview; a "Preview · Exit" badge links to `?preview=off`, which clears it.
- Preview links also retire `/school-supplies` (redirects to the Family Portal); the live page stays until approval.
- To publish: move `preview.css` rules into `site-a11y.css`/`giving.css`, swap `pages/redesign/home.html` into `pages/index.html`, drop the school-supplies page, and remove the preview injection.
