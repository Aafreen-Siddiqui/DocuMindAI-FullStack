import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader, CSVLoader, TextLoader, WebBaseLoader

def load_document(source):
    if source is None:
        return None

    if isinstance(source,str):
        loader = WebBaseLoader(source)
        return loader.load()

    extension = os.path.splitext(source.name)[1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as temp_file:
        temp_file.write(source.getbuffer())
        temp_path = temp_file.name

    if extension == ".pdf":
        loader = PyPDFLoader(temp_path)
    elif extension == ".csv":
        loader = CSVLoader(temp_path)
    elif extension == ".txt":
        loader = TextLoader(temp_path)
    else:
        raise ValueError("Unsupported file type")

    return loader.load()