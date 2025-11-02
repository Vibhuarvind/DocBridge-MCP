
import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters
from groq import Groq
from utils import get_response_from_llm
from dotenv import load_dotenv

load_dotenv()

DEBUG_FILE = open("debug_client.log", "w", encoding="utf-8")

def debug(msg):
    DEBUG_FILE.write(f"{msg}\n")
    DEBUG_FILE.flush()

import sys
sys.stdout.reconfigure(encoding='utf-8')


server_params = StdioServerParameters(
    command="uv",
    args=["run", "mcp_server.py"],
    env=None
)

async def main():

    async with stdio_client(server_params) as (read_stream, write_stream):

        async with ClientSession(read_stream,write_stream) as session:
            
            await session.initialize()

            tools_reponse = await session.list_tools()
           
            debug(f"Available Tools: {[t.name for t in tools_reponse.tools]}")

            query = "How to use Chroma DB with Langchain"
            library = "langchain"
            res = await session.call_tool(
                "get_docs",
                arguments = {
                    "query": query,
                    "library": library
                }
            )
            debug(f'Called tool get_docs with query: {query} and library: {library}')
            debug('-'*60)
            debug(f"Tool Response: {res.content}")
            debug('-'*60)
            context = res.content[0].text if res.content else ""
            debug(f"Context fetched: {context}")
            debug('-'*60)

            ## LLM functions to create a human readable answer

            user_prompt_with_context = f"Query:{query}, Conext {context}"
            debug(f"User Prompt with Context: {user_prompt_with_context}")
            debug('-'*60)

            System_Prompt ="""
               Answer ONLY from the provided context, if information is not available in the context,
               then say 'I don't know'.

               "Keep every 'Source' line exactly; list sources at the end"
            """
            answer = get_response_from_llm(user_prompt = user_prompt_with_context,
                                            system_prompt=System_Prompt,
                                            model="openai/gpt-oss-20b")
            debug(f"Final Answer: {answer}")
            debug('-'*60)
            print("Final Answer:",answer)

if __name__ == "__main__":
    asyncio.run(main())