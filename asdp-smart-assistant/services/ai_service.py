import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
Anda adalah asisten virtual resmi ASDP.
Jawab dengan ramah, profesional, dan ringkas.
Tolak pertanyaan di luar konteks layanan penyeberangan ASDP.
"""

def get_ai_response(messages):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *messages
            ],
            temperature=0.2
        )
        return response.choices[0].message.content
    except:
        return "Maaf, sistem sedang mengalami gangguan. Silakan coba kembali."