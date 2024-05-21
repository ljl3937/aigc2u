import streamlit as st
import os

from ai_tools.weekly_report.send_yuque_doc import SendYuqueDocTool
from ai_tools.weekly_report.weekly_reports import GetWeeklyReportsTool

st.title("周报汇总")

# openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
from openai import OpenAI
from utils.llms import LLMs

def summarize_reports(reports):
    summary = "团队工作周报：\n\n"
    all_str = ""
    for name, report in reports:
        all_str += f"{name}：\n{report}\n\n"
    # 初始化LLM
    llm = LLMs(model_name="glm-3-turbo", temprature=0.7).get_llm()

    from langchain_core.prompts import ChatPromptTemplate
    prompt = ChatPromptTemplate.from_messages([
        ("system", """你是一个部门工作周报撰写者,请根据用户输入的个人工作周报内容生成部门工作周报。
         - 要求markdown格式。
         - 将个人周报合并，生成部门本周工作总结。
         - 每个要点要符合MECE。
         - 请直接输出汇总的周报内容，不要有别的废话。
         - 生成的部门工作周报不包含人名。"""),
        ("user", "{input}")
    ])
    from langchain_core.output_parsers import StrOutputParser

    output_parser = StrOutputParser()

    chain = prompt | llm | output_parser
    summary = chain.stream({"input": all_str})

    return summary

def send_email(content: str):
    
    # 配置阿里企业邮箱
    mail_host = "smtp.qiye.aliyun.com"
    sender = os.getenv("ALI_SENDER")
    passwd = os.getenv("ALI_PASSWD")
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header
    from email.utils import formataddr
    receivers = os.getenv("ALI_RECEIVERS")
    # 用markdown格式发送邮件
    content = f"""{content}"""
    import markdown2
    content = markdown2.markdown(content)
    print(content)
    print(sender)
    print(receivers)
    msg = MIMEText(content, 'html', 'utf-8')
    msg['From'] = formataddr(["xdfs", sender])
    msg['To'] = receivers
    msg['Subject'] = Header("AI&UI小组工作周报", 'utf-8').encode()
    print(msg)
    to_list = receivers.split(',')
    try:
        server = smtplib.SMTP_SSL(mail_host, 465)
        server.login(sender, passwd)
        server.sendmail(sender, to_list, msg.as_string())
        server.close()
        return '邮件发送成功'
    except Exception as e:
        return '邮件发送失败 %s' % e


def zhoubao_summary(date):
    get_reports_tool = GetWeeklyReportsTool()
    # get_reports_tool.get_members()
    reports = get_reports_tool.run(date)
    print(reports)
    summary = summarize_reports(reports)
    return st.write_stream(summary)
    # st.form_submit_button("发布语雀", SendYuqueDocTool().run(summary))
    # st.form_submit_button("发送邮件", send_email(summary))

with st.form("myform"):
    date = st.text_input("输入日期:", "",placeholder="输入日期格式为20210806, 默认为本周五")
    submitted = st.form_submit_button("Submit")
    # if not openai_api_key:
    #     st.info("Please add your OpenAI API key to continue.")
    if submitted:
        st.session_state.result = zhoubao_summary(date)


if "result" in st.session_state:
    if st.button("发语雀和邮件"):
        if "```markdown" in st.session_state.result:
            send_str = st.session_state.result.replace("```markdown", "").replace("```", "")
        else:
            send_str = st.session_state.result
        SendYuqueDocTool().run(send_str)
        send_email(send_str)
