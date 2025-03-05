import requests
import json
from dotenv import load_dotenv
import os

# 環境変数の読み込み
load_dotenv()

url = "https://api.openai.com/v1/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + os.environ["OPENAI_API_KEY"]
}

data = {
    "model": "gpt-3.5-turbo-instruct",
    "prompt": "Say hello to the world in a simple sentence.",
    "max_tokens": 100,
    "temperature": 0.722,
    "n": 3
}

response = requests.post(url=url, headers=headers, json=data)
print(json.dumps(response.json(), indent=2))