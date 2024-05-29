from langchain_openai import ChatOpenAI
from langchain_community.llms import Baichuan
from langchain_community.llms import QianfanLLMEndpoint
from langchain_community.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import os


class LLMs:
    def __init__(self, model_name, temprature=0.1):
        self.model_name = model_name
        self.temprature = temprature

    def get_llm(self):
        if self.model_name == "gpt-4":
            llm = ChatOpenAI(
                model_name="gpt-4",
                openai_api_key=os.environ["OPENAI_API_KEY"],
                streaming=False,
                temperature=self.temprature
            )
            return llm
        elif self.model_name == "glm-4" or self.model_name == "glm-3-turbo":
            llm = ChatOpenAI(
                model_name=self.model_name,
                openai_api_base="https://open.bigmodel.cn/api/paas/v4",
                openai_api_key=os.environ["ZHIPU_API_KEY"],
                streaming=True,
                temperature=self.temprature,
                callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
            )
            return llm
        elif self.model_name == "baichuan":
            llm = Baichuan(baichuan_api_key=os.environ["BAICHUAN_API_KEY"])
            return llm
        elif self.model_name == "qianfan":
            llm = QianfanLLMEndpoint(streaming=True, model="ERNIE-Speed")
            return llm
        elif self.model_name == "mistral":
            llm = Ollama(model="mistral")
            return llm
        elif self.model_name == "gemma":
            llm = Ollama(model="gemma:2b")
            return llm
        elif self.model_name == "deepseek":
            llm = ChatOpenAI(
                model_name='deepseek-chat',
                openai_api_base="https://api.deepseek.com",
                openai_api_key=os.environ["DEEPSEEK_API_KEY"],
                max_tokens=1024,
                streaming=True,
                temperature=self.temprature,
                callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
            )
            return llm
