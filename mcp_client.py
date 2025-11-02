import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters
from groq import Groq
import os
from utils import get_response_from_llm
from dotenv import load_dotenv

load_dotenv()

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
           
            print("Available Tools:",[t.name for t in tools_reponse.tools])

            query = "How to connect to chroma db with langchain in python?"
            library = "langchain"
            res = await session.call_tool(
                "get_docs",
                arguments = {
                    "query": query,
                    "library": library
                }
            )
            print("Tool Response:",res.content)
            context = res.content 

            ## LLM functions to create a human readable answer

            user_prompt_with_context = f"Query:{query}, Conext {context}"

            System_Prompt ="""
               Answer ONLY from the provided context, if information is not available in the context,
               then say 'I don't know'.

               "Keep every 'Source' line exactly; lisyt sources at the end"
            
            """
            
            answer = get_response_from_llm(user_prompt = user_prompt_with_context,
                                            system_prompt=System_Prompt,
                                            model="openai/gpt-oss-20b")
            
            print("Final Answer:",answer)
            


if __name__ == "__main__":
    asyncio.run(main())