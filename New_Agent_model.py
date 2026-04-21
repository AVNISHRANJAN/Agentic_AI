from langchain_ollama import ChatOllama
import subprocess
from langchain_core.tools import tool
from langchain.agents import create_react_agent, AgentExecutor

model = ChatOllama(model="gemma4", temperature=0.9)

SYSTEM_PROMPT = """
You are a Docker Expert. You can explain things in 1-2 lines max.
You don't overthink, hallucinate or keep reasoning in a loop.
You Reason -> Act according to user prompt

these are the things you do:
1/ You tell about errors (what went wrong, etc)
2/ You tell about the root cause (What was the cause likely)
3/ You tell about the fix or solution in short
"""

@tool
def show_running_containers():
    """Tool1: Show running Docker containers."""
    result = subprocess.run(["docker", "ps"], capture_output=True, text=True)
    print(f"Return code: {result.returncode}")
    print(f"Standard Output:\n{result.stdout}")
    print(f"Standard Error:\n{result.stderr}")

@tool
def show_docker_logs_by_name(container_name: str):
    """Tool2: Show logs of a specific Docker container."""
    result = subprocess.run(["docker", "logs", container_name], capture_output=True, text=True)
    print(f"Return code: {result.returncode}")
    print(f"Standard Output:\n{result.stdout}")
    print(f"Standard Error:\n{result.stderr}")

tools = [show_running_containers, show_docker_logs_by_name]

user_input = input("Enter your messages:\n")

agent = create_react_agent(model, tools)
agent_executor = AgentExecutor(agent=agent, tools=tools)

response = agent_executor.invoke({
    "messages": [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]
})

print(response["messages"][-1].content)





# from langchain_ollama import Ollama
# import subprocess
# from langchain_core.tools import tool
# from langchain.agents import create_agent

# SYSTEM_PROMPT = """
# You are a Docker Expert. You can explain things in 1-2 lines max.
# You don’t overthink, hallucinate or keep reasoning in a loop.
# You Reason -> Act according to user prompt

# these are the things you do:
# 1/ You tell about errors (what went wrong, etc)
# 2/ You tell about the root cause (What was the cause likely)
# 3/ You tell about the fix or solution in short
# """

# llm = Ollama(model="gemma4", temperature=0.9)


# @tool
# def show_running_containers() -> str:
#     """Tool1: Show running Docker containers."""
#     result = subprocess.run(["docker", "ps"], capture_output=True, text=True)
#     if result.returncode != 0:
#         return f"Return code: {result.returncode}\nStandard Error:\n{result.stderr}"
#     return result.stdout or "No running containers."


# @tool
# def show_docker_logs_by_name(container_name: str) -> str:
#     """Tool2: Show logs of a specific Docker container."""
#     result = subprocess.run(["docker", "logs", container_name], capture_output=True, text=True)
#     if result.returncode != 0:
#         return f"Return code: {result.returncode}\nStandard Error:\n{result.stderr}"
#     return result.stdout or f"No logs found for container: {container_name}"


# tools = [show_running_containers, show_docker_logs_by_name]

# user_input = input("Enter your message:\n")

# agent = create_agent(llm, tools)
# response = agent.invoke(
#     {
#         "messages": [
#             {"role": "system", "content": SYSTEM_PROMPT},
#             {"role": "user", "content": user_input},
#         ]
#     }
# )

# print(response["messages"][-1].content)
