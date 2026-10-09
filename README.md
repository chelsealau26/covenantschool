# covenantschool

## Static hosting

Run `python3 scripts/build-static.py` and publish the generated `dist/`
directory. It contains the HTML pages plus the `assets/` and `pdfs/`
directories. Publishing `pages/` alone omits the fundraiser's local logos,
illustrations and downloads.

Wrangler runs this build automatically. For a dashboard-configured static
hosting project, use the same build command and `dist` output directory.
The Replit preview continues to use `python server.py`.
