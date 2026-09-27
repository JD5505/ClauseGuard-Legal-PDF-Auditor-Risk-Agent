from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

def create_vector_store(chunks):
    try:
        old_store = Chroma(
            collection_name="clauseguard",
            embedding_function=embeddings,
            persist_directory="./chroma_db"
        )

        old_store.delete_collection()
    except Exception:
        pass

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="clauseguard",
        persist_directory="./chroma_db"
    )

    return vector_store


def load_vector_store():

    vector_store = Chroma(
        persist_directory="./chroma_db",
        collection_name="clauseguard",
        embedding_function=embeddings
    )

    return vector_store