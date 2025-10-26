import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

server_params = StdioServerParameters(
    command="uv",
    args=["run", "mcp_server.py"],
    env=None
)

async def main():

    async with stdio_client(server_params) as (read_stream, write_stream):

        async with ClientSession(read_stream,write_stream) as sessions:
            
            await sessions.initialize()

            tools_reponse = await sessions.list_tools()
           
            print("Available Tools:",[t.name for t in tools_reponse.tools])

            query = "How to connect to chromadb DB with llama-index in python?"
            library = "llama-index"
            res = await sessions.call_tool(
                "get_docs",
                arguments = {
                    "query": query,
                    "library": library
                }
            )
            print("Tool Response:",res)

if __name__ == "__main__":
    asyncio.run(main())