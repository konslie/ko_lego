# Memory

## Current Session Goal
Implementing a Playwright-based scraper and Telegram notifier managed by GitHub Actions. (Cloud Edition PRD)

## Progress vs Goal
- Tested Python Playwright script locally (using Python 3.10), confirmed avoidance of `403 Forbidden` and successfully extracted `백오더 가능, 2026년 3월 31일 출고 예정`.
- Implemented `main.py` which ties `scraper.py` checking logic to a Telegram Bot.
- Added GitHub Actions `.github/workflows/daily-run.yml` enabling 09:00 KST daily runs and automatic workflow termination if backorder dates are changed before Mar 31st.

## Critical Technical Decisions & Roadblocks
- Relying on `playwright-stealth` which faced some PyPI dependency issues locally inside Python 3.12 (`pkg_resources` missing); circumvented by pinning `setuptools<70.0.0` inside `requirements.txt` to restore compatibility.
- Encountered Telegram `Chat not found` error which indicates the Bot token or Chat ID is incorrect, or the user has not initiated a conversation with the bot via `/start`. 
- GitHub Actions IP addresses are aggressively flagged by Lego.com's Cloudflare setup (Captcha "보안확인수행중"). Implemented Javascript property injections (`navigator.webdriver`, `languages`, `plugins`) and simulated mouse movements/scrolling to evade this layer.

## Next Step
- Push the `macos-latest` runner changes and screenshot debugging to GitHub.
- Manually trigger the GitHub Action and review the `error_screenshot.png` artifact to see what page the bot is given if a timeout still occurs.
