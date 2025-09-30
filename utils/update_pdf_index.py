
import os
import pickle
import faiss
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from settings import PDF_DIR, INDEX_DIR, OPENAI_API_KEY

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


def build_index():
    loader = PyPDFDirectoryLoader(PDF_DIR)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    vectorstore = FAISS.from_documents(texts, embeddings)

    # Save FAISS index
    faiss.write_index(vectorstore.index, os.path.join(INDEX_DIR, "index.faiss"))

    with open(os.path.join(INDEX_DIR, "index.pkl"), "wb") as f:
        pickle.dump(vectorstore, f)

    print(" FAISS index built and saved successfully.")

if __name__ == "__main__":
    os.makedirs(INDEX_DIR, exist_ok=True)
    build_index()
