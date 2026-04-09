from openai import OpenAI
import os 

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_answer(query,context):
    prompt=f"""
    You are an  HR assistant.
    Answer ONLY from the context below.
    Context:
    {context}
    Question:
    {query}"""
    response = client.chat.completions.create(model="gpt-4o", messages =[{"role": "user","content":prompt}], temperature=0.2)
    return response.choices[0].message.content
