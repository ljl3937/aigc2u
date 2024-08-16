import streamlit as st
from playwright.sync_api import sync_playwright
from utils.llms import LLMs
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def run(playwright, url):
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://www.baidu.com/
    # page.goto("https://docs.qq.com/aio/p/scxmsn78nzsuj64?p=LyUhXC9azxBeh7GJ0TtA9SG")
    page.goto(url)
    # 等待页面加载完成
    page.wait_for_load_state("networkidle")

    # Click input[name="wd"]
    # content = page.locator("#sc-page-content").inner_html()
    # content = page.locator("#sc-sidebar-section").inner_html()
    # 获取页面内容
    content = page.inner_html("body")

    print(content)
    context.close()
    browser.close()
    return content

if __name__ == '__main__':
    st.title("Scrapfly Test")
    doc_html = ""
    if 'doc' not in st.session_state:
        st.session_state.doc = ""
    with st.form("get_markdown"):
        url = st.text_input("Url:", "",placeholder="Please enter the url")
        submitted = st.form_submit_button("Submit")
        # if not openai_api_key:
        #     st.info("Please add your OpenAI API key to continue.")
        if submitted:
            with sync_playwright() as playwright:
                doc_html = run(playwright, url)
                llm = LLMs(model_name="deepseek", temprature=0.7).get_llm()
                prompt = ChatPromptTemplate.from_template("请提取以下html中的文章文本内容：\n\n{content}\n\n请将提取的内容以markdown格式输出，文中的图片链接保留,并且包括隐藏标签的内容，注意，只提取文章内容：")
                output_parser = StrOutputParser()
                chain = prompt | llm | output_parser
                doc_stream = chain.stream({"content": doc_html})
                st.session_state.doc = st.write_stream(doc_stream)
    st.session_state.key = 'value'
    print(st.session_state.doc)


