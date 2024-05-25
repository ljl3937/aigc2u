from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
import os
from langchain_openai import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

llm = ChatOpenAI(
    temperature=0.95,
    model="glm-4",
    openai_api_key=os.environ.get("ZHIPU_API_KEY"),
    openai_api_base="https://open.bigmodel.cn/api/paas/v4/"
)
# prompt = ChatPromptTemplate(
#     messages=[
#         SystemMessagePromptTemplate.from_template(
#             "You are a nice chatbot having a conversation with a human."
#         ),
#         MessagesPlaceholder(variable_name="chat_history"),
#         HumanMessagePromptTemplate.from_template("{question}")
#     ]
# )

# memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
# conversation = LLMChain(
#     llm=llm,
#     prompt=prompt,
#     verbose=True,
#     memory=memory
# )
# conversation.invoke({"question": "tell me a joke"})

os.environ["TAVILY_API_KEY"] = os.environ.get("TAVILY_API_KEY")
tools = [TavilySearchResults(max_results=2)]
prompt = hub.pull("hwchase17/react")

# Choose the LLM to use
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
agent_executor.invoke({"input": "LangChain是什么?"})