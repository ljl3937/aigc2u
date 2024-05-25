from crewai_tools import BaseTool
from pydantic.v1 import BaseModel, Field
from typing import Type, List
import requests
import os
from dotenv import load_dotenv

class GetWeeklyReport(BaseModel):
    title: str = Field(..., title="发送人", description="用于区分是谁发的周报")
    content: str = Field(..., title="周报内容", description="周报的具体内容")


class GetWeeklyReportsTool(BaseTool):
    name: str = "成员周报获取工具"
    description: str = "被用来获取语雀中的团队成员的工作周报"
    def get_this_friday(self):
        import datetime
        today = datetime.date.today()
        today_weekday = today.weekday()
        if today_weekday == 4:
            return today
        elif today_weekday > 4:
            return today - datetime.timedelta(days=(today_weekday-4) % 7)
        else:
            return today + datetime.timedelta(days=(4 - today_weekday) % 7)
    
    def get_members(self):
        load_dotenv()
        auth_token = os.getenv("YUQUE_AUTH_TOKEN")
        print(auth_token)
        login = os.getenv("YUQUE_LOGIN")
        url = f"https://www.yuque.com/api/v2/groups/{login}/users"
        header = {"X-Auth-Token": auth_token}
        response = requests.get(url, headers=header)
        members = response.json()
        print(members)
        return members["data"]

    def creat_doc(self, title: str, content: str):
        load_dotenv()
        auth_token = os.getenv("weekly_report/.env")
        login = os.getenv("YUQUE_LOGIN")
        slug = os.getenv("YUQUE_SLUG")
        create_doc_url = f"https://www.yuque.com/api/v2/repos/{login}/{slug}/docs"
        header = {"X-Auth-Token": auth_token}
        data = {
            "slug": slug,
            "title": "部门工作周报",
            "format": "markdown",
            "body": content
        }
        response = requests.post(create_doc_url, headers=header, data=data)
        print(response.json())
        return response.json()

    def _run(self, date) -> list[GetWeeklyReport]:
        load_dotenv()
        auth_token = os.getenv("YUQUE_AUTH_TOKEN")
        login = os.getenv("YUQUE_LOGIN")
        slug = os.getenv("YUQUE_SLUG")
        get_toc_url = f"https://www.yuque.com/api/v2/repos/{login}/{slug}/toc"
        header = {"X-Auth-Token": auth_token}
        response = requests.get(get_toc_url, headers=header)
        toc = response.json()
        # 因为我们的周报是周五发送，因此我们的目录名是周五的日期，格式为20210806
        if date is '':
            this_friday = self.get_this_friday().strftime("%Y%m%d")
        else:
            this_friday = date
        uuid = ""
        doc_ids = []
        docs = []
        for item in toc["data"]:
            if item["type"] == "TITLE" and item["title"] == this_friday:
                uuid = item["uuid"]
                break
        for doc in toc["data"]:
            if doc["type"] == "DOC" and doc["parent_uuid"] == uuid:
                doc_ids.append(doc["id"])
        print(doc_ids)
        for doc_id in doc_ids:
            get_doc_url = f"https://www.yuque.com/api/v2/repos/{login}/{slug}/docs/{doc_id}"
            response = requests.get(get_doc_url, headers=header)
            doc = response.json()
            item = GetWeeklyReport(title=doc["data"]["title"], content=doc["data"]["body"])
            docs.append(item)
        return docs

# get_reports_tool = GetWeeklyReportsTool()
# get_reports_tool.get_members()
# get_reports_tool.run()
