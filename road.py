import ollama

response = ollama.chat(
    model='llava',
    messages=[
        {
            'role': 'user',
            'content': 'Analyze this road image and tell if there is a crack or pothole. Give short answer.',
            'images': ['/home/avnish/Agentic_Ai/test.png']
        }
    ]
)

print(response['message']['content'])