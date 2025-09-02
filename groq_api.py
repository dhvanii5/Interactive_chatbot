import requests
from config import GROQ_API_KEY

def get_groq_response(user_query, system_prompt=None):
    """Get a response from Groq API"""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    messages.append({"role": "user", "content": user_query})

    data = {
        "model": "llama3-70b-8192",
        "messages": messages,
        "temperature": 0.5,
        "max_tokens": 250
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"
