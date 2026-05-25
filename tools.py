import datetime
import requests
from ollama import chat

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



 




# topic extraction 


# intent   

def classify_intent(user_input):

    classification_prompt = f"""
You are an intent classifier.

Your job is to classify the user's request into ONE category only.
- Use "research" when the user asks to research a topic or generate a report.

Categories:
- calculator
- weather
- time
- chat
- research 

Rules:
- Respond with ONLY one category word.
- No explanations.
- No extra text.

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
