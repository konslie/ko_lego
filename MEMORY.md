# Memory

## Current Session Goal
Implementing a Playwright-based scraper and Telegram notifier managed by GitHub Actions. (Cloud Edition PRD)

## Progress vs Goal
- Tested Python Playwright script locally (using Python 3.10), confirmed avoidance of `403 Forbidden` and successfully extracted `백오더 가능, 2026년 3월 31일 출고 예정`.
- Implemented `main.py` which ties `scraper.py` checking logic to a Telegram Bot.
- Added GitHub Actions `.github/workflows/daily-run.yml` enabling 09:00 KST daily runs and automatic workflow termination if backorder dates are changed before Mar 31st.

## Critical Technical Decisions & Roadblocks
- Relying on `playwright-stealth` which faced some PyPI dependency issues locally inside Python 3.12 (`pkg_resources` missing); circumvented by testing in Python 3.10 and using `ubuntu-latest` (Python 3.10) for final GitHub Actions runtime where it evaluates successfully.
- Added early termination conditions so it doesn't run infinitely. 

## Next Step
- Final verification of the artifacts, wait for user to configure their Telegram Bot Tokens and push to GitHub so they can manually trigger the Action to confirm it runs well in the cloud.
