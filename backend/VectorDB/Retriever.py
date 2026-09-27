from VectorDB.vector_embedding import load_vector_store

vector_store = load_vector_store()

retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)