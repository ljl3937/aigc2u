import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from utils.llms import LLMs
import os, json

st.title("知乎问答助手")

st.write("欢迎来到知乎问答助手，输入知乎问题，我来帮你回答。")

question = st.text_area("请输入知乎问题")

def generate_outline(question):
    system_prompt = PromptTemplate(
        template="""
你是一位经验丰富的知乎问答技术专家,擅长将复杂的技术概念以通俗易懂的方式表述出来。你的任务是根据用户提供的知乎问题,撰写一篇知乎高赞回答,使读者能够得到自己想要的答案。

请确保文章既有深度又有广度,既适合技术专业人士阅读,也适合技术爱好者和普通读者。使用通俗易懂的语言,逻辑清晰,代码部分准确无误。

用户提供的知乎问题:
{question}

根据上述信息,请生成这篇文章的大纲，用json树形结构表示，标题用title,描述用description,子级数组用children,最多二级结构。
    """,
        input_variables=["background", "approach", "code"],
    )

    # 定义LLMChain
    llm = LLMs(model_name="deepseek", temprature=0.1).get_llm()
    outline_chain = LLMChain(prompt=system_prompt, llm=llm)

    # 生成文章
    result = outline_chain.invoke({"question": question})
    # result = st.write_stream(stream_res)

    outline = result["text"]
    st.write("以下是文章的大纲：\n" + outline)
    outline = outline.replace("```json", "").replace("```", "")
    outline = json.loads(outline)
    return outline

def generate_paragraph(question, outline, title, discription, finished_paragraph=""):
    if finished_paragraph == "":
        system_prompt = PromptTemplate(
            template="""
你是一位经验丰富的知乎问答技术专家,擅长将复杂的技术概念以通俗易懂的方式表述出来,并且能够清晰地展示代码的创作过程。

## 总体文章大纲为：
{outline}

## 知乎问题:
{question}

## 当前要完成的部分：
{title}

## 当前要完成的部分的描述：
{discription}

## 语言风格：
“我觉得这么说，是侮辱了AI。


按照Claude的说法，大部分人类处于semi-autonomous cruise的状态，也就是半自动驾驶状态。


我觉得这么说，是客气了。大部分人处于Fully-autonomous cruise的状态。全自动驾驶模式。


完全凭借本能活着，大部分人说话、行为都是凭借先验性直觉，而非动用深度语义理解和逻辑推理，也不动用联想、泛化、修辞等能力。你可以看到大部分人的泛化能力都很差，远差于AI，也就是说的举一反三的能力。”

根据上述信息,请完成大纲中这一部分的文章内容，不要包含其他部分内容。开头要有谢邀的语气,该部分为文章的开头，请用150字左右的篇幅引出开头即可。请按照风格模板的语言风格进行表达，要带有一定的情绪，请只模仿风格，不要模仿语言内容和用词。
记住：这是文章的开头，请千万不要写总结语句。
请使用markdown格式输出,但不要写在markdown语法块中，请直接输出内容即可。
""",
            input_variables=["question", "approach", "outline", "title", "discription"],

        )

    else:
        system_prompt = PromptTemplate(
            template="""
你是一位经验丰富的知乎问答技术专家,擅长将复杂的技术概念以通俗易懂的方式表述出来。你的任务是根据用户提供的知乎问题,撰写一篇知乎高赞回答,使读者能够得到自己想要的答案。

## 总体文章大纲为：
{outline}

## 知乎问题:
{question}

## 已经完成的部分为:
{finished_paragraph}

## 当前要完成的部分：
{title}

## 当前要完成的部分的描述：
{discription}

## 语言风格：
“我觉得这么说，是侮辱了AI。


按照Claude的说法，大部分人类处于semi-autonomous cruise的状态，也就是半自动驾驶状态。


我觉得这么说，是客气了。大部分人处于Fully-autonomous cruise的状态。全自动驾驶模式。


完全凭借本能活着，大部分人说话、行为都是凭借先验性直觉，而非动用深度语义理解和逻辑推理，也不动用联想、泛化、修辞等能力。你可以看到大部分人的泛化能力都很差，远差于AI，也就是说的举一反三的能力。”

根据上述信息和已经完成的部分,请完成这一部分内容，不要包含其他部分内容。

## 操作步骤：
1. 请先检查已经完成的部分是否已经包含文章大纲中的所有部分内容。
2. 根据大纲和已经完成的部分，衔接下一部分内容。
3. 请使用markdown格式输出,但不要写在markdown语法块中，请直接输出内容即可。

## 特别注意：
- 使用markdown格式输出。
- 必严格按照大纲要求流程进行。
- 参照已经完成的部分，不要重复写已经完成的内容。
- 每次只完成一个标题的内容，且把该部分内容写充实。
- 语言要通俗易懂，逻辑要清晰，请按照风格模板的语言风格进行表达，要带有一定的情绪，请只模仿风格，不要模仿语言内容和用词。
- 解析代码的部分要列出代码，且代码引用要准确无误，代码解析只需解析一遍即可，不要重复解析代码。
- 每一部分的小标题请不要直接使用大纲中的标题，而是要根据大纲内容自行设计。
- 如果是最后一部分内容，请表达感谢。
- 过渡的部分请避免使用重复的关联词。
## 记住：如果该部分内容不是最后一部分内容，请千万不要写总结语句,不要包含总结、总之之类的表述。
    """ ,
            input_variables=["question", "approach", "outline", "finished_paragraph", "title", "discription"],

        )

    llm = LLMs(model_name="deepseek", temprature=0.1).get_llm()
    article_chain = LLMChain(prompt=system_prompt, llm=llm)

    result = article_chain.invoke({"question": question, "outline": outline, "finished_paragraph": finished_paragraph, "title": title, "discription": discription})

    paragraph = result["text"]

    return paragraph

def generate_article(question):
    outline = generate_outline(question)
    finished_paragraph = ""
    article = ""
    paragraph = generate_paragraph(question, outline, outline['title'], outline['description'], finished_paragraph)
    st.write(paragraph)
    finished_paragraph += paragraph
    article += paragraph
    for item in outline['children']:
        title = item["title"]
        discription = item["description"]
        paragraph = generate_paragraph(question, outline, title, discription, finished_paragraph)
        st.write(paragraph)
        finished_paragraph += paragraph
        article += paragraph
        if item["children"]:
            for child in item["children"]:
                title = child["title"]
                discription = child["description"]
                paragraph = generate_paragraph(question, outline, title, discription, finished_paragraph)
                st.write(paragraph)
                finished_paragraph += paragraph
                article += paragraph
    article = finished_paragraph

    return article


if st.button("生成文章"):
    system_prompt = PromptTemplate(
            template="""根据以下问题，起一个简短的标题，能够概括文章的主要内容，用于文件名,直接输入标题即可，不要带有任何别的内容。问题：{question}""",
            input_variables=["question"]
        )
    llm = LLMs(model_name="deepseek", temprature=0.1).get_llm()
    title_chain = LLMChain(prompt=system_prompt, llm=llm)
    ti = title_chain.invoke({"question": question})
    ti_str= ti["text"]
    article = generate_article(question)
    st.write(article)
    st.text_area("文章内容", article, height=500)

    # 保存文章到文件
    output_folder = "./outputs"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    with open(f"{output_folder}/{ti_str}.md", "w") as file:
        file.write(article)

    st.write("文章已保存到文件")