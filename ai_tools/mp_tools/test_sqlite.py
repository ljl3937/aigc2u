# from langchain.agents import create_sql_agent
from langchain.agents import create_json_agent
# from langchain.sql_database import SQLDatabase
from langchain_openai import OpenAI
from langchain_community.llms import QianfanLLMEndpoint
from langchain_community.chat_models import ChatZhipuAI
from langchain_community.agent_toolkits import JsonToolkit
from langchain_community.tools.json.tool import JsonSpec
import os
from do_db import *
import json
from dotenv import load_dotenv

load_dotenv()

articles = get_article_from_date('2024-04-16 00:00:00')

print(articles)
data = {"data": articles}
json_spec = JsonSpec(dict_=data, max_value_length=4000)
json_toolkit = JsonToolkit(spec=json_spec)

# 创建 SQL 代理
# llm = OpenAI(temperature=0.2)
llm = ChatZhipuAI(model="glm-4", temperature=0.1)
json_agent = create_json_agent(llm, toolkit=json_toolkit, verbose=True)

# 运行查询
query = """请从文章列表中找出适合写公众号的参考文章。
* 要求符合AI大模型开发方向
"""
result = json_agent.invoke(query)

print(result)
