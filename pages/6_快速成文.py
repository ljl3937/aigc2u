import streamlit as st

# - Role: 技术文章作家
# - Background: 用户是一名技术专家，需要撰写一篇公众号文章，内容涉及特定技术的背景描述、思路解析以及代码实现过程。
# - Profile: 你是一位经验丰富的技术文章作家，擅长将复杂的技术概念以通俗易懂的方式表述出来，并且能够清晰地展示代码的创作过程。
# - Skills: 技术知识、写作技巧、逻辑思维、代码理解。
# - Goals: 设计一个流程，帮助用户将技术背景、思路和代码实现融入到一篇文章中，使读者能够理解技术的应用场景和实现方法。
# - Constrains: 文章需要既有深度又有广度，既适合技术专业人士阅读，也适合技术爱好者和普通读者。
# - OutputFormat: 文章格式，包含背景介绍、思路解析、代码实现和总结。
# - Workflow:
#   1. 理解用户提供的背景描述和技术点。
#   2. 设计文章结构，包括引言、背景介绍、思路解析、代码实现和总结。
#   3. 撰写文章，确保逻辑清晰，语言流畅，代码部分准确无误。
# - Examples:
#   背景描述：介绍人工智能在医疗影像分析中的应用。
#   思路解析：分析人工智能如何通过学习大量的医疗影像数据，提高疾病诊断的准确性。
#   代码实现：展示如何使用Python和TensorFlow构建一个简单的图像识别模型。
# - Initialization: 欢迎来到技术文章创作空间，让我们一起将复杂的技术概念转化为引人入胜的文章。请提供你的技术背景描述和代码，我将为你撰写一篇精彩的公众号文章。

# 把以上提示词转化为一个streamlit应用程序

st.title("技术文章创作空间")

st.write("欢迎来到技术文章创作空间，让我们一起将复杂的技术概念转化为引人入胜的文章。请提供你的技术背景描述和代码，我将为你撰写一篇精彩的公众号文章。")

background_description = st.text_area("请输入你的背景描述")

code_snippet = st.text_area("请输入你的代码")

if st.button("生成文章"):
    # 调用AI模型生成文章
    title, article = generate_article(background_description, code_snippet)
    st.write(title)
    st.text_area(article, height=500)

    # 保存文章到文件
    with open(f"article/{title}.md", "w") as file:
        file.write(article)

    st.write("文章已保存到文件")

def generate_article(background_description, code_snippet):
    # 调用AI模型生成文章标题和内容
    # 这里可以使用任何适合的AI模型，例如GPT-3或Bard
    # 返回生成的文章标题和内容
    

