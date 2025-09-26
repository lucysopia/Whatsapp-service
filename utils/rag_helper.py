import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate

INDEX_DIR = os.getenv("INDEX_DIR", "vectorstore/")


def load_vectorstore(model_name: str):
    """Load FAISS index for a given bus model"""
    model_index_path = os.path.join(INDEX_DIR, model_name)
    if not os.path.exists(model_index_path):
        raise ValueError(f"No FAISS index found for {model_name}")
    return FAISS.load_local(model_index_path, OpenAIEmbeddings(model="text-embedding-3-small"), allow_dangerous_deserialization=True)


def query_manual(model_name: str, question: str) -> str:
    """Query the FAISS index and get an answer from ChatGPT"""
    db = load_vectorstore(model_name)
    docs = db.similarity_search(question, k=4)

    context = "\n\n".join([d.page_content for d in docs])

    prompt = PromptTemplate.from_template("""
    You are a helpful assistant for bus engineers and technicians. 
    Use the context below to answer the question in simple, clear steps. 
    If you don’t know, say you don’t know.

    Context:
    {context}

    Question: {question}
    Answer:
    """)

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    response = llm.predict(prompt.format(context=context, question=question))
    return response
