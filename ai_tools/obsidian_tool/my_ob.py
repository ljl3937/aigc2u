from langchain_community.document_loaders import ObsidianLoader
from langchain.agents import create_react_agent
from langchain_openai import OpenAI
from langchain.tools import Tool
from langchain.indexes import VectorstoreIndexCreator
from langchain import hub, PromptTemplate, schema
from langchain.output_parsers import RegexParser

loader = ObsidianLoader("/home/jialin/Documents/AI/")
docs = loader.load()

index = VectorstoreIndexCreator().from_documents(docs)

def query_index(query):
    response = index.query(query)
    return response

ob_tool = Tool(
    name="查询obsidian索引",
    func=query_index,
    description="使用obsidian的索引来查询内容"
)

# llm = OpenAI()

# template = """Answer the following questions as best you can. You have access to the following tools:

# {tools}

# Use the following format:

# Question: {input}
# Thought: {agent_scratchpad}
# {result}"""
# # prompt = hub.pull("bluesky4cn/react-chat")
# prompt = PromptTemplate(
#     template=template,
#     input_variables=["input", "tools", "agent_scratchpad"],
#     tool_names=["查询obsidian索引"],
#     output_parser=RegexParser(
#         regex=r"Result: ?(.*)$",
#         output_keys=["result"],
#         default_output_key="result",
#     ),
# )

# # 创建代理
# tools = [ob_tool]
# agent = create_react_agent(tools=tools, llm=llm, prompt=prompt)

# # 设置代理执行器
# from langchain.agents import AgentExecutor
# agent_executor = AgentExecutor(
#     agent=agent,
#     tools=tools,
#     verbose=True,
#     handle_parsing_errors=True
# )

# 运行代理
# query = "总结卡片写作法?"
# # result = agent_executor.invoke({"chat_history":"以下内容请使用ob_tool工具进行查询","agent_scrtchpad":"","input": query})
# # print(result)

# print(index.query_with_sources(query))
