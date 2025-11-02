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

DEBUG_FILE = open("debug_server.log", "w", encoding="utf-8")

def debug(msg):
    DEBUG_FILE.write(f"{msg}\n")
    DEBUG_FILE.flush()

MCP = FastMCP("MCP Web Scraper Tool",debug=True)

SERPER_URL = "https://google.serper.dev/search"

# query = "Chroma DB with Pinecone"

async def web_Search(query: str) -> dict | None:     #type hints
    payload = json.dumps({
    "q": query,
    "num": 2
    })
    debug('-'*60)
    debug(f"SERPER payload: {payload}")
    debug('-'*60)

    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        raise ValueError("❌ SERPER_API_KEY not found in .env file")

    headers = {
    'X-API-KEY': str(api_key),
    'Content-Type': 'application/json'
    }
    debug('-'*60)
    debug(f"SERPER headers: {headers}")
    debug('-'*60)

    async with httpx.AsyncClient() as client:
        response = await client.post(
            SERPER_URL, headers=headers,
            data=payload, timeout=30.0
        )
        response.raise_for_status()
        debug('-'*60)
        debug(f"SERPER response: {response.text[:500]}")
        debug('-'*60)
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
            # Force UTF-8 encoding
            response.encoding = 'utf-8'
            raw_html = response.text

        # Detect JS-heavy page
        if "Enable JavaScript" in raw_html or "Please enable cookies" in raw_html:
            raw_html = await fetch_js_url(url)

        # Clean and return text
        cleaned_response = clean_html_to_txt(raw_html)

        # If trafilatura returns nothing, use fallback
        if not cleaned_response or len(cleaned_response.strip()) == 0:
            import re
            # Fallback: Remove HTML tags and clean up
            text = re.sub('<[^<]+?>', '', raw_html)
            text = re.sub(r'\s+', ' ', text)
            text = text.strip()[:5000]
            cleaned_response = text
        
        cleaned_response = cleaned_response.encode('utf-8', errors='replace').decode('utf-8')

        #Ensure the response is valid UTF-8 and doesn't have problematic chars
        # Replace any problematic characters
        return cleaned_response

    except Exception as e:
        return f"❌ Error fetching URL {url}: {e}"


# async def fetch_url(url: str) -> str:
#     """
#     Fetches and cleans HTML content from a URL.
#     Handles encoding issues properly.
#     """
#     try:
#         async with httpx.AsyncClient() as client:
#             response = await client.get(url, timeout=30.0)
#             # Force UTF-8 encoding
#             response.encoding = 'utf-8'
#             raw_html = response.text

#         # Detect JS-heavy page
#         if "Enable JavaScript" in raw_html or "Please enable cookies" in raw_html:
#             raw_html = await fetch_js_url(url)

#         # Clean and return text
#         cleaned_response = clean_html_to_txt(raw_html)
        
#         # If trafilatura returns nothing, use fallback
#         if not cleaned_response or len(cleaned_response.strip()) == 0:
#             import re
#             # Fallback: Remove HTML tags and clean up
#             text = re.sub('<[^<]+?>', '', raw_html)
#             text = re.sub(r'\s+', ' ', text)
#             text = text.strip()[:5000]
#             cleaned_response = text
        
#         # Ensure the response is valid UTF-8 and doesn't have problematic chars
#         # Replace any problematic characters
#         cleaned_response = cleaned_response.encode('utf-8', errors='replace').decode('utf-8')
        
#         return cleaned_response

#     except Exception as e:
#         return ""f"❌ Error fetching URL {url}: {e}"
    
# step 3: after reading doc debug code accordingly - write tool function based on above supporting functions

docs_urls = {
    "chroma-db": "chromadb.readthedocs.io",
    "pinecone": "docs.pinecone.io",
    "langchain": "python.langchain.com",
    "uvicorn": "uvicorn.org",
    "openai": "platform.openai.com",
    "llama-index": "gpt-index.readthedocs.io",
    "fastapi": "fastapi.tiangolo.com"
}

debug('-'*60)
debug(f"Docs URLs: {docs_urls.keys()}")

# creating tool function    
@MCP.tool()
async def get_docs(query :str, library: str):

    """
    Search to get official latest documentation content based on query and library name 
    supports langchain, openai, chromadb, pinecone, uvicorn, fastapi, llama-index.

    Args:
        query (str): The query to find e.g. "Build a REST API endpoint to upload files".
        library (str): The library to be searched is e.g. "fastapi".
    
    Returns:
        str: Summarized content from official documentation.

    """

    #NORMALIZATIONS
    # convert library to lowercase for consistent matching
    library = library.lower()

    # convert keys of docs_urls also temporarily to lowercase for lookup
    lowercased_docs_url = {k.lower(): v for k, v in docs_urls.items()}

    debug('-'*60)
    debug(f"Lowercased Docs URLs keys: {lowercased_docs_url.keys()}")
    debug(f"Lowercased Docs urls: {lowercased_docs_url}")
    debug(f'lowercased library: {library}')
    debug('-'*60)

    # we dont wanrt to scrape general docs, but official docs reponses should be received from web search
    # if tool not found in docs then create general responses
    if library not in lowercased_docs_url:
        raise ValueError(f"❌ Library {library} documentation URL not found")
    
    debug('-'*60)
    debug(f"Searching docs for library: {library}, query: {query}")
    debug('-'*60)
    
    # strategy to get what we want => _python.langchain.com/docs/ chromadb connection
    query = f"site:{lowercased_docs_url[library]} {query}"

    debug('-'*60)
    debug(f"Strategy Query being searched: {query}")
    debug('-'*60)

    results = await web_Search(query=query)

    debug('-'*60)
    debug(f"Web Search Results: {results}")
    debug('-'*60)

     # if we dont get any results
    if len(results['organic']) == 0:
        return f"❌ No results found for query: {query}"
    
    text_part = []
    for r in results['organic']:
        link = r.get("link", "") # getting link from each organic result
        raw = await fetch_url(link)

        # we want to see authentic info, so need to see from which url we are getting content
        if raw:
            labeled = f"Source: {link}\n{raw}"
            print("Source :", link)
            text_part.append(labeled)
    
    debug('-'*60)
    debug(f"Fetched and cleaned text parts: {text_part}")
    debug('-'*60)
        
    return "\n\n".join(text_part)

def main():
    MCP.run(transport="stdio")

if __name__ == "__main__":
    main()   