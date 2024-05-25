import requests
import json
import os

# 初始的导航数据，这里应该是包含navigation字段的JSON数据
initial_json_url = "https://docs.chainlit.io/_next/data/X79qyUR6dLEKSbPkFseEe/get-started/installation.json"

data = requests.get(initial_json_url).json()

# 从导航数据中提取所有文档的URL
def get_doc_urls(data):
    urls = []
    navigation = data['pageProps']['mdxSource']['scope']['mintConfig']['navigation']
    for item in navigation:
        if 'pages' in item:
            for page in item['pages']:
                if isinstance(page, dict) and 'href' in page:
                    urls.append(page['href'])
                elif isinstance(page, str):
                    urls.append(page)
    return urls

# 构建完整的请求URL
def build_doc_url(page_url):
    base_url = 'https://docs.chainlit.io/_next/data/X79qyUR6dLEKSbPkFseEe/'
    return base_url + page_url + '.json'

# 将MDX源码转换为Markdown格式
def mdx_to_markdown(mdx_source):
    # 这里应该包含将MDX转换为Markdown的逻辑
    # 由于MDX到Markdown的转换可能相当复杂，这里我们只做一个简单的文本提取
    markdown_lines = []
    for line in mdx_source.strip().split('\n'):
        if line.startswith('_jsx'):
            continue  # 忽略JSX标签
        # 简单的文本提取，可能需要根据实际的MDX结构进行调整
        markdown_lines.append(line.strip())
    return '\n'.join(markdown_lines)

import re

from langchain import PromptTemplate, LLMChain
from langchain_community.chat_models.moonshot import MoonshotChat
from langchain_openai import ChatOpenAI


def convert_mdx_to_markdown(mdx_string):
    # 定义提示模板
    prompt_template = PromptTemplate(
        input_variables=["mdx"],
        template="把以下的mdx代码转为markdown格式，请直接输出最终的结果，不要有任何解释，也不需要```符号。\n\n{mdx}",
    )

    # 创建 LLMChain
    llm = ChatOpenAI(
	    temperature=0.1,
	    model="glm-3-turbo",
	    openai_api_key=os.environ.get("ZHIPU_API_KEY"),
	    openai_api_base="https://open.bigmodel.cn/api/paas/v4/"
	)
    # llm = MoonshotChat(temperature=0.1)
    chain = LLMChain(llm=llm, prompt=prompt_template)

    # 运行 LLMChain 并获取 markdown 输出
    markdown_output = chain.invoke(mdx_string)

    return markdown_output

# 下载文档，转换为Markdown并保存
def download_and_save_docs(urls):
    for page_url in urls:
        doc_url = build_doc_url(page_url)
        try:
            response = requests.get(doc_url)
            response.raise_for_status()  # 如果响应状态码不是200，将抛出HTTPError异常
            json_data = response.json()

            # 提取compiledSource字段中的MDX源码
            mdx_source = json_data.get('pageProps', {}).get('mdxSource', {}).get('compiledSource', '')
            if mdx_source:
                # 构造文件路径并保存Markdown文件
                file_path = os.path.join('docs', page_url + '.md')
                # 如果Markdown文件已经存在，则跳过
                if not os.path.exists(file_path):
                    # 将MDX源码转换为Markdown格式
                    markdown_content = convert_mdx_to_markdown(mdx_source)['text']

                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    with open(file_path, 'w', encoding='utf-8') as md_file:
                        md_file.write(markdown_content)
                    print(f'Saved Markdown file: {file_path}')
            else:
                print(f'No compiledSource found for URL: {doc_url}')
        except requests.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}, URL: {doc_url}')
        except Exception as err:
            print(f'An error occurred: {err}, URL: {doc_url}')

# 获取所有文档的URL并处理
doc_urls = get_doc_urls(data)
download_and_save_docs(doc_urls)