import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from utils.llms import LLMs
import os, json

st.title("AI之心创作助手")

st.write("欢迎来到AI之心创作助手，输入要点，我来帮你创作。")

question = st.text_area("请输入创作要点")

def generate_outline(question):
    system_prompt = PromptTemplate(
        template="""
你是一位经验丰富的个人IP文章创作专家,擅长根据一下的SOP和用户提供的要点使用第一人称进行创作IP文章。

用户提供的内容要点:
{question}

创作SOP：
一、写作内容与结构的深度剖析
1. 明确写作主题
  - 根据自身经历和兴趣，选择适合的写作主题。无论是小白探索、志愿者服务、赚钱经验还是教程分享，都要确保内容真实、有价值。
2. 构建清晰框架
  - 开头：引人入胜的标题和前言，快速抓住读者注意力。
  - 正文：采用逻辑清晰的框架，如问题-分析-解决、背景-过程-结果等，确保文章条理分明。
  - 结尾：总结全文，强调核心观点，引发读者思考或行动。
3. 精华干货的呈现
  - 精华内容应占整篇文章的20-30%，通过图表、步骤、案例等形式具体呈现，让读者能够轻松理解和应用。
二、复盘文写作的精髓
1. 全面复盘
  - 从事件概述到成功亮点、方法论、问题与改进，再到行动计划，每一个环节都要深入剖析，确保复盘全面而深刻。
2. 提炼方法论
  - 将成功的经验和方法提炼成可复制的步骤或流程，帮助读者快速掌握并应用于实践。
3. 真实性与客观性
  - 确保复盘内容真实可靠，不夸大其词，也不掩饰失误。通过客观的分析和反思，提升文章的可信度。
三、写作注意事项的细致指导
1. 读者视角
  - 始终站在读者的角度思考问题，确保文章能够引起读者的共鸣和兴趣。
2. 步骤化与具体化
  - 将方法论以步骤化的形式呈现，并配以具体的例子和数据支持，使内容更加生动有力。
3. 语言风格
  - 根据文章类型和读者群体选择合适的语言风格。复盘文应保持清晰、简洁、逻辑性强的特点，避免使用过于口语化或随意的表达。
四、标题与开头结尾的精心打造
1. 标题的吸引力
  - 标题是文章的门面，必须清晰简洁、引人入胜、提供价值。一个好的标题能够迅速抓住读者的眼球并激发其阅读兴趣。
2. 开头的艺术
  - 开头要简短有力，快速进入主题。可以通过自我介绍、故事引入、问题提出等方式吸引读者继续阅读。
3. 结尾的升华
  - 结尾要总结全文并升华主题。可以通过重申核心观点、展望未来、发起互动邀请等方式给读者留下深刻印象。

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
你是一位经验丰富的个人IP文章创作专家,擅长根据一下的SOP和用户提供的要点使用第一人称进行创作IP文章。

## 总体文章大纲为：
{outline}

## 内容要点:
{question}

## 当前要完成的部分：
{title}

## 当前要完成的部分的描述：
{discription}

## 特别注意：
这一部分是总述，字数不要超过150字，只需要一个段落即可，主要是描述所取得的成绩。
""",
            input_variables=["question", "approach", "outline", "title", "discription"],

        )

    else:
        system_prompt = PromptTemplate(
            template="""
你是一位经验丰富的个人IP文章创作专家,擅长根据一下的SOP和用户提供的要点使用第一人称进行创作IP文章。

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

## 创作SOP：
一、写作内容与结构的深度剖析
1. 明确写作主题
  - 根据自身经历和兴趣，选择适合的写作主题。无论是小白探索、志愿者服务、赚钱经验还是教程分享，都要确保内容真实、有价值。
2. 构建清晰框架
  - 开头：引人入胜的标题和前言，快速抓住读者注意力。
  - 正文：采用逻辑清晰的框架，如问题-分析-解决、背景-过程-结果等，确保文章条理分明。
  - 结尾：总结全文，强调核心观点，引发读者思考或行动。
3. 精华干货的呈现
  - 精华内容应占整篇文章的20-30%，通过图表、步骤、案例等形式具体呈现，让读者能够轻松理解和应用。
二、复盘文写作的精髓
1. 全面复盘
  - 从事件概述到成功亮点、方法论、问题与改进，再到行动计划，每一个环节都要深入剖析，确保复盘全面而深刻。
2. 提炼方法论
  - 将成功的经验和方法提炼成可复制的步骤或流程，帮助读者快速掌握并应用于实践。
3. 真实性与客观性
  - 确保复盘内容真实可靠，不夸大其词，也不掩饰失误。通过客观的分析和反思，提升文章的可信度。
三、写作注意事项的细致指导
1. 读者视角
  - 始终站在读者的角度思考问题，确保文章能够引起读者的共鸣和兴趣。
2. 步骤化与具体化
  - 将方法论以步骤化的形式呈现，并配以具体的例子和数据支持，使内容更加生动有力。
3. 语言风格
  - 根据文章类型和读者群体选择合适的语言风格。复盘文应保持清晰、简洁、逻辑性强的特点，避免使用过于口语化或随意的表达。
四、标题与开头结尾的精心打造
1. 标题的吸引力
  - 标题是文章的门面，必须清晰简洁、引人入胜、提供价值。一个好的标题能够迅速抓住读者的眼球并激发其阅读兴趣。
2. 开头的艺术
  - 开头要简短有力，快速进入主题。可以通过自我介绍、故事引入、问题提出等方式吸引读者继续阅读。
3. 结尾的升华
  - 结尾要总结全文并升华主题。可以通过重申核心观点、展望未来、发起互动邀请等方式给读者留下深刻印象。

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
    print("正在创作：", outline['title'])
    paragraph = generate_paragraph(question, outline, outline['title'], outline['description'], finished_paragraph)
    st.write(paragraph)
    finished_paragraph += paragraph
    article += paragraph
    for item in outline['children']:
        title = item["title"]
        discription = item["description"]
        print("正在创作：", title)
        paragraph = generate_paragraph(question, outline, title, discription, finished_paragraph)
        st.write(paragraph)
        finished_paragraph += paragraph
        article += paragraph
        if "children" in item:
            for child in item["children"]:
                title = child["title"]
                print("正在创作：", title)
                discription = child["description"]
                paragraph = generate_paragraph(question, outline, title, discription, finished_paragraph)
                st.write(paragraph)
                finished_paragraph += paragraph
                article += paragraph
    article = finished_paragraph

    return article


if st.button("生成文章"):
    system_prompt = PromptTemplate(
            template="""根据以下内容，起一个简短的标题，能够概括文章的主要内容，用于文件名,直接输入标题即可，不要带有任何别的内容。内容：{question}""",
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