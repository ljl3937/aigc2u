from langchain.chat_models import ChatOpenAI
# from langchain_community.llms.moonshot import Moonshot
from langchain_community.llms import QianfanLLMEndpoint
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig

import chainlit as cl


@cl.on_chat_start
async def on_chat_start():
    model = ChatOpenAI(streaming=True)
    # model = QianfanLLMEndpoint(streaming=True)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "你是一个机器人",
            ),
            ("human", "{question}"),
        ]
    )
    runnable = prompt | model | StrOutputParser()
    cl.user_session.set("runnable", runnable)

@cl.on_message
async def on_message(message: cl.Message):
    runnable = cl.user_session.get("runnable")  # type: Runnable

    msg = cl.Message(content="")
    answer_prefix_tokens=["FINAL", "ANSWER"]

    async for chunk in runnable.astream(
        {"question": message.content},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler(
            stream_final_answer=True,
            answer_prefix_tokens=answer_prefix_tokens,
        )]),
    ):
        await msg.stream_token(chunk)

    await msg.send()
