import os
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from settings import INDEX_DIR, OPENAI_API_KEY


os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


def load_faiss_index(bus_model: str, index_dir: str = INDEX_DIR):
    """
    Load FAISS index for a specific bus model.
    """
    model_dir = os.path.join(index_dir, bus_model)

    if not os.path.exists(model_dir):
        raise FileNotFoundError(f"FAISS index not found for {bus_model} in {model_dir}")

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    # Load directly with LangChain
    vectorstore = FAISS.load_local(model_dir, embeddings, allow_dangerous_deserialization=True)
    
    return vectorstore

def query_rag(bus_model: str, query: str) -> str:
    """
    Query the FAISS index for the given bus model.
    """
    try:
        vectorstore = load_faiss_index(bus_model)
        docs = vectorstore.similarity_search(query, k=3)

        if not docs:
            return "Sorry, I could not find relevant information."

        context = "\n".join([doc.page_content for doc in docs])

        llm = OpenAI(openai_api_key=OPENAI_API_KEY, temperature=0)
        prompt = f"Answer the question based on the context below:\n\n{context}\n\nQuestion: {query}\nAnswer:"

        return llm(prompt)

    except FileNotFoundError as e:
        return str(e)
    except Exception as e:
        return f"Error while querying RAG: {e}"
