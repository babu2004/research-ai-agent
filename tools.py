import datetime
import requests
from ollama import chat
import json

model = 'qwen2.5-coder:3b'

# calculator

def calculator(expression):
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as error:
        return f"Error: {error}"
    
# time

def get_time():
    current_time = datetime.datetime.now()
    return current_time.strftime("%I:%M %p")

# weather


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



# intent   

def classify_intent(user_input):

    classification_prompt = f"""
    You are an advanced intent classification system. Your job is to classify the user's request into EXACTLY ONE category from the list below.

    Available Categories:
    - calculator (For mathematical equations, basic arithmetic, or number solving)
    - weather (For checking temperature, rain, or forecasts)
    - time (For asking the current time, date, or time zones)
    - research (ONLY use this when the user explicitly asks to "generate a report", "write a research paper", or uses the command word "research")
    - chat (For general knowledge, definitions, history questions, casual talk, or translation requests)
    - memory (For when the user asks about saved research or memory)

    Examples for Guidance:
    User: "research machine learning" -> research
    User: "can you generate a research report on solar panels" -> research
    User: "what are the alphabets in tamil" -> chat
    User: "tell me a joke" -> chat
    User: "what is 45 * 2" -> calculator
    User: "is it raining today" -> weather
    User: "retrive the memory" -> memory
    user: "show the saved memory" -> memory 


    Rules:
    1. Respond with ONLY the single lowercase category word from the list.
    2. Absolutely no markdown code blocks, punctuation, or extra explanations.

    User request:
    {user_input}
    """


    response = chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": classification_prompt
            }
        ]
    )

    intent = response["message"]["content"].strip().lower()

    return intent

#=================
# MEMORY FUNCTION
#=================

def load_memory():

    try:
        with open("memory.json", "r", encoding="utf-8") as file:
            return json.load(file)

    except Exception as error:
        print(f"Loading memory failed: {error}")
        return []


def save_memory(memory_data):

    try:
        with open("memory.json", "w", encoding="utf-8") as file:
            json.dump(memory_data, file, indent=4)

    except Exception as error:
        print(f"Failed to save memory: {error}")


def show_memory():

    memory = load_memory()

    if not memory:
        return "\nNo memory found.\n"

    output = ""

    for index, item in enumerate(memory, start=1):
        output += f"\n{index}. {item['title']}"

    return output
    