from ollama import chat
from ddgs import DDGS
import json

model = 'qwen2.5-coder:3b'

# topic extraction

def extract_research_topic(user_input):
    extraction_prompt=f"""

    you are a topic extraction system.

    Extract only the research topic from the user's request.

    Rules:
    - Return only the topic
    - No explanation
    - No extra text

    Examples:

    User: research AI agents
    Topic: AI agents

    User: create a report on machine learning
    Topic: machine learning

    User: tell me about vector databases
    Topic: vector databases


    user request:
    {user_input}

    """
    respond = chat(
        model = model,
        messages = [
            {
                "role":"user",
                "content": extraction_prompt
            }
        ]
    )

    topic = respond["message"]["content"].strip()

    return topic


# Web Search 

def web_search(query):

    results_text = ""

    with DDGS() as ddgs:
        
        results = ddgs.text(query, max_results=5)

        for index, result in enumerate(results, start=1):

            title = result["title"]

            body = result["body"]

            results_text += (
                f"\n Result {index}: \n"
                f"Title: {title}\n"
                f"snippet: {body}\n"
            )

    return results_text
        


# Research

def research_topic(topic):

    print("\n[Searching web...]")

    web_results = web_search(topic)

    research_prompt = f"""
    You are an expert research analyst. Your task is to extract, analyze, and format a comprehensive, beginner-friendly research report into a strict JSON object.

    Topic: {topic}
    Web Search Context:
    {web_results}

    You must return a valid JSON object matching this exact structure:
    {{
        "title": "Research Report: {topic}",
        "overview": "Clear, high-level summary of what this topic is, its core definition, and why it matters today. Exactly 1-2 paragraphs.",
        "key_concepts": [
            "**Term 1**: Definition of the first foundational concept, rule, or pillar critical to understanding this topic.",
            "**Term 2**: Definition of the second foundational concept.",
            "**Term 3**: Definition of the third foundational concept."
        ],
        "applications": [
            "**Application 1 **: A concrete, current example of how this topic is actively used in the industry today.",
            "**Application 2 **: A second current real-world example."
        ],
        "future_trends": [
            "A highlight of an upcoming technological advancement or development expected in the next 5-10 years.",
            "A description of a potential challenge, blocker, or ethical consideration facing the topic."
        ]
    }}

    Content & Quality Requirements:
    1. Tone: Professional yet accessible to a beginner. Avoid overly dense academic jargon.
    2. Format: Use Markdown elements like **bolding** *inside* the JSON string values to maximize scannability for the array items.
    3. Content: Ensure each field contains distinct, non-overlapping information. Do not repeat facts across sections.
    4. Data Integrity: Rely on the provided Web Search Context to pull factual, current, and concrete data points.

    Output Rules:
    - Return ONLY the raw, valid JSON object.
    - Do NOT wrap the JSON in markdown code blocks (e.g., do not use ```json ... ```).
    - Do NOT include any conversational intro/outro text, markdown titles, or explanations outside the JSON object.
    """

    response = chat(
        model = model,
        messages = [
            {
                "role":"user",
                "content": research_prompt
            }
        ]
    )

    output = response["message"]["content"]
    clean_output = (
    output
    .replace("```json", "")
    .replace("```", "")
    .strip()
)

    try:
        parsed_json = json.loads(clean_output,strict = False)
        
        return parsed_json
    
    except Exception as error:
        print("\nJSON Parsing Error: ")
        print(error)
        
        return {
            "title": topic,
            "overview": "JSON parsing failed.",
            "key_concepts": [],
            "applications": [],
            "future_trends": []
        }




