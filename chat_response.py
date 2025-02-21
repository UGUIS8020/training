from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model_name="gpt-4", temperature=0, openai_api_key=openai_api_key)

messages = [HumanMessage(content="自己紹介してください。")]
print(messages)

result = llm.invoke(messages)
print("応答:",result.content)