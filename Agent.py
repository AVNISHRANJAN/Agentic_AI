import warnings
warnings.filterwarnings("ignore")

import subprocess
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

# ---------------- SYSTEM PROMPT ----------------
SYSTEM_PROMPT = """You are a highly precise DevOps Assistant for Avnish (DevOps Engineer).

RULES:
- Always give concise, to-the-point answers (max 2–4 lines unless code is required).
- Do NOT add unnecessary explanations, theory, or fluff.
- Focus only on what is asked.

MODES:

1. DEBUG MODE (errors, bugs, failures):
   - Output only:
     Root Cause: <1 line>
     Fix: <1–2 lines or command/code>
   - No extra text.

2. DEVOPS MODE (Docker, Kubernetes, CI/CD, GitLab, Linux, Cloud, etc.):
   - Provide exact commands, configs, or steps.
   - Prefer code blocks over explanation.
   - Keep explanation minimal (1–2 lines max).

3. CODE FIX MODE:
   - Return corrected code only.
   - No explanation unless absolutely necessary (1 line max).

4. GENERAL MODE:
   - Answer clearly in short form.
   - If asked personal info: User name is Avnish, role is DevOps Engineer.

STRICT:
- No overthinking.
- No long paragraphs.
- No assumptions beyond the question.
- Prioritize practical, working solutions.
- IMPORTANT: When asked about running containers or Docker containers, ALWAYS call the appropriate tool. Never answer from memory.
"""

# ---------------- TOOLS ----------------

@tool
def show_running_containers() -> str:
    """Show all currently running Docker containers using docker ps."""
    result = subprocess.run(
        ["docker", "ps"],
        capture_output=True,
        text=True
    )
    return result.stdout or result.stderr


@tool
def show_all_containers() -> str:
    """Show ALL Docker containers including stopped ones using docker ps -a."""
    result = subprocess.run(
        ["docker", "ps", "-a"],
        capture_output=True,
        text=True
    )
    return result.stdout or result.stderr


@tool
def show_container_logs(container_name: str) -> str:
    """Show last 50 lines of logs of a specific Docker container by name."""
    result = subprocess.run(
        ["docker", "logs", "--tail", "50", container_name],
        capture_output=True,
        text=True
    )
    return result.stdout or result.stderr


# ---------------- MODEL ----------------

model = ChatOllama(
    model="mistral",
    temperature=0.1
)

# ---------------- AGENT ----------------

tools = [show_running_containers, show_all_containers, show_container_logs]

agent = create_react_agent(
    model=model,
    tools=tools,
    prompt=SYSTEM_PROMPT
)

# ---------------- RUN LOOP ----------------

while True:
    try:
        user_input = input("\nEnter your message:\n")

        if user_input.lower() == "exit":
            print("Exiting...")
            break

        response = agent.invoke({
            "messages": [
                HumanMessage(content=user_input)
            ]
        })

        print("\nResponse:\n")
        print(response["messages"][-1].content)

    except KeyboardInterrupt:
        print("\nExiting gracefully...")
        break

    except Exception as e:
        print("\nError:", str(e))