from crewai_tools import BaseTool
from dotenv import load_dotenv
import os
import requests

class SendYuqueDocTool(BaseTool):
    name: str = "发送语雀文档工具"
    description: str = "用于发送或者发布语雀文档到语雀知识库的工具"

    def get_this_friday(self):
        import datetime
        today = datetime.date.today()
        today_weekday = today.weekday()
        print(today_weekday)
        if today_weekday == 4:
            return today
        elif today_weekday > 4:
            return today - datetime.timedelta(days=(today_weekday-4) % 7)
        else:
            return today + datetime.timedelta(days=(4 - today_weekday) % 7)
    

    def _run(self, content: str) -> str:
        load_dotenv()
        auth_token = os.getenv("YUQUE_AUTH_TOKEN")
        login = os.getenv("YUQUE_LOGIN")
        slug = os.getenv("YUQUE_SLUG")
        # 获取周报所在目录的uuid
        get_toc_url = f"https://www.yuque.com/api/v2/repos/{login}/{slug}/toc"
        header = {"X-Auth-Token": auth_token}
        res_toc = requests.get(get_toc_url, headers=header)
        toc = res_toc.json()
        this_friday = self.get_this_friday().strftime("%Y%m%d")
        print(this_friday)
        target_uuid = ""
        for item in toc["data"]:
            if item["type"] == "TITLE" and item["title"] == this_friday:
                target_uuid = item["uuid"]
                break
        print(target_uuid)
        # 需要单独调用更新目录接口才能更新文档到目录
        if target_uuid == "":
            return "未找到周报目录"
        create_doc_url = f"https://www.yuque.com/api/v2/repos/{login}/{slug}/docs"
        header = {"X-Auth-Token": auth_token}
        data = {
            "title": "部门工作周报",
            "format": "markdown",
            "body": content
        }
        created_article = requests.post(create_doc_url, headers=header, data=data)
        update_toc_url = f"https://www.yuque.com/api/v2/repos/{login}/{slug}/toc"
        data = {
            "action": "appendNode",
            "action_mode": "child",
            "type": "DOC",
            "doc_ids": [created_article.json()["data"]["id"]],
            "target_uuid": target_uuid
        }
        response = requests.put(update_toc_url, headers=header, json=data)
        return "创建语雀文档成功！"
    
# cy = CreateYuqueDocTool()
# content = '''
# ## 本周重点工作

# ### XDFS 相关
# * XDFS 5.5.6：本周无特定问题处理。
# * XDFS 6 & 6.2 开发：
#   - 处理了混选lvm和xfs盘的清理问题，进行独立操作。
#   - 修复了FTP服务启动和更新问题，操作流程优化。
#   - 处理了锁屏输入错误密码无错误提示问题。
#   - 对象网关服务取消子目录路径，API端口改为服务端口，console端口改为管理端口。
#   - 添加了不建议同一节点的brick在同一副本EC组中的提示。
#   - 硬盘管理批量操作添加lvm传参。
#   - 定位配额编辑报错相关问题。

# ### Fass 项目
# * Fass 2.2：
#   - 进行了多项优化，包括告警规则、日志下载接口、节点管理界面等。
#   - 修复了快照管理列表排序、磁盘密码接口报错、创建VIP接口报错等问题。
# * Fass 2.0 维护：计划进行项目维护和版本适配。

# ### FOSS 项目
# * FOSS 3.0 开发：
#   - 完成了原有功能接口的对接和新功能接口的调试。
#   - 开发了存储池界面节点注册及硬盘注册组件。
#   - 修改了存储桶管理页面组件。
#   - 对接网络域配置接口及步骤逻辑的开发书写。
#   - 遇到了接口修改或不可用的问题，正在与开发团队协调。

# ### XFile
# * XFile 精简版：
#   - 开发了资源列表页面、资源转移表单组件等。
#   - 增加了手动切换共享功能，优化了代码。
#   - 支持用户管理中的用户和组以文件的形式上传导入数据库和下载导出文件。

# ### 项目支持
# * 处理了客户环境安装问题和网页访问问题。
# * 国家电网项目安全漏扫问题解决。

# ### 前端逻辑
# * XFile 精简版开发与优化。
# * FASS 2.0 开发与优化。
# * XDFS 6.x 开发与优化。

# ### UI界面
# * FASS 2.2 版本优化需求及问题修复。
# * FOSS 3.0 资源池管理页组件重写。

# ## 下周计划
# * 继续进行 XDFS 6 相关开发和问题处理。
# * FOSS 3.0 页面组件后续开发。
# * Fass 2.0 后续维护跟进。
# * XFile 精简版需求变更调整及资源列表相关内容联调。
# * XDFS6软配额监控告警功能跟测。
# * XDFS6相关问题的处理和解决。
# * XDFS6推送安装功能实现与功能自测。
# '''

# cy.run(content)
