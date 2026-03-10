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
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080},
            locale='ko-KR',
            timezone_id='Asia/Seoul',
            java_script_enabled=True,
            has_touch=False,
            is_mobile=False
        )
        page = await context.new_page()
        
        # Inject realistic navigator properties
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            Object.defineProperty(navigator, 'languages', {
                get: () => ['ko-KR', 'ko', 'en-US', 'en']
            });
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3]
            });
        """)
        
        # Apply stealth to evade bot detection
        await stealth_async(page)
        
        try:
            # Navigate to the page
            await page.goto(URL, wait_until='domcontentloaded', timeout=45000)
            
            # Wait a bit, then move the mouse to simulate human
            await page.wait_for_timeout(2000)
            await page.mouse.move(x=100, y=100)
            await page.wait_for_timeout(1000)
            await page.mouse.move(x=500, y=500)
            await page.mouse.wheel(delta_x=0, delta_y=300)
            
            # Wait a few more seconds to let any popups or dynamic rendering finish
            await page.wait_for_timeout(5000)
            
            # Additional mouse movement
            await page.mouse.move(x=200, y=200)
            
            # Wait for the specific availability element to appear
            element = await page.wait_for_selector(SELECTOR, timeout=20000, state="attached")
            
            if element:
                text = await element.inner_text()
                return text.strip()
            else:
                return "Error: Element found but is empty."
                
        except Exception as e:
            try:
                await page.screenshot(path="error_screenshot.png")
            except:
                pass
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
