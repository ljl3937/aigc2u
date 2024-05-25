from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import sqlite3
import time
import csv
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.chat_models.moonshot import MoonshotChat
from langchain_community.chat_models import QianfanChatEndpoint
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain_core.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain_community.document_transformers import Html2TextTransformer
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# 加载 .env 文件，假设位于当前脚本的同一目录下
load_dotenv()
class Mp_his:
    def __init__(self):
        options = Options()
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
        options.add_argument("--incognito")
        self.driver = webdriver.Chrome(options=options)
        self.vars = {}

    def wait_for_window(self, timeout=2):
        time.sleep(round(timeout / 1000))
        wh_now = self.driver.window_handles
        wh_then = self.vars["window_handles"]
        if len(wh_now) > len(wh_then):
            return set(wh_now).difference(set(wh_then)).pop()
    
    def check_exist(self, link):
        # 检查数据库中是否存在该文章
        conn = sqlite3.connect("mp1.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM mp_articles WHERE link = ?", (link,))
        result = cursor.fetchone()
        conn.close()
        return result
    
    def get_his(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.driver.get("http://mp.weixin.qq.com/")
        self.vars["window_handles"] = self.driver.window_handles
        if self.driver.find_elements(By.CLASS_NAME, "login__type__container__scan__qrcode"):
            # 等待二维码出现
            time.sleep(2)
            qrcode = self.driver.find_element(
                By.CLASS_NAME, "login__type__container__scan__qrcode")
            qrcode.screenshot("./qrcode.png")
        # 等待.new-creation__menu-item:nth-child(2) svg出现
        WebDriverWait(self.driver, 60).until(expected_conditions.presence_of_element_located(
            (By.CSS_SELECTOR, ".new-creation__menu-item:nth-child(2) svg")))
        self.driver.find_element(
            By.CSS_SELECTOR, ".new-creation__menu-item:nth-child(2) svg").click()
        self.vars["win670"] = self.wait_for_window(2000)
        self.driver.switch_to.window(self.vars["win670"])
        self.driver.find_element(By.ID, "js_editor_insertlink").click()
        # 从mp.csv中读取公众号名称
        with open('mp.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                self.driver.find_element(
                    By.XPATH, "//button[contains(.,\'选择其他公众号\')]").click()
                # 输入公众号名称
                self.driver.find_element(
                    By.CSS_SELECTOR, ".weui-desktop-search__wrp .weui-desktop-form__input").send_keys(row[0])
                self.driver.find_element(
                    By.CSS_SELECTOR, ".weui-desktop-search__wrp .weui-desktop-form__input").send_keys(Keys.ENTER)
                time.sleep(1)
                # 选择第一个公众号.inner_link_account_item的第一个
                WebDriverWait(self.driver, 60).until(expected_conditions.presence_of_element_located(
                    (By.CSS_SELECTOR, ".inner_link_account_item:nth-child(1)")
                ))
                self.driver.find_element(
                    By.CSS_SELECTOR, ".inner_link_account_item:nth-child(1)").click()
                
                while True:
                    # 循环class 为 .inner_link_article_item的 label 标签
                    for i in range(1, 5):
                        WebDriverWait(self.driver, 60).until(expected_conditions.presence_of_element_located(
                            (By.CSS_SELECTOR, f".inner_link_article_item:nth-child({i})")))
                        label = self.driver.find_element(
                            By.CSS_SELECTOR, f".inner_link_article_item:nth-child({i})")
                        author = row[0]
                        title = label.find_element(
                            By.CSS_SELECTOR, "div span:nth-child(2)").text
                        publish_date_str = label.find_element(
                            By.CSS_SELECTOR, ".inner_link_article_date").text
                        publish_date = datetime.strptime(
                            publish_date_str, "%Y-%m-%d")
                        link = label.find_element(
                            By.CSS_SELECTOR, "a").get_attribute("href")
                        # 当发布时间小于昨天，结束循环
                        # if publish_date < datetime.now() - timedelta(days=7):
                        #     print("发布时间不在一周内，结束循环")
                        #     break
                        # 数据库里面有这篇文章，结束循环
                        if self.check_exist(link):
                            continue
                        
                        summary = ""
                        # 加载html并获取概述
                        if os.environ['SUMMARY_FLAG'] == 'True':
                            loader = AsyncHtmlLoader([link])
                            doc = loader.load()
                            h2t = Html2TextTransformer()
                            docs_transformed = h2t.transform_documents(doc)
                            text_splitter = RecursiveCharacterTextSplitter()
                            texts = text_splitter.split_documents(docs_transformed)
                            prompt_template = """写下一段文字的摘要:
    "{text}"
    摘要内容:"""
                            prompt = PromptTemplate.from_template(prompt_template)
                            llm_chain = LLMChain(llm=QianfanChatEndpoint(model="ERNIE-Speed-128K",temperature=0.1), prompt=prompt)
                            stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")
                            summary = stuff_chain.invoke(texts)["output_text"]

                        # 写入sqlite3
                        conn = sqlite3.connect('mp1.db')
                        c = conn.cursor()
                        # 查询 title 是否已经存在
                        c.execute("SELECT * FROM mp_articles WHERE title = ?", (title,))

                        if c.fetchone():
                            print("title已经存在")
                            continue

                        c.execute(
                            "INSERT INTO mp_articles (title, author, publish_date, link, summary) VALUES (?, ?, ?, ?, ?)", (title, author, publish_date, link, summary))
                        conn.commit()
                        # 写入mysql数据库
                        import mysql.connector
                        
                        mydb = mysql.connector.connect(
                            host=os.environ['MYSQL_HOST'],
                            user=os.environ['MYSQL_USER'],
                            password=os.environ['MYSQL_PASSWORD'],
                            database="mp_articles"
                        )
                        mycursor = mydb.cursor()
                        mycursor.execute(
                            "INSERT INTO mp_articles (title, author, publish_date, link, summary) VALUES (%s, %s, %s, %s, %s)", (title, author, publish_date, link, summary))
                        mydb.commit()

                        print(f"{title} 写入成功")
                    try:
                        self.driver.find_element(By.LINK_TEXT, "下一页").click()
                    except:
                        break
                    




if __name__ == "__main__":
    
    mp_his = Mp_his()
    mp_his.get_his()