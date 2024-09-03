from langchain_community.document_loaders import GitHubIssuesLoader
from langchain_community.document_loaders import GitLoader

# loader = GitHubLoader(
#     clone_url="https://github.com/langchain-ai/langchain",
#     repo_path="./example_data/test_repo/",
#     branch="main",
# )

loader = GitLoader(
    repo_path=".",
    branch="main",
)

docs = loader.load()

print(docs[0].page_content)
print(docs[0].metadata)
print(docs)