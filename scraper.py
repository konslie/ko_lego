import asyncio
import re
import datetime
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

URL = "https://www.lego.com/ko-kr/product/apxgp-team-race-car-from-f1-the-movie-77252"
SELECTOR = 'span[data-test="product-overview-availability"]'

async def fetch_status():
    async with async_playwright() as p:
        # Launch browser in headless mode with extra arguments for evasion
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-blink-features=AutomationControlled',
                '--disable-infobars',
                '--window-size=1920,1080',
            ]
        )
        # Create a new context with standard user agent and language matching local behaviors
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080},
            locale='ko-KR',
            timezone_id='Asia/Seoul'
        )
        page = await context.new_page()
        
        # Apply stealth to evade bot detection
        await stealth_async(page)
        
        try:
            # Navigate to the page
            await page.goto(URL, wait_until='load', timeout=45000)
            
            # Wait a few seconds to let any popups or dynamic rendering finish
            await page.wait_for_timeout(5000)
            
            # Wait for the specific availability element to appear
            element = await page.wait_for_selector(SELECTOR, timeout=20000, state="attached")
            
            if element:
                text = await element.inner_text()
                return text.strip()
            else:
                return "Error: Element found but is empty."
                
        except Exception as e:
            return f"Error: {e}"
        finally:
            await browser.close()
            
def check_termination_condition(status_text: str) -> bool:
    """
    Checks if the GitHub Action should terminate.
    Returns True if termination condition met (Action disabled), False otherwise.
    Condition: Backorder date is earlier than March 31, 2026.
    """
    # Look for patterns like "2026년 3월 31일" or "3월 31일"
    match = re.search(r'(\d+)월\s*(\d+)일', status_text)
    if match:
        month = int(match.group(1))
        day = int(match.group(2))
        
        # Condition: If it's March and the day is earlier than 31st
        if month == 3 and day < 31:
            return True
            
    # Also terminate if it's past March 31st naturally
    current_date = datetime.datetime.now()
    if current_date.year > 2026 or (current_date.year == 2026 and current_date.month > 3):
        return True
        
    return False

if __name__ == "__main__":
    result = asyncio.run(fetch_status())
    print(f"Scraped Data: {result}")
    
    if not result.startswith("Error"):
        is_terminated = check_termination_condition(result)
        print(f"Meets Termination Condition: {is_terminated}")
