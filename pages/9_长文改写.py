import streamlit as st
# from langchain.llms import OpenAI
from utils.llms import LLMs
from langchain.prompts import PromptTemplate
from ai_tools.medium import med_art
from langchain.agents import initialize_agent, Tool
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langsmith import traceable
import os

st.title("长文改写")

with st.sidebar:
    if os.environ.get("DEEPSEEK_API_KEY") is None:
        openai_api_key = st.text_input("Deepseek API Key", type="password")
        "[Get an Deepseek API key](https://platform.deepseek.com/)"
    else: 
        openai_api_key = os.environ.get("DEEPSEEK_API_KEY")


@traceable
def generate_response1():
    llm = LLMs(model_name="glm-3-turbo", temprature=0.7).get_llm()
    
    system_prompt = """你是一位创业者。我们将进行一次多轮对话,你需要将一篇商业计划书中针对个人用户的部分改掉，改为针对买我们服务的外国公司，尤其是想要来日本投资，做生意的公司。产品改为为企业提供AI定制解决方案，包括AI生成PPT、AI简历、AI培训、AI阅读、AI人力资源等。定价为每年100万日元取消基础版和专业版。
    请按照以下规则进行:
    1. 我会每次提供文章的一部分内容,你需要将其改写，如不需要改写，请保持原文不变，如果完全不符合以上原则，请重写该部分内容。
    2. 请不要添加任何其他文字即可。
    """
    
    prompt = PromptTemplate(input_variables=["context"], template="{context}")

    if not os.path.exists("articles/outputs"):
        os.makedirs("articles/outputs")
    
    
    with open(f"articles/long_art.md", "r") as f:
        article_markdown = f.read()

    memory = ConversationBufferMemory()
    chain = LLMChain(llm=llm, prompt=prompt, memory=memory)
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0, separators=["\n\n"])
    texts = text_splitter.split_text(article_markdown)

    chinese_translation = ''
    for text in texts:
        result = chain.run(context=system_prompt + text)
        chinese_translation += "\n\n" + result
        st.write(result)
    
    title = chinese_translation.split("#", 1)[1].split("\n", 1)[0]
    with open(f"articles/outputs/{title}.md", "w") as f:
        f.write(chinese_translation)
    return "改写完成"

with st.form("my_form"):
    # text = st.text_input("id:", placeholder="请输入medium文章的id")
    submitted = st.form_submit_button("Submit")
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
    elif submitted:
        # generate_response(text)
        generate_response1()