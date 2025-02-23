import langchain
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate  

langchain.verbose = True

chat = ChatOpenAI(model_name="gpt-4", temperature=0)

template = """
次のコマンドの概要を説明してください

コマンド: {command}
"""
prompt = PromptTemplate(template=template, input_variables=["command"])

chain = LLMChain(llm=chat, prompt=prompt)

result = chain.invoke("ls")

print(result)
