import os
import asyncio
from telegram import Bot
from scraper import fetch_status, check_termination_condition

# Tokens should be injected securely via GitHub Secrets
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

async def send_telegram_message(message: str):
    """Sends a formatted message to the specified Telegram Chat ID."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram credentials missing. Skipping notification.")
        return

    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    try:
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        print("Notification sent successfully.")
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")

async def main():
    print("Starting Lego Backorder Monitor...")
    status_text = await fetch_status()
    print(f"Extraction Result: {status_text}")
    
    # 1. Formatting the Message
    if status_text.startswith("Error"):
        final_message = f"🚨 **Lego Monitor Alert** 🚨\n\nFailed to extract product status.\nDetails: {status_text}"
        should_terminate = False
    else:
        # Check termination condition based on user PRD
        should_terminate = check_termination_condition(status_text)
        
        status_emoji = "✅" if "재고" in status_text or "가능" in status_text else "⚠️"
        final_message = (
            f"🏎️ **Lego APXGP (77252) Status** 🏎️\n\n"
            f"Status: {status_emoji} {status_text}\n"
        )
        if should_terminate:
             final_message += "\n🛑 **Notice**: The backorder date is earlier than March 31st (or it is past March 31st). GitHub Actions will be terminated/disabled."

    # 2. Fire the Notification
    await send_telegram_message(final_message)
    
    # 3. Handle GitHub Actions Termination Signal
    # We exit with a specific code (e.g. 0 for success, or we can use GitHub outputs to disable the workflow)
    # For now, we will just print a known string so the workflow can grep it or we exit with a specific code.
    if should_terminate:
        print("TERMINATION_CONDITION_MET=true")
        # You could also use the official GitHub Actions method to set output:
        # with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        #     print(f"terminate=true", file=fh)
        
if __name__ == "__main__":
    asyncio.run(main())
