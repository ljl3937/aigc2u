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
            # {'ERNIE-3.5-8K-0205', 'ERNIE-Speed', 'ERNIE-3.5-4K-0205',
            # 'ERNIE-Bot', 'Mixtral-8x7B-Instruct', 'ERNIE-3.5-8K-1222',
            # 'CodeLlama-7b-Instruct', 'ERNIE-Speed-128k', 'Llama-2-13b-chat',
            # 'XuanYuan-70B-Chat-4bit', 'SQLCoder-7B', 'AquilaChat-7B',
            # 'Llama-2-7b-chat', 'ERNIE-Bot-turbo', 'BLOOMZ-7B', 'ERNIE-Bot-8k',
            # 'Qianfan-Chinese-Llama-2-7B', 'Yi-34B-Chat', 'ChatGLM2-6B-32K',
            # 'EB-turbo-AppBuilder', 'Llama-2-70b-chat', 'ERNIE-Bot-4',
            # 'Qianfan-BLOOMZ-7B-compressed', 'ChatLaw', 'Qianfan-Chinese-Llama-2-13B'}
            llm = QianfanLLMEndpoint(streaming=True, model="ERNIE-Speed")
            return llm
        elif self.model_name == "mistral":
            llm = Ollama(model="mistral")
            return llm
        elif self.model_name == "gemma":
            llm = Ollama(model="gemma:2b")
            return llm
