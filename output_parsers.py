import langchain
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field, validator
from typing import List

langchain.verbose = True

chat = ChatOpenAI(model="gpt-4", temperature=0)

class Rrecipe(BaseModel):
    ingredients: List[str] = Field(description="ingredients of the dish")
    steps: List[str] = Field(description="steps to make the dish")

template = """料理のレシピを教えてください

{format_instructions}

料理名: {dish}

"""

parser = PydanticOutputParser(pydantic_object=Rrecipe)

prompt = PromptTemplate(
    template=template,
    input_variables=["dish"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

print(parser.get_format_instructions())

chain = LLMChain(llm=chat, prompt=prompt)

output = chain.invoke({"dish": "カレー"})
print(output)

output_text = output['text']  # 'text' フィールドを抽出
recipe = parser.parse(output_text)  # 文字列としてパース
print(recipe)
print(type(recipe))
