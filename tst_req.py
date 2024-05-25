# from langchain_openai import OpenAI
from langchain_community.llms import QianfanLLMEndpoint
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatZhipuAI
from langchain.chains import LLMRequestsChain, LLMChain

from langchain.prompts import PromptTemplate
import os

llm = ChatOpenAI(
    temperature=0.1,
    model="glm-4",
    openai_api_key=os.getenv("ZHIPU_API_KEY"),
    openai_api_base="https://open.bigmodel.cn/api/paas/v4/"
)
# llm = QianfanLLMEndpoint(
#     temperature=0.1
# )
template = """
Between >>> and <<< are the raw search result text from google.
Extract the text content of the article and translate it into Chinese. If the specific article is not included, please say "not found". If the extracted article content contains personal promotional information, please remove it. Please keep the image links and other links in the article. Please translate the entire article. Output in Markdown format
Extracted:
<answer or "not found"
>>>> {requests_result} <<<Extracted:
"""
PROMPT = PromptTemplate(
    input_variables=["requests_result"],
    template=template,
)
chain = LLMRequestsChain(llm_chain=LLMChain(
    llm=llm, prompt=PROMPT))
# question = "What are the Three (3) biggest countries, and their respective sizes?"
inputs = {"url": "https://medium.com/gitconnected/langgraph-gemini-pro-custom-tool-streamlit-multi-agent-application-development-79c1473086b8"}
output = chain(inputs)
print(chain)
print(output)