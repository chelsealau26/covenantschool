# Covenant Christian School Website

A static HTML website for Covenant Christian School (Mobile, AL), imported from the school's Simvoly-hosted site via a GitHub scrape-import.

## How to run

The project uses a simple Python static file server:

```
python server.py
```

This serves on **port 5000**. The workflow "Start application" is configured to run this automatically.

## Project structure

| Path | Description |
|------|-------------|
| `pages/` | All HTML pages (17 pages — index, athletics, calendar, tuition, etc.) |
| `assets/` | Images, logos, sponsor graphics downloaded from the original site |
| `pdfs/` | PDF documents (handbooks, forms, calendars) |
| `server.py` | Static file server — routes `/` → `pages/index.html`, `/assets/*`, `/pdfs/*` |
| `css-urls.txt` | CSS asset URLs from the original scrape |
| `wrangler.toml` | Cloudflare Pages config (original deploy target; not used here) |

## Pages

- `index.html` — Home
- `athletics.html` — Athletics
- `calendar.html` — Calendar
- `contact.html` — Contact
- `curriculum.html` — Curriculum
- `tuition.html` — Tuition
- `mission-values.html` — Mission & Values
- `new-student-application.html` — Apply
- `schedule-tour.html` — Schedule a Tour
- `scholarship-opportunities.html` — Scholarships
- `school-supplies.html` — School Supplies
- `technology.html` — Technology
- `ways-to-give.html` — Ways to Give
- `employment-openings.html` — Employment
- `aftercare.html` — Aftercare
- `ftp.html` — FTP
- `privacy-policy.html` — Privacy Policy

## Notes

- Page content and styles are largely self-contained in each HTML file, loading scripts/styles from the Simvoly CDN (`static.web-repository.com`, `content.app-sources.com`).
- Local asset files in `assets/` are not yet referenced by the HTML pages (they use CDN URLs). The assets are available for future use if you want to make the site fully offline-capable.
