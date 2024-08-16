# from langchain_community.document_loaders import AsyncHtmlLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain.chains.summarize import load_summarize_chain
# from langchain_community.chat_models.moonshot import MoonshotChat
# from langchain.chains.combine_documents.stuff import StuffDocumentsChain
# from langchain_core.prompts import PromptTemplate
# from langchain.chains.llm import LLMChain


# urls = ["https://python.langchain.com/v0.1/docs/integrations/retrievers/activeloop/"]

# import requests
# res = requests.get(urls[0])
# print(res)
# # print(res.content)
# # loader = AsyncHtmlLoader(urls,proxies={"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"})
# # docs = loader.load()
# # from langchain_community.document_transformers import Html2TextTransformer


# # h2text = Html2TextTransformer()
# # docs_transformed = h2text.transform_documents(docs)

# # text_splitter = RecursiveCharacterTextSplitter(chunk_size=4096)
# # texts = text_splitter.split_documents(docs_transformed)


# # print(texts[0].page_content)
# # print(len(texts))
# # prompt_template = """写下一段文字的摘要:
# # "{text}"
# # 摘要内容:"""
# # prompt = PromptTemplate.from_template(prompt_template)
# # llm_chain = LLMChain(llm=MoonshotChat(temperature=0), prompt=prompt)
# # stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")
# # # chain = load_summarize_chain(MoonshotChat(temperature=0), chain_type="stuff")
# # summary = stuff_chain.invoke(texts)
# # output = summary["output_text"]
# # print(f"Summary: {summary}")
# # print("===========")
# # print(f"Summary: {output}")



from crawl4ai import WebCrawler
from crawl4ai.extraction_strategy import LLMExtractionStrategy

# Create an instance of WebCrawler
crawler = WebCrawler()

# Warm up the crawler (load necessary models)
crawler.warmup()

# Run the crawler on a URL
result = crawler.run(url="https://blog.csdn.net/nav/ai")
url = "https://blog.csdn.net/nav/ai"
result = crawler.run(
        url=url,
        word_count_threshold=1,
        extraction_strategy= LLMExtractionStrategy(
            provider= QianfanChatEndpoint(model="ERNIE-Speed",temperature=0.1), 
            schema=OpenAIModelFee.schema(),
            extraction_type="schema",
            instruction="""From the crawled content, extract all mentioned model names along with their fees for input and output tokens. 
            Do not miss any models in the entire content. One extracted model JSON format should look like this: 
            {"model_name": "GPT-4", "input_fee": "US$10.00 / 1M tokens", "output_fee": "US$30.00 / 1M tokens"}."""
        ),            
        bypass_cache=True,
    )

# Print the extracted content
print(result.markdown)