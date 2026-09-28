from langchain_core.tools import tool
from VectorDB.vector_embedding import load_vector_store


@tool
def search_document(query: str) -> str:
    """
    Search the currently uploaded legal document for relevant clauses,
    terms, conditions, obligations, risks, deadlines and other information.
    """

    vector_store = load_vector_store()

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 3}
    )

    documents = retriever.invoke(query)

    if not documents:
        return "No relevant information was found in the uploaded document."

    return "\n\n".join(
        document.page_content
        for document in documents
    )