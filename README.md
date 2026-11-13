# kfnxt.com

Static website for KFNXT (KF Integrated Energy Private Limited), built by `build.py` and published by GitHub Pages.

## Adding or removing services
Services come from **KF Ledger** (tables *Service Category* and *Service*, company `CO-KFE`).
Until KFNXT services are entered in KF Ledger, `data/catalog.json` holds the starter list from the old website.

1. Add the category / service in KF Ledger under company `CO-KFE`.
2. Run **publishAll** in the "KF websites publisher" Apps Script (or wait for the nightly run).
3. GitHub rebuilds the site in 1–2 minutes. Every category gets its own page (`/services/<name>`), a card on the home page, a footer link and a sitemap entry; the "Six ways…" heading counts itself.

## Website-only settings: `data/site.json`
One-line description, search-friendly name and icon per category, display order, and service IDs to hide.

## Other files
- `src/assets/`: stylesheet, logo, favicon. `src/content/`: privacy policy and terms.
