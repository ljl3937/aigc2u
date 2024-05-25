import requests
from langchain.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

load_dotenv()

# 定义自定义工具

class Input(BaseModel):
    id: str = Field(..., title="文章id", description="Medium文章的id")

class GetMediumTool(BaseTool):
    name = "custom_api_tool"
    description = "一个用于根据文章id获取medium文章的工具"
    args_schema: Type[BaseModel] = Input

    def _run(self, article_id: str) -> str:
        """使用该工具调用API"""
        base_url = "https://medium2.p.rapidapi.com"
        headers = {
            "X-RapidAPI-Key": os.environ.get("RAPID_API_KEY"),
            "X-RapidAPI-Host": "medium2.p.rapidapi.com"
        }
        url = f"{base_url}/article/{article_id}/markdown"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        result = response.json()['markdown']
        print(type(result))
        return result

    def run(self, article_id: str, verbose: bool = False, color: str = 'black', callbacks=None, llm_prefix='', observation_prefix='') -> str:
        """调用工具的入口函数"""
        if 'Observation:' in article_id:
            import json
            dict_data = json.loads(article_id.replace('\nObservation:', '').replace("'", "\""))
            article_id = dict_data['article_id']
        # 判断article_id是个json字符串
        if isinstance(article_id, dict):
            article_id = article_id['article_id']
        return self._run(article_id)

# # 使用自定义工具
# api_tool = GetMediumTool()
# id = "110844f22a1a"
# result = api_tool.run(id)
# print(result) # 输出API响应
