import os
import sys
# 获取脚本所在目录的上一级目录
script_dir = os.path.dirname(os.getcwd())
# 改变当前工作目录为脚本所在目录的上一级目录
# os.chdir(script_dir)
print(os.getcwd())
sys.path.append(os.getcwd())
import re
import requests
from datetime import datetime
from utils.llms import LLMs, Coze_api
from langchain_core.prompts import ChatPromptTemplate

def get_md_files(directory):
    md_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    return md_files

def get_title(file_path):
    # 获取文件名
    file_name = os.path.basename(file_path)
    # 去掉文件后缀名
    title = os.path.splitext(file_name)[0]
    return title

def get_date(file_path):
    # 获取文件的修改时间
    date = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
    return date

def generate_description(content):
    # 使用大模型生成文章总结
    description = ""
    llm = LLMs(model_name="deepseek", temprature=0.7).get_llm()

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
    description = chain.invoke({"input": content})

    return description

def generate_image(title, alt):
    coze_api = Coze_api()
    workflow_id = "7407383012478320655"
    params = {
        "title": alt
    }
    res = coze_api.run_workflow(workflow_id=workflow_id,parameters=params)
    # 使用大模型生成图片并上传到阿里云oss中，获取到的地址作为image和ogImage
    import json
    img_url = json.loads(res['data'])['output']
    img = requests.get(img_url).content
    import random
    filename = 'blg_' + alt + str(random.randint(100, 999))
    # 保存图片到本地
    with open("/tmp/{}.jpg".format(filename), 'wb') as f:
        f.write(img)
    # 生成图片的alt
    oss_folder = "oss://jjbiji-pic/"
    # 文件名为alt+3位随机数
    command = ['ossutil', 'cp', '-f', "/tmp/{}.jpg".format(filename), oss_folder]
    import subprocess
    subprocess.run(command, check=True)
    image = "https://jjbiji-pic.oss-cn-beijing.aliyuncs.com/{}.jpg".format(filename)
    ogImage = image
    return image, ogImage

def generate_alt(title):
    # 使用大模型对title的总结作为alt
    llm = LLMs(model_name="qianfan", temprature=0.7).get_llm()

    prompt = ChatPromptTemplate.from_messages([
        ("system", """- 把用户输入内容概括为6个字以内。务必保证字数不超过6个字，直接输出结果，不要有人格多余的字
"""),
        ("user", "{input}")
    ])
    from langchain_core.output_parsers import StrOutputParser

    output_parser = StrOutputParser()

    chain = prompt | llm | output_parser
    alt = chain.invoke({"input": title})
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
        alt = generate_alt(title)
        image, ogImage = generate_image(title, alt)
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

directory = '/Volumes/sandisk/code/mywebsite/jjbiji1/专家专栏'
new_directory = '/tmp/zhuanjia'
add_attributes_to_md_files(directory, new_directory)

