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

st.title("翻译Medium")

with st.sidebar:
    if os.environ.get("DEEPSEEK_API_KEY") is None:
        openai_api_key = st.text_input("Deepseek API Key", type="password")
        "[Get an Deepseek API key](https://platform.deepseek.com/)"
    else: 
        openai_api_key = os.environ.get("DEEPSEEK_API_KEY")

@traceable
def generate_response(input_text):
    llm = LLMs(model_name="glm-3-turbo", temprature=0.7).get_llm()
    # llm = OpenAI(temperature=0.7)
    template = """作为一名技术文章翻译专家。
以下====和====之间是英文Markdown文章片段:
=====
{article_markdown} 
=====
请将其翻译成中文。
翻译结果不要私自添加多余的markdown标记，保持原文的markdown格式。
翻译结果只输出markdown格式的翻译结果，不要包含任何其他内容（包括解释文字）。
    """
    prompt = PromptTemplate(input_variables=["article_markdown"], template=template)
    medium_tool = med_art.GetMediumTool()
    # tools = [
    #     medium_tool
    # ]
    # agent = initialize_agent(tools, llm, agent="zero-shot-react-description")
    # # article_markdown = agent.run(f"获取以下 id 的 Markdown 内容: {input_text}")
    # article_markdown = agent.run(f"获取id为{input_text}的Medium文章的Markdown内容并翻译成中文,输出格式还是markdown，请直接输出结果，不要有多余的文字。")

    memory = ConversationBufferMemory()
    chain = LLMChain(llm=llm, prompt=prompt, memory=memory)
    # 如果article.md存在，就直接读取，如果不存在，则写入
    if os.path.exists(f"articles/{input_text}.md"):
        with open(f"articles/{input_text}.md", "r") as f:
            article_markdown = f.read()
    else:
        with open(f"articles/{input_text}.md", "w") as f:
            article_markdown = medium_tool.run(input_text)
            f.write(article_markdown)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0, separators=["\n\n"])
    texts = text_splitter.split_text(article_markdown)

    chinese_translation = ''
    st.write("```markdown\n")
    for text in texts:
        result = chain.run(text)
        if result.startswith("```markdown"):
            result = result.split("\n", 1)[1]
            result = result.rsplit("\n", 1)[0]
        chinese_translation += "\n\n" + result
        title = result.split("\n", 1)[0].split(" ", 1)[1]
        with open(f"articles/output/{title}.md", "w") as f:
            f.write(result)
        st.write(result)

    # chinese_translation = chain.run(article_markdown)
    # while "已翻译结束" not in chinese_translation:
    #     human_input = "继续"
    #     chinese_translation += chain.run(human_input=human_input)
    # st.write(chinese_translation)
    st.write("\n```")
    return


@traceable
def generate_response1(input_text):
    llm = LLMs(model_name="glm-3-turbo", temprature=0.7).get_llm()
    
    system_prompt = """你是一位专业的技术文章翻译专家。我们将进行一次多轮对话,你需要将一篇英文 Markdown 文章翻译成中文。
    请按照以下规则进行:
    1. 我会每次提供文章的一部分内容,你需要将其翻译成中文。
    2. 请不要添加任何其他文字即可。
    """
    
    prompt = PromptTemplate(input_variables=["context"], template="{context}")
    
    # 如果article.md存在，就直接读取，如果不存在，则写入
    if os.path.exists(f"articles/{input_text}.md"):
        with open(f"articles/{input_text}.md", "r") as f:
            article_markdown = f.read()
    else:
        with open(f"articles/{input_text}.md", "w") as f:
            medium_tool = med_art.GetMediumTool()
            article_markdown = medium_tool.run(input_text)
            f.write(article_markdown)

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
        f.write(result)
    return "翻译完成"

with st.form("my_form"):
    text = st.text_input("id:", placeholder="请输入medium文章的id")
    submitted = st.form_submit_button("Submit")
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
    elif submitted:
        # generate_response(text)
        generate_response1(text)