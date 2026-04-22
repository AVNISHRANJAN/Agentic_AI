import asyncio
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama import ChatOllama

async def main():
    #this brings up the MCP server and fetches the tools from it
    client = MultiServerMCPClient( 
        {
            "docker-mcp": {
                "transport": "stdio",
                "command": "/home/avnish/Agentic_Ai/venv/bin/python3",
                "args": ["/home/avnish/Agentic_Ai/mcp_server.py"],
            },
        }
    )

    tools = await client.get_tools()

    llm = ChatOllama(model="llama3", temperature=0.7)

    agent = create_agent(
        llm,
        tools
    )

    response = await agent.invoke({
        "messages": [
            {"role": "user", 
            "content": "how many containers are running?"}
        ]
    })

    print(response["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())
