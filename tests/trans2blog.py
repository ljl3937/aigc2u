import os
import re
import requests
from datetime import datetime
from utils.llms import LLMs, Coze_api

def get_md_files(directory):
    md_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    return md_files

def get_title(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    title = re.search(r'title:\s*(.*)', content).group(1)
    return title

def get_date(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    date = re.search(r'date:\s*(.*)', content).group(1)
    return date

def generate_description(content):
    # 使用大模型生成文章总结
    description = ""
    llm = LLMs(model_name="deepseek", temprature=0.7).get_llm()

    from langchain_core.prompts import ChatPromptTemplate
    prompt = ChatPromptTemplate.from_messages([
        ("system", """- 提取用户输入内容的主体内容
- 不对提取的主题内容做任何修改
- 字数为300字左右
"""),
        ("user", "{input}")
    ])
    from langchain_core.output_parsers import StrOutputParser

    output_parser = StrOutputParser()

    chain = prompt | llm | output_parser
    description = chain.stream({"input": content})

    return description

def generate_image(title):
    coze_api = Coze_api()
    res = coze_api.run_workflow(title)
    # 使用大模型生成图片并上传到阿里云oss中，获取到的地址作为image和ogImage
    img_url = res['data']['output']
    image = "/blogs-img/{}.jpg".format(title)
    ogImage = image
    return image, ogImage

def generate_alt(title):
    # 使用大模型对title的总结作为alt
    alt = "{}的图片".format(title)
    return alt

def generate_tags(directory):
    # 目录名称作为tags的第0个元素
    tags = [os.path.basename(directory)]
    return tags

def add_attributes_to_md_files(directory, new_directory):
    md_files = get_md_files(directory)
    for file_path in md_files:
        title = get_title(file_path)
        date = get_date(file_path)
        image, ogImage = generate_image(title)
        alt = generate_alt(title)
        tags = generate_tags(directory)

        # 获取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        description = generate_description(content)

        # 添加文件属性
        new_content = f'---\ntitle: {title}\ndate: {date}\ndescription: {description}\nimage: {image}\nalt: {alt}\nogImage: {ogImage}\ntags: {tags}\npublished: true\n---\n' + content

        # 写入文件
        new_file_path = os.path.join(new_directory, os.path.basename(file_path))
        with open(new_file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

directory = '/c/code/jjbiji1/专家专栏'
new_directory = '/tmp/zhuanjia'
add_attributes_to_md_files(directory, new_directory)

