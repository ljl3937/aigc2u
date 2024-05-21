from langchain.chat_models import ChatOpenAI
# from langchain_community.llms.moonshot import Moonshot
# from langchain_community.llms import QianfanLLMEndpoint
from langchain_community.llms import ChatGLM
from langchain_mistralai import ChatMistralAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig
from langchain.agents import initialize_agent, AgentType, Tool, AgentExecutor, create_react_agent
# from langchain.tools import WikipediaSearchTool, WolframAlphaQueryTool
# from langchain_openai import OpenAI
from openai import OpenAI
from ai_tools.obsidian_tool.my_ob import ob_tool
from langchain.utilities.serpapi import SerpAPIWrapper
from langchain.chains import LLMMathChain
from dotenv import load_dotenv
from langchain import hub
import os

import chainlit as cl

from ai_tools.mdx_tools.chain import load_chain
from langchain_community.chat_models import ChatZhipuAI

load_dotenv()



@cl.on_chat_start
async def start():
    # llm = ChatOpenAI(temperature=0.1, streaming=True)
    llm1 = ChatMistralAI(temperature=0.1, streaming=True)
    # llm1 = ChatOpenAI(
    #     temperature=0.1,
    #     model="glm-4",
    #     openai_api_key=os.environ.get("ZHIPU_API_KEY"),
    #     openai_api_base="https://open.bigmodel.cn/api/paas/v4/"
    # )
    #llm1 = ChatZhipuAI(temperature=0.01, model="glm-4")
    # llm1 = OpenAI(
    #     api_key = os.environ.get("MOONSHOT_API_KEY"),
    #     base_url = "https://api.moonshot.cn/v1",
    # )
    # llm1 = OpenAI(
    #     api_key = os.environ.get("DEEPSEEK_API_KEY"),
    #     base_url = "https://api.deepseek.com/v1",
    # )
    search = SerpAPIWrapper()
    # llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
    qa_tool = load_chain()

    tools = [
        # Tool(
        #     name="Search",
        #     func=search.run,
        #     description="useful for when you need to answer questions about current events. You should ask targeted questions",
        # ),
        # ob_tool,
        qa_tool,
    ]
    agent = initialize_agent(
        tools, llm1, agent="chat-zero-shot-react-description", verbose=True
    )
    # prompt = hub.pull("hwchase17/react")
    # agent = create_react_agent(llm1, tools, prompt)
    # agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    agent.handle_parsing_errors = True
    cl.user_session.set("agent", agent)

    # actions = [
    #     cl.Action(name="周报总结", value="周报总结", description="点击生成本周部门工作周报!"),
    #     cl.Action(name="ChainLit QA", value="ChainLit QA", description="Chainlit问答!"),
    # ]

    # await cl.Message(content="请选择你要进行的操作:", actions=actions).send()

@cl.action_callback("周报总结")
async def on_action(action: cl.Action):
    print("The user clicked on the action button!")

    return "Thank you for clicking on the action button!"


@cl.action_callback("ChainLit QA")
async def on_action(action: cl.Action):
    print("The user clicked on the action button!")
    return "Thank you for clicking on the action button!"

@cl.on_message
async def main(message: cl.Message):
    agent = cl.user_session.get("agent")  # type: AgentExecutor
    cb = cl.LangchainCallbackHandler(stream_final_answer=True)

    await cl.make_async(agent.invoke)(message.content, callbacks=[cb])

# @cl.on_chat_start
# async def on_chat_start():
#     model = ChatOpenAI(streaming=True)
#     # model = QianfanLLMEndpoint(streaming=True)
#     prompt = ChatPromptTemplate.from_messages(
#         [
#             (
#                 "system",
#                 "你是一个机器人",
#             ),
#             ("human", "{question}"),
#         ]
#     )
#     runnable = prompt | model | StrOutputParser()
#     cl.user_session.set("runnable", runnable)

# @cl.on_message
# async def on_message(message: cl.Message):
#     runnable = cl.user_session.get("runnable")  # type: Runnable

#     msg = cl.Message(content="")
#     answer_prefix_tokens=["FINAL", "ANSWER"]

#     async for chunk in runnable.astream(
#         {"question": message.content},
#         config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler(
#             stream_final_answer=True,
#             answer_prefix_tokens=answer_prefix_tokens,
#         )]),
#     ):
#         await msg.stream_token(chunk)

#     await msg.send()
