import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

def post_chat_completions(content):
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.environ["OPENAI_API_KEY"]
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role":"user","content":content}],
        "max_tokens": 100,
        "temperature": 0,
    }

    response = requests.post(url=url, headers=headers, json=data)
    print(json.dumps(response.json(), indent=2))

post_chat_completions("Hello! I'm Masahiko")
post_chat_completions("Do you know my name?")