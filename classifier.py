from openai import OpenAI
import os
client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def classify_chunk(text):
    prompt = f"""
    Classify this text into one category:
    HR,IT,Travel,Finance,General

    Text:
    {text[:500]}

    Return ONLY the category."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip().lower()