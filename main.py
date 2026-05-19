from ollama import chat
import re
import datetime
import requests
import os
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
print(WEATHER_API_KEY)
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


def get_weather(city):

    url = f"https://wttr.in/{city}?format=j1"

    response = requests.get(url)

    data = response.json()

    try:

        current = data["current_condition"][0]

        temperature = current["temp_C"]

        description = current["weatherDesc"][0]["value"]

        humidity = current["humidity"]

        return (
            f"City: {city}\n"
            f"Temperature: {temperature}°C\n"
            f"Weather: {description}\n"
            f"Humidity: {humidity}%"
        )

    except Exception as error:

        return f"Weather data not found: {error}"

def classify_intent(user_input):

    classification_prompt = f"""
You are an intent classifier.

Your job is to classify the user's request into ONE category only.

Categories:
- calculator
- weather
- time
- chat

Rules:
- Respond with ONLY one category word.
- No explanations.
- No extra text.

User request:
{user_input}
"""

    response = chat(
        model="phi3:mini",
        messages=[
            {
                "role": "user",
                "content": classification_prompt
            }
        ]
    )

    intent = response["message"]["content"].strip().lower()

    return intent


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