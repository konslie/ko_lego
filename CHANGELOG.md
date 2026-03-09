# Changelog

## [v1.0.0] - Lego Monitor Cloud Edition - 2026-03-09
- Initialized Python project with Playwright and Stealth capabilities to evade 403 blocks.
- Implemented robust `span[data-test="product-overview-availability"]` scraping to extract backorder date strings.
- Added Telegram bot integration for daily notification.
- Configured GitHub Actions CI/CD to run daily at 09:00 KST.
- Implemented termination logic (Action disables itself if backorder date < March 31st).
