import os
import glob
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

DATA_DIR = os.getenv("PDF_DIR", "manuals/")
INDEX_DIR = os.getenv("INDEX_DIR", "indexes/")  # base folder for all model indexes


def split_documents(documents, chunk_size=800, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " "]
    )
    return splitter.split_documents(documents)


def build_faiss_indexes():
    os.makedirs(INDEX_DIR, exist_ok=True)

    pdf_files = glob.glob(os.path.join(DATA_DIR, "*.pdf"))
    if not pdf_files:
        print("[WARN] No PDFs found in 'manuals/'. Add PDFs and rerun.")
        return

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    for pdf_file in pdf_files:
        print(f"[INFO] Loading {pdf_file} ...")
        loader = PyPDFLoader(pdf_file)

        # Extract model name from filename (before first "_")
        model_name = os.path.splitext(os.path.basename(pdf_file))[0].split("_")[0]
        model_index_path = os.path.join(INDEX_DIR, model_name)

        pages = loader.load()
        for p in pages:
            p.metadata["model"] = model_name
            p.metadata["source"] = os.path.basename(pdf_file)

        print(f"[INFO] Splitting {len(pages)} pages for {model_name}...")
        chunks = split_documents(pages)

        print(f"[INFO] Creating embeddings for {len(chunks)} chunks ({model_name})...")
        vectorstore = FAISS.from_documents(chunks, embeddings)

        os.makedirs(model_index_path, exist_ok=True)
        print(f"[INFO] Saving FAISS index for {model_name} → {model_index_path}")
        vectorstore.save_local(model_index_path)

    print("[SUCCESS] All indexes built and saved!")


if __name__ == "__main__":
    build_faiss_indexes()
