import requests
import json
from dotenv import load_dotenv
import os

# 環境変数から API キーを読み込み
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY が設定されていません")

url = "https://api.openai.com/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai_api_key}"
}

data = {
    "model": "gpt-3.5-turbo",  # モデル名を修正
    "messages": [
        {"role": "user", "content": "こんにちは"}
    ]
}

response = requests.post(url=url, headers=headers, data=json.dumps(data))
print(response)
print(json.dumps(response.json(), indent=2))
