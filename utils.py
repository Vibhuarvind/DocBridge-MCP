import trafilatura
import os
from dotenv import load_dotenv
from groq import Groq
from playwright.async_api import async_playwright

load_dotenv()

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
        # debug(f"content fetched {url}: {content[:500]}")
        return content
    
def get_response_from_llm(user_prompt, system_prompt,model):

    api_key = os.getenv("GROQ_API_KEY")
    groq_client = Groq(api_key=api_key)

    chat_completion = groq_client.chat.completions.create(
            messages = [
                {"role":"system","content": system_prompt},
                {"role":"user","content": user_prompt},
            ],
        model=model,
    )
    return chat_completion.choices[0].message.content

# testing the function call
# print(get_response_from_llm(user_prompt="what is capital of India?", 
#                               system_prompt="You are a helpful assistant.", 
#                                   model="openai/gpt-oss-20b"))