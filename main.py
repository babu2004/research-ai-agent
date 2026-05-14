from ollama import chat

print("\n=== Autonomous Research AI Assistant ===\n")
print("Type 'exit' to quit.\n")

conversation_history = [
    {
        "role": "system",
        "content": (
            "You are a helpful AI Engineering mentor. "
            "Explain concepts simply and practically. "
            "Focus on AI engineering, LLMs, agents, and startups."
        )
    }
]

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("\nGoodbye!\n")
        break

    conversation_history.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    response = chat(
        model="phi3:mini",
        messages=conversation_history
    )

    assistant_message = response["message"]["content"]

    conversation_history.append(
        {
            "role": "assistant",
            "content": assistant_message
        }
    )

    print("\nAI Assistant:\n")
    print(assistant_message)
    print("\n" + "-" * 50 + "\n")