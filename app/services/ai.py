import os
from typing import List
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_groq(messages) -> str:
    """Envia mensagens para o Groq e retorna o texto bruto da resposta."""
    response = client.chat.completions.create(
        # model="llama-3.1-8b-instant",
        model="groq/compound",
        messages=messages,
        temperature=0.7,
    )
    return response.choices[0].message.content or ""
