from ollama import chat
import re
import datetime
import random

print("\n=== Autonomous Research AI Assistant ===\n")
print("Type 'exit' to quit.\n")



# TOOLS


def calculator(expression):
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as error:
        return f"Error: {error}"


def get_time():
    current_time = datetime.datetime.now()
    return current_time.strftime("%I:%M %p")


def random_fact():

    facts = [
        "Python was created by Guido van Rossum.",
        "LLMs predict the next token, not actual thoughts.",
        "AI agents combine reasoning with tools.",
        "RAG stands for Retrieval-Augmented Generation."
    ]

    return random.choice(facts)



# CONVERSATION MEMORY

conversation_history = [
    {
        "role": "system",
        "content": (
            "You are a helpful AI Engineering mentor. "
            "Explain concepts clearly and practically."
        )
    }
]



# MAIN LOOP


while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("\nGoodbye!\n")
        break

    user_lower = user_input.lower()

    print("\n" + "=" * 50)

    
    # CALCULATOR TOOL
    

    math_symbols = ["+", "-", "*", "/", "%"]

    is_math = any(symbol in user_input for symbol in math_symbols)

    if is_math:

        expression = re.sub(r"[^0-9+\-*/().% ]", "", user_input)

        print("\n[Using Calculator Tool]")
        print(f"Expression: {expression}")

        tool_result = calculator(expression)

        print("\nTool Result:")
        print(tool_result)

    
    # TIME TOOL
    

    elif "time" in user_lower:

        print("\n[Using Time Tool]")

        current_time = get_time()

        print("\nCurrent Time:")
        print(current_time)

    
    # RANDOM FACT TOOL
    

    elif "fact" in user_lower:

        print("\n[Using Random Fact Tool]")

        fact = random_fact()

        print("\nRandom Fact:")
        print(fact)

    
    # NORMAL AI CHAT
    

    else:

        print("\n[Using AI Chat]")

        conversation_history.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        assistant_response = chat(
            model="phi3:mini",
            messages=conversation_history
        )

        assistant_text = assistant_response["message"]["content"]

        conversation_history.append(
            {
                "role": "assistant",
                "content": assistant_text
            }
        )

        print("\nAI Response:")
        print(assistant_text)

    print("\n" + "=" * 50 + "\n")