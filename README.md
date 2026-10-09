# covenantschool

## Static hosting

Run `python3 scripts/build-static.py` and publish the generated `dist/`
directory. It contains the HTML pages plus the `assets/` and `pdfs/`
directories. Publishing `pages/` alone omits the fundraiser's local logos,
illustrations and downloads.

Wrangler runs this build automatically. For a dashboard-configured static
hosting project, use the same build command and `dist` output directory.
The Replit preview continues to use `python server.py`.

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
