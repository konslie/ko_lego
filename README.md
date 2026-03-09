# Lego Backorder Monitor (LBM)

## Overview
Lego Backorder Monitor is an automated scraping tool built with Python and Playwright. It checks the stock availability of the Lego APXGP Team Race Car (77252) daily, evading bot detection, and sends alerts via Telegram. If the backorder date is advanced before March 31, 2026, it will automatically shut down further alerts.

## Installation

1. Install Python 3.10+
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```
3. Create a Telegram Bot using `@BotFather` on Telegram and get your `TELEGRAM_BOT_TOKEN`.
4. Get your `TELEGRAM_CHAT_ID`. (You can use `@userinfobot` to find your ID).

## Usage

### Local Testing
```bash
export TELEGRAM_BOT_TOKEN="your_token_here"
export TELEGRAM_CHAT_ID="your_chat_id_here"
python main.py
```

### GitHub Actions (Cloud Edition)
The project is configured to run automatically everyday at 09:00 AM KST via GitHub Actions.
To set this up:
1. Push this repository to GitHub.
2. Go to **Settings > Secrets and variables > Actions**.
3. Add `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` as repository secrets.
4. Manually trigger the workflow using `workflow_dispatch` to verify setup.
