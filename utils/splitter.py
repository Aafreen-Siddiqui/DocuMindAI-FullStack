from langchain_text_splitters import RecursiveCharacterTextSplitter

def splitting_docs(docs):
    if docs is None:
        return None
    splitter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    return chunks