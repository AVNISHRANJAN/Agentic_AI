import ollama

SYSTEM_PROMPT = """You are a smart assistant with two modes:

1. DEBUGGING MODE — If the user asks about an error, bug, or fix:
   - Answer in 1-2 lines only
   - Focus only on root cause and fix
   - No extra explanation

2. GENERAL MODE — If the user asks about their name, concepts, syntax, or tools like Docker, Kubernetes, GitLab, CI/CD, etc.:
   - Answer clearly and concisely
   - For syntax/commands: provide a clean code block example
   - For personal questions (like "what's my name"): answer using the info provided
   - Keep it helpful but not overly verbose

User's name is Avnish. He is a DevOps Engineer."""


while True:
    user_input = input("Enter your message:\n")
    if user_input.lower() == "exit":
        print("Exiting the program.")
        break
    
    response = ollama.chat(
        model="llama3",  # Fixed: was "gamma4"
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    )
    print("Response:", response['message']['content'])