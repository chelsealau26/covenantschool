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
Dismissal or following its CTA suppresses it for seven days in that browser,
and it does not reopen within the same tab session. Clearing or blocking
browser storage can prevent cross-visit suppression. There is no personal
information collection. Existing banner/footer links remain usable without JS.

Update school-confirmed progress in `assets/fundraiser-progress.json`, then
rebuild and publish through the normal process. The Python preview and static
build inject this one source into both the homepage welcome and fundraiser jug.
Generated HTML is not a second source to maintain. The popup uses the same
campaign cutoff as the banner and is retired by the server and in open tabs.
