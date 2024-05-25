import os 
from tqdm import tqdm
from langchain.document_loaders import UnstructuredFileLoader
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

def get_files(dir_path):
    # args：dir_path，目标文件夹路径
    file_list = []
    for filepath, dirnames, filenames in os.walk(dir_path):
        # os.walk 函数将递归遍历指定文件夹
        for filename in filenames:
            # 通过后缀名判断文件类型是否满足要求
            if filename.endswith(".md"):
                # 如果满足要求，将其绝对路径加入到结果列表
                file_list.append(os.path.join(filepath, filename))
            elif filename.endswith(".txt"):
                file_list.append(os.path.join(filepath, filename))
    return file_list


def get_text(dir_path):
    # args：dir_path，目标文件夹路径
    # 首先调用上文定义的函数得到目标文件路径列表
    file_lst = get_files(dir_path)
    # docs 存放加载之后的纯文本对象
    docs = []
    # 遍历所有目标文件
    for one_file in tqdm(file_lst):
        file_type = one_file.split('.')[-1]
        if file_type == 'md':
            loader = UnstructuredMarkdownLoader(one_file)
        elif file_type == 'txt':
            loader = UnstructuredFileLoader(one_file)
        else:
            # 如果是不符合条件的文件，直接跳过
            continue
        docs.extend(loader.load())
    print("加载完成")
    return docs


def split_docs(docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=150)
    split_docs = text_splitter.split_documents(docs)
    print("划分完成")
    return split_docs


def save_docs(split_docs, persist_directory):
    from langchain_nomic.embeddings import NomicEmbeddings
        
    # 定义持久化路径
    persist_directory = 'data_base/vector_db/chroma'
    vectorstore = Chroma.from_documents(
        documents=split_docs,
        embedding=NomicEmbeddings(model="nomic-embed-text-v1"),
        persist_directory=persist_directory  # 允许我们将persist_directory目录保存到磁盘上
    )
    vectorstore.persist()
    retriever = vectorstore.as_retriever()
    print("持久化完成")
    return retriever


if __name__ == '__main__':
    # 定义目标文件夹路径
    dir_path = '/home/jialin/Documents/dev_docs/Chainlit'
    # 获取目标文件夹下的所有文件
    docs = get_text(dir_path)
    # 划分文档
    split_docs = split_docs(docs)
    # 持久化文档
    retriever = save_docs(split_docs, dir_path)

    
