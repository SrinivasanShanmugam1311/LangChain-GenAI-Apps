"""
Document Q&A using LangChain, FAISS, and OpenAI embeddings + Chat model.
"""

import sys
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

# ✅ new OpenAI imports
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

# load .env file
load_dotenv()

def build_vectorstore(pdf_path: str, persist_dir: str = "faiss_index"):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    emb = OpenAIEmbeddings()
    db = FAISS.from_documents(chunks, emb)
    return db

def interactive_qa(db):
    retriever = db.as_retriever(search_kwargs={"k": 4})
    llm = ChatOpenAI(temperature=0)
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, verbose=False)

    print("Document Q&A. Type 'exit' to quit.")
    while True:
        q = input("\nQuestion: ").strip()
        if q.lower() in ("exit", "quit"):
            break
        ans = qa.invoke(q)   # ✅ use invoke instead of run
        print("\nAnswer:\n", ans["result"])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python doc_qa.py /path/to/doc.pdf")
        sys.exit(1)
    pdf = sys.argv[1]
    if not Path(pdf).exists():
        print("PDF not found:", pdf); sys.exit(1)

    print("Building vectorstore (this may take a minute)...")
    db = build_vectorstore(pdf)
    print("Vectorstore ready.")
    interactive_qa(db)
