from langchain.prompts import PromptTemplate

template ="""
次のコマンドの概要を説明してください

コマンド: {command}
"""

prompt = PromptTemplate(
    template=template,
    input_variables=["command"]
)

result = prompt.format(command="ls")

print(result)

