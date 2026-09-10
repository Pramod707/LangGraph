from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")


async def main():
    client = MultiServerMCPClient({
        "math": {
            "command": "python",
            "args": ["mathserver.py"],
            "transport": "stdio",
        },
        "weather": {
            "url": "http://127.0.0.1:8000/mcp",
            "transport": "streamable-http",
        },
    })

    tools = await client.get_tools()
    model = ChatGroq(model="qwen/qwen3.8-27b")
    agent = create_agent(model, tools)

    math_response = await agent.ainvoke({
        "messages": [{"role": "user", "content": "what is (3+6)^3"}]
    })

    print("maths res: ", math_response["messages"][-1].content)


asyncio.run(main())
