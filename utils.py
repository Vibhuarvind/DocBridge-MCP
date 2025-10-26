import trafilatura
from playwright.async_api import async_playwright

# Existing function
def clean_html_to_txt(response: str) -> str:
    try:
        extracted = trafilatura.extract(
            response,
            include_comments=False,
            include_tables=False,
            favor_recall=False
        )
        return extracted.strip() if extracted else ""
    except Exception as e:
        raise e

# New function for JS-heavy pages
async def fetch_js_url(url: str) -> str:
    """
    Fetches HTML content of a JS-rendered page using Playwright.
    Args:
        url (str): URL to fetch
    Returns:
        str: Full HTML content after rendering JS
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        content = await page.content()
        await browser.close()
        return content
