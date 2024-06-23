import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from utils.llms import LLMs
import os

st.title("技术文章创作空间")

st.write("欢迎来到技术文章创作空间，让我们一起将复杂的技术概念转化为引人入胜的文章。请提供你的技术背景描述和代码，我将为你撰写一篇精彩的公众号文章。")

background_description = st.text_area("请输入你的背景描述")

code_snippet = st.text_area("请输入你的代码")

def generate_outline(background, code):
    # 调用AI模型生成文章标题和内容
    # 这里可以使用任何适合的AI模型，例如GPT-3或Bard
    # 返回生成的文章标题和内容

    # 定义系统提示词
    system_prompt = PromptTemplate(
        template="""
你是一位经验丰富的技术文章作家,擅长将复杂的技术概念以通俗易懂的方式表述出来,并且能够清晰地展示代码的创作过程。你的任务是根据用户提供的技术背景、思路和代码,撰写一篇公众号文章,使读者能够理解技术的应用场景和实现方法。

文章内容应包括:
1. 背景介绍
2. 概念解释
3. 思路解析
4. 代码实现解析
5. 总结

请确保文章既有深度又有广度,既适合技术专业人士阅读,也适合技术爱好者和普通读者。使用通俗易懂的语言,逻辑清晰,代码部分准确无误。

用户提供的技术背景:
{background}

用户提供的代码实现:
{code}

根据上述信息,请生成这篇文章的大纲，用markdown格式表示。
    """,
        input_variables=["background", "approach", "code"],
    )

    # 定义LLMChain
    llm = LLMs(model_name="glm-3-turbo", temprature=0.1).get_llm()
    outline_chain = LLMChain(prompt=system_prompt, llm=llm)

    # 生成文章
    result = outline_chain.invoke({"background": background, "code": code})

    outline = result["text"]
    return outline

def generate_paragraph(background, code, outline, finished_paragraph=""):
    if finished_paragraph == "":
        system_prompt = PromptTemplate(
            template="""
你是一位经验丰富的技术文章作家,擅长将复杂的技术概念以通俗易懂的方式表述出来,并且能够清晰地展示代码的创作过程。

## 文章大纲为：
{outline}

## 文章写作的背景:
{background}

根据上述信息,请完成大纲中第一部分的文章内容，不要包含其他部分内容。
请使用markdown格式输出。
""",
            input_variables=["background", "approach", "code", "outline"],

        )

    else:
        system_prompt = PromptTemplate(
            template="""
你是一位经验丰富的技术文章作家,擅长将复杂的技术概念以通俗易懂的方式表述出来,并且能够清晰地展示代码的创作过程。你的任务是根据用户提供的技术背景、思路和代码,撰写一篇公众号文章,使读者能够理解技术的应用场景和实现方法。

## 文章大纲为：
{outline}

## 文章写作的背景:
{background}

## 用户提供的代码实现:
{code}

## 已经完成的部分为:
{finished_paragraph}

根据上述信息和已经完成的部分,请续写下一部分内容，不要包含其他部分内容。

## 注意事项：
- 使用markdown格式输出。
- 必严格按照大纲要求流程进行。
- 参照已经完成的部分，不要重复写已经完成的内容。
- 每次只完成一个标题的内容，且把该部分内容写充实。
- 语言要通俗易懂，逻辑要清晰。
- 解析代码的部分要列出代码，且代码引用要准确无误。
- 每一部分的小标题请不要直接使用大纲中的标题，而是要根据大纲内容自行设计。
- 如果文章已经完成，请直接返回“文章已完成”，不要再输出其他任何内容。
    """ ,
            input_variables=["background", "approach", "code", "outline"],

        )

    llm = LLMs(model_name="glm-3-turbo", temprature=0.1).get_llm()
    article_chain = LLMChain(prompt=system_prompt, llm=llm)

    result = article_chain.invoke({"background": background, "code": code, "outline": outline, "finished_paragraph": finished_paragraph})

    paragraph = result["text"]

    return paragraph

def generate_article(background, code):
    outline = generate_outline(background, code)
    finished_paragraph = ""
    article = ""
    while "文章已完成" not in finished_paragraph:
        paragraph = generate_paragraph(background, code, outline, finished_paragraph)
        finished_paragraph += paragraph + "\n\n"
        if "文章已完成" in finished_paragraph:
            break
    article = finished_paragraph
    title = article.split("\n\n")[0]

    return title, article


if st.button("生成文章"):
    # 调用AI模型生成文章
    title, article = generate_article(background_description, code_snippet)
    st.write(title)
    st.text_area("文章内容", article, height=500)

    # 保存文章到文件
    output_folder = "./outputs"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    with open(f"{output_folder}/{title}.md", "w") as file:
        file.write(article)

    st.write("文章已保存到文件")