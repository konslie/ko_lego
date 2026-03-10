# Changelog

## [v1.0.2] - Action Reliability Update - 2026-03-10
- Switched GitHub Actions runner from `ubuntu-latest` to `macos-latest` to avoid Linux datacenter IP blocks.
- Added macOS matching User-Agent in `scraper.py`.
- Implemented error screenshot capture and artifact upload on GitHub Actions for debugging timeouts.

## [v1.0.1] - Dependency Fix - 2026-03-10
- Fixed `playwright-stealth` module loading error (`pkg_resources` missing) by pinning `setuptools<70.0.0` in `requirements.txt`.
- Resolved timeout issues where the scraper failed due to stealth module initialization failure.

## [v1.0.0] - Lego Monitor Cloud Edition - 2026-03-09
- Initialized Python project with Playwright and Stealth capabilities to evade 403 blocks.
- Implemented robust `span[data-test="product-overview-availability"]` scraping to extract backorder date strings.
- Added Telegram bot integration for daily notification.
- Configured GitHub Actions CI/CD to run daily at 09:00 KST.
- Implemented termination logic (Action disables itself if backorder date < March 31st).
