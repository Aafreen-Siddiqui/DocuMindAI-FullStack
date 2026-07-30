from langchain_community.vectorstores import FAISS

def storing_vector_and_retriever(chunks, embeddings):
    vector_store = FAISS.from_documents(chunks,embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k":4})
    return retriever
    