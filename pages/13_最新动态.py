import streamlit as st
import os, pymysql
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from utils.llms import LLMs
import subprocess

st.title("最新动态生成器")

# 默认提示词
default_prompt = """请根据查询到的近期微博内容，写一篇最新动态的文章。
- 要求文章要条目清晰，使用网络用语，以接地气的方式表达出来。
- 请参考提供微博内容的最有吸引力的 6 个话题。
- 文中有乱码的话题不要选择。
- 如果文中带有链接，请同样把链接带上。
- 每个话题结束的时候要把原微博的链接带上，微博的链接地址一般格式示例为：https://weibo.com/5073702779618472/OuVlrEmcE，其中的5073702779618472为id，OuVlrEmcE为bid。
- 如果微博内容有视频的，不要给出视频地址，提示用户看微博的原地址即可"""

# 创建一个文本区域用于输入提示词
prompt = st.text_area("输入提示词", value=default_prompt, height=100)

# 创建一个按钮
if st.button("生成"):
    # 连接到MySQL数据库
    conn = pymysql.connect(
        host=os.environ['MYSQL_HOST'],
        user=os.environ['MYSQL_USER'],
        password=os.environ['MYSQL_PASSWORD'],
        database=os.environ['MYSQL_DB']
    )
    
    try:
        with conn.cursor() as cursor:
            # 查询最近3天的所有微博内容
            sql = """
            SELECT * FROM weibo 
            WHERE created_at >= DATE_SUB(CURDATE(), INTERVAL 3 DAY) 
            ORDER BY created_at DESC
            """
            cursor.execute(sql)
            results = cursor.fetchall()
            
            # 过滤出text字段，并记录对应的id和screen_name
            weibo_content = []
            for result in results:
                weibo_content.append({
                    'id': result[0],
                    'bid': result[1],
                    'text': result[4],
                    'screen_name': result[3]
                })
            
            # 将查询结果转换为字符串
            weibo_text = "\n".join([f"{item['screen_name']}（ID: {item['id']}，BID: {item['bid']}）：{item['text']}" for item in weibo_content])
            
            # 创建提示模板
            template = f"""
            {prompt}
            
            以下是最近的微博内容：
            {weibo_text}
            
            请根据以上内容生成一篇最新动态文章。
            
            - 在生成文章时，每个话题起一个标题。
            - 请在每个话题结束后标记这个话题对应的微博ID和用户名，标记格式为【用户名-微博ID】,注意，该标记是为了代替图片的，不是标题，务必放在每个话题的末尾，且保证只出现一次，不要反复出现。
            """
            
            prompt_template = PromptTemplate(template=template, input_variables=[])
            
            # 使用LLMChain生成文章
            llm = LLMs(model_name="glm-4-flash", temprature=0.7).get_llm()
            chain = LLMChain(llm=llm, prompt=prompt_template)
            
            # 生成文章
            article = chain.run({})
            
            # 解析生成的文章，插入图片
            for item in weibo_content:
                if str(item['id']) in article:
                    img_dir = f"ai_tools/weibo_crawler/weibo/{item['screen_name']}/img/原创微博图片"
                    img_tags = []
                    if os.path.exists(img_dir):
                        for img_file in os.listdir(img_dir):
                            if f"_{item['id']}" in img_file:
                                img_path = os.path.join(img_dir, img_file)
                                
                                # 上传图片到OSS
                                oss_folder = os.getenv("OSS_FOLDER")
                                if os.name == 'posix':
                                    # 区分 Linux 和MacOS
                                    if os.uname().sysname == 'Darwin':
                                        command = ['ossutil', 'cp', '-f', img_path, oss_folder]
                                    else:
                                        command = ['ossutil64', 'cp', '-f', img_path, oss_folder]
                                elif os.name == 'nt':
                                    command = ['ossutil.exe', 'cp', '-f', img_path, oss_folder]
                                else:
                                    print("Error: Unsupported operating system.")
                                    exit(1)
                                
                                subprocess.run(command)
                                
                                # 获取图片的OSS链接
                                img_url = "https://jjbiji-pic.oss-cn-beijing.aliyuncs.com/{}".format(img_file)
                                img_tags.append(f'![微博图片]({img_url})')
                    
                    if img_tags:
                        img_html = '\n'.join(img_tags)  # 使用换行符连接多个图片引用
                    else:
                        img_html = ''  # 如果没有找到图片，设置为空字符串
                    
                    article = article.replace(f'【{item["screen_name"]}-{item["id"]}】', img_html, 1)
            
            print(article)
            # 显示生成的文章
            st.markdown(article, unsafe_allow_html=True)
    
    finally:
        conn.close()
