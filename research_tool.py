from ollama import chat

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


# Research

def research_topic(topic):
    research_prompt = f"""
    You are an expert research analyst. Write a comprehensive, beginner-friendly research report on the topic provided below.

    Topic: {topic}

    The report MUST be structured with the following exact Markdown headers:
    # Research Report: {topic}

    ## Overview
    Provide a clear, high-level summary of what this topic is, its core definition, and why it matters today. Keep it to 1-2 paragraphs.

    ## Key Concepts
    Define 3-4 foundational terms, rules, or pillars critical to understanding this topic. Use bullet points with bold text for the terms. Do not add introductory or concluding fluff to this section.

    ## Real-World Applications
    Provide 2-3 concrete, current examples of how this topic is actively used in the industry today. Use brief, punchy subheadings for each example.

    ## Future Trends
    Highlight upcoming technological advancements, potential challenges/blockers, or developments expected in the next 5-10 years.

    Writing Requirements:
    1. Tone: Professional yet accessible to a beginner. Avoid overly dense academic jargon.
    2. Format: Use Markdown elements (bolding, bullet points) to maximize scannability.
    3. Content: Ensure each section contains distinct, non-overlapping information. Do not repeat facts across sections.
    4. Output: Return ONLY the structured Markdown report. Do not include conversational intro/outro text (like "Sure, here is your report").
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

    return response["message"]["content"]

