from ollama import chat
import json
import re

print("\n=== Autonomous Research AI Assistant ===\n")
print("Type 'exit' to quit.\n")

def calculator(expression):
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as error:
        return f"Error: {error}"


conversation_history = [
    {
        "role": "system",
        "content": (
            "You are a helpful AI Engineering mentor. "
            "Explain concepts clearly and practically."
        )
    }
]


while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("\nGoodbye!\n")
        break

    # SIMPLE RULE-BASED ROUTER

    math_symbols = ["+", "-", "*", "/", "%"]

    is_math = any(symbol in user_input for symbol in math_symbols)



    if is_math:

        expression_prompt = f"""
you are a AI tool extraction system

your task:
- detect math expression
- retuen only valid JSON format 

Rules:
- output ONLY JSON format
- no explanation
- no markdown 
- no extra text
- no need to mention json in the output  

format :

{{
    "expression": "45 + 34"
}}



user request:
{user_input}
"""

        expression_response = chat(
            model="phi3:mini",
            messages=[
                {
                    "role": "user",
                    "content": expression_prompt
                }
            ]
        )

        raw_response = expression_response["message"]["content"]
        print(f"\n[Raw JSON Response]:\n{raw_response}")
        clean_response = raw_response.replace("```json", "").replace("```", "").strip()

        try:

            parsed_json = json.loads(clean_response)
            expression = parsed_json["expression"]
            print(f"\n[parsed_expression]: {expression}")
            tool_result = calculator(expression)
            print("\nTool Result:\n")
            print(tool_result)

        except Exception as error:

            print("\nJson parsing error:")
            print(error)



    else:

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

        print("\nAI Response:\n")
        print(assistant_text)

    print("\n" + "-" * 50 + "\n")