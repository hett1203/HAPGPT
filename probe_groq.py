import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path('.env'))
from groq import Groq
client = Groq(api_key=os.getenv('GROQ_API_KEY') or os.getenv('API_KEY'))
for model in ['openai/gpt-oss-120b', 'llama-3.3-70b-versatile', 'llama-3.1-8b-instant', 'mistral-saba-24b']:
    try:
        r = client.chat.completions.create(model=model, messages=[{'role':'user','content':'hi'}])
        print(model, 'OK', r.choices[0].message.content[:120])
    except Exception as e:
        print(model, 'ERROR', type(e).__name__, e)
