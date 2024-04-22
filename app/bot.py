# app/bot.py
from llama_index.core.agent import ReActAgent
from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from pathlib import Path
from llama_index.core import VectorStoreIndex, Settings
from app.index_generator import init_indexes

# Load environment variables
load_dotenv()

# Settings for embedding model
Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5",
    # Optional GPU configuration (if you have a GPU available)
    # encode_kwargs={"device": "cuda", "batch_size": 100}
)

# Assemble all tools
def assemble_tools():
    indexes = init_indexes()

    tools = [
        QueryEngineTool(query_engine=indexes["packages"].as_query_engine(streaming=True), metadata=ToolMetadata(
            name="jazz_packages",
            description="Provides information about various Jazz mobile packages."
        )),
        QueryEngineTool(query_engine=indexes["offers"].as_query_engine(streaming=True), metadata=ToolMetadata(
            name="jazz_offers",
            description="Provides information about various Jazz offers."
        )),
        QueryEngineTool(query_engine=indexes["data_offers"].as_query_engine(streaming=True), metadata=ToolMetadata(
            name="jazz_data_offers",
            description="Provides information about various Jazz data offers."
        )),
        QueryEngineTool(query_engine=indexes["complaints"].as_query_engine(streaming=True), metadata=ToolMetadata(
            name="jazz_complaints",
            description="Provides help regarding frequent Jazz complaints and other information."
        ))
    ]

    return tools

llm = OpenAI("gpt-3.5-turbo")

agent = ReActAgent.from_tools(assemble_tools(), llm=llm)

async def chat(prompt: str):
    try:
        responses = agent.stream_chat(message=prompt)
        for response in responses.response_gen:
            yield response + ""  # Ensures the client can differentiate responses
    except Exception as e:
        yield "Error processing your request: " + str(e) + ""

