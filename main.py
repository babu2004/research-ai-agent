from ollama import chat
import re
from tools import calculator, get_time, get_weather,classify_intent 
from research_tool import extract_research_topic,research_topic

model = "qwen2.5-coder:3b"

print("\n=== Autonomous Research AI Assistant ===\n")
print("Type 'exit' to quit.\n")


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

    intent = classify_intent(user_input)

    print(f"\n[Detected Intent]: {intent}")

    # =========================
    # CALCULATOR TOOL
    # =========================

    if intent == "calculator":

        expression = re.sub(r"[^0-9+\-*/().% ]", "", user_input)

        print("\n[Using Calculator Tool]")

        tool_result = calculator(expression)

        print("\nTool Result:")
        print(tool_result)
        
    # =========================
    # TIME TOOL
    # =========================

    elif intent == "time":

        print("\n[Using Time Tool]")

        current_time = get_time()

        print("\nCurrent Time:")
        print(current_time)


    # =========================
    # WEATHER TOOL
    # =========================

    elif intent == "weather":

        print("\n[Using Weather Tool]")

        city = input("Enter city: ")

        weather_result = get_weather(city)

        print("\nWeather Info:")
        print(weather_result)

    # =========================
    # RESEARCH TOOL
    # =========================        

    elif intent == "research":

        print("\n[Using Research Workflow]")

        topic = extract_research_topic(user_input)
        

        report = research_topic(topic)

        print("\nResearch Report:\n")
        print(report)

        # SAVE REPORT

        filename = f"{topic.replace(' ', '_')}_report.txt"

        with open(filename, "w", encoding="utf-8") as file:

            file.write(report)

        print(f"\nReport saved as: {filename}")

    # =========================
    # NORMAL CHAT
    # =========================

    else:

        print("\n[Using AI Chat]")

        conversation_history.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        assistant_response = chat(
            model=model,
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