# src/vectorstore.py
# Handles embeddings, ChromaDB vector store, and retriever setup

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from src.config import HF_TOKEN, EMBEDDING_MODEL, CHROMA_DIR
import chromadb
import time
import os
import gc

COLLECTION_NAME = "aemet_alerts"

os.environ["HUGGINGFACEHUB_API_TOKEN"] = HF_TOKEN


def load_embeddings() -> HuggingFaceEmbeddings:
    """Load the HuggingFace sentence-transformer embedding model."""
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"token": HF_TOKEN}
    )


def build_vectorstore(chunks: list, embeddings: HuggingFaceEmbeddings) -> Chroma:
    """Build a fresh ChromaDB vector store from document chunks."""

    # Release any existing handle (Windows file-lock fix)
    try:
        chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
        existing = [c.name for c in chroma_client.list_collections()]
        if COLLECTION_NAME in existing:
            chroma_client.delete_collection(COLLECTION_NAME)
            print(f"Deleted old collection '{COLLECTION_NAME}' ✅")
        del chroma_client
        gc.collect()
        time.sleep(0.5)
    except Exception as e:
        print(f"Could not delete collection (will overwrite): {e}")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_DIR
    )
    print(f"Stored {vectorstore._collection.count()} chunks in ChromaDB ✅")
    return vectorstore


def load_vectorstore(embeddings: HuggingFaceEmbeddings) -> Chroma:
    """Load an existing ChromaDB vector store from disk."""
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR
    )


def get_retriever(vectorstore: Chroma, k: int = 5):
    """Return a retriever from the vector store."""
    return vectorstore.as_retriever(search_kwargs={"k": k})