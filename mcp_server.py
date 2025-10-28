# creating ai web scraping tool
# step 1: search web

import os
import json
import httpx
import asyncio
from fastmcp import FastMCP
from utils import clean_html_to_txt, fetch_js_url
from dotenv import load_dotenv

# query = "TDENGINE DB CONNECTION PYTHON"
load_dotenv()

MCP = FastMCP("MCP Web Scraper Tool")

SERPER_URL = "https://google.serper.dev/search"

# query = "Chroma DB with Pinecone"

async def web_Search(query: str) -> dict | None:     #type hints
    payload = json.dumps({
    "q": query,
    "num": 2
    })

    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        raise ValueError("❌ SERPER_API_KEY not found in .env file")

    headers = {
    'X-API-KEY': str(api_key),
    'Content-Type': 'application/json'
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            SERPER_URL, headers=headers,
            data=payload, timeout=30.0
        )
        response.raise_for_status()
        return response.json()
    

# res = asyncio.run(web_Search(query="Chroma DB"))
# print(res)


# step 2: go and open official documentation only not any other due to security purposes

async def fetch_url(url: str) -> str:
    """
    Fetches and cleans HTML content from a URL.
    Uses static HTTP request by default, 
    and falls back to Playwright for JS-heavy pages.
    """
    try:
        # Static fetch
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=30.0)
            raw_html = response.text

        # Detect JS-heavy page
        if "Enable JavaScript" in raw_html or "Please enable cookies" in raw_html:
            raw_html = await fetch_js_url(url)

        # Clean and return text
        cleaned_response = clean_html_to_txt(raw_html)
        return cleaned_response

    except Exception as e:
        return f"❌ Error fetching URL {url}: {e}"

# step 3: after reading doc debug code accordingly - write tool function based on above supporting functions

docs_urls = {
        "chroma-db":"https://chromadb.readthedocs.io/en/latest/",
        "Pinecone":"https://docs.pinecone.io/docs/quickstart",
        "Langchain":"https://python.langchain.com/docs/",
        "uv":"https://www.uvicorn.org/",
        "Openai":"https://platform.openai.com/docs",
        "llama-index":"https://gpt-index.readthedocs.io/en/latest/",
        "FastAPI":"https://fastapi.tiangolo.com/"
}

# creating tool function    
@MCP.tool()
async def get_docs(query :str, library: str):

    """
    Search to get official latest documentation content based on query and library name 
    supports langchain, openai, chromadb, pinecone, uvicorn, fastapi, llama-index.
    """

    #NORMALIZATIONS
    # ✅ convert library to lowercase for consistent matching
    library = library.lower()

    # ✅ convert keys of docs_urls also temporarily to lowercase for lookup
    lowercased_docs_url = {k.lower(): v for k, v in docs_urls.items()}

    if library not in lowercased_docs_url:
        raise ValueError(f"❌ Library {library} documentation URL not found")

    query = f"site:{lowercased_docs_url[library]} {query}"

    results = await web_Search(query=query)

    if len(results['organic']) == 0:
        return f"❌ No results found for query: {query}"
    
    text_part = []
    for r in results['organic']:
        link = r.get("link", "")
        raw = await fetch_url(link)
        if raw:
            labeled = f"Source: {link}\n{raw}"
            print("Source :", link)
            text_part.append(labeled)
        
    return "\n\n".join(text_part)


def main():
    MCP.run(transport="stdio")

if __name__ == "__main__":
    main()   