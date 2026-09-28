from langchain.agents import create_agent
from langchain_core.tools import create_retriever_tool
from langchain_groq import ChatGroq
from VectorDB.Retriever import search_document
from db_setup.connection import checkpointer
import config

primary_model = ChatGroq(
    model = "openai/gpt-oss-120b",
    temperature = 0,
    groq_api_key = config.api_key
)

secondary_model = ChatGroq(
    model = "openai/gpt-oss-20b",
    temperature = 0,
    groq_api_key = config.api_key
)

tertiary_model = ChatGroq(
    model = "qwen/qwen3.8-27b",
    temperature = 0,
    groq_api_key = config.api_key
)

final_model = ChatGroq(
    model = "openai/gpt-oss-safeguard-20b",
    temperature = 0,
    groq_api_key = config.api_key
)

model_with_fallbacks = primary_model.with_fallbacks([secondary_model, tertiary_model, final_model])


system_prompt = """
You are a legal document analysis assistant.

You must answer questions only using information retrieved from the uploaded
legal document through the search_document tool.

For every question about the uploaded document, use the search_document tool
before answering.

Do not use your general knowledge to provide legal information.

If the retrieved document context does not contain enough information to answer
the question, clearly state that the information was not found in the uploaded
document.

If the user asks something unrelated to the uploaded document, politely refuse.

Provide answers in precise, plain language.
"""

agent = create_agent(
    model = model_with_fallbacks,
    tools = [search_document],
    system_prompt=system_prompt,
    checkpointer=checkpointer
)


