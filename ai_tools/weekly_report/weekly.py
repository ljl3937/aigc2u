import os
from dotenv import load_dotenv
from ai_tools.weekly_report.weekly_reports import GetWeeklyReportsTool
from ai_tools.weekly_report.send_yuque_doc import *
from langchain_community.chat_models import QianfanChatEndpoint
from langchain_community.chat_models.moonshot import MoonshotChat

def read_weekly_reports(directory):
    reports = []
    for filename in os.listdir(directory):
        if filename.endswith('.md'):
            name = filename.split('.')[0]  # 假设文件名是"姓名 工作周报"
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                reports.append({"name": name, "report": file.read()})
    return reports



def summarize_reports(reports):
    summary = "团队工作周报：\n\n"
    all_str = ""
    for name, report in reports:
        all_str += f"{name}：\n{report}\n\n"
    # 初始化LLM
    # llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"),model="gpt-3.5-turbo-0125")
    llm = QianfanChatEndpoint(model="ERNIE-Bot-4", request_timeout=120)
    # llm = MoonshotChat()

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
    summary = chain.invoke({"input": all_str})

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

def main():
    load_dotenv()
    print("")
    get_reports_tool = GetWeeklyReportsTool()
    # get_reports_tool.get_members()
    reports = get_reports_tool.run()
    print(reports)
    # reports = read_weekly_reports("./docs")
    summary = summarize_reports(reports)
    print(summary)
    choice = input("是否发送邮件和语雀？(y/n)")

    if choice == "y":
        yuque_tool = SendYuqueDocTool()
        yuque_tool.run(summary)
        send_email(summary)
    else:
        print("已取消发送")

if __name__ == "__main__":
    main()
