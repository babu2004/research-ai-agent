from ollama import chat

print("\n=== Autonomous Research AI Assistant ===\n")

user_question = input("Ask something: ")

response = chat(
    model='phi3:mini',
    messages=[
        {
            'role': 'user',
            'content': user_question,
        },
    ]
)

print("\nAI Response:\n")
print(response['message']['content'])