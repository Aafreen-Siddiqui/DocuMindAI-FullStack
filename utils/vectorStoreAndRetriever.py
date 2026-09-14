from langchain_community.vectorstores import FAISS

def storing_vector_and_retriever(chunks, embeddings, file_type):
    vector_store = FAISS.from_documents(chunks,embeddings)
    print("File type, ", file_type)
    if file_type == ".csv":
        k = len(chunks)       # Retrieve all CSV rows
    else:
        k = 4 
    retriever = vector_store.as_retriever(search_kwargs={"k":k})
    return retriever
    