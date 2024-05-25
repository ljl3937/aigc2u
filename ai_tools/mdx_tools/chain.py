from langchain.vectorstores import Chroma
from langchain_nomic.embeddings import NomicEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_community.tools.vectorstore.tool import VectorStoreQAWithSourcesTool

import os

def load_chain():
    persist_directory = 'data_base/vector_db/chroma'
    vectorstore = Chroma(
        embedding_function=NomicEmbeddings(model="nomic-embed-text-v1"),
        persist_directory=persist_directory  # 允许我们将persist_directory目录保存到磁盘上
    )

    # 创建 LLMChain
    llm = ChatOpenAI(
        temperature=0.1,
        model="glm-3-turbo",
        openai_api_key=os.environ.get("ZHIPU_API_KEY"),
        openai_api_base="https://open.bigmodel.cn/api/paas/v4/"
    )

    template = """使用以下上下文来回答最后的问题。如果你不知道答案，就说你不知道，不要试图编造答
    案。尽量使答案简明扼要。总是在回答的最后说“谢谢你的提问！”。
    {context}
    问题: {question}
    有用的回答:"""
    QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context","question"],template=template)

    # 运行 chain
    # qa_chain = RetrievalQA.from_chain_type(llm,retriever=vectorstore.as_retriever(),return_source_documents=True,chain_type_kwargs={"prompt":QA_CHAIN_PROMPT})
    tool = VectorStoreQAWithSourcesTool(
        name="vector_db_qa",
        vectorstore=vectorstore,
        llm=llm,
        description="使用这个工具从向量数据库中搜索Chainlit相关信息并生成答案。输入是你的查询。"
    )
    return tool

# if __name__ == "__main__":
#     qa_chain = load_chain()
#     result = qa_chain({"query": "What is Chainlit?"})
#     print(result)
