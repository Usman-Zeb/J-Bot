import string
from dotenv import load_dotenv
import os
from llama_index_client import TextNode
import streamlit as st
import pandas as pd
from llama_index.core.query_engine import PandasQueryEngine
from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.readers.file import CSVReader
from prompts import new_prompt, instruction_str, context
import torch
from transformers import BitsAndBytesConfig
from llama_index.llms.huggingface import HuggingFaceLLM
from note_engine import note_engine
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from pathlib import Path
from llama_index.llms.gemini import Gemini
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
import json


load_dotenv()

# quantization_config = BitsAndBytesConfig(
#     load_in_4bit=True,
#     bnb_4bit_compute_dtype=torch.float16,
#     bnb_4bit_quant_type="nf4",
#     bnb_4bit_use_double_quant=True,
# )


# llm = HuggingFaceLLM(
#     model_name="berkeley-nest/Starling-LM-7B-alpha",
#     tokenizer_name="berkeley-nest/Starling-LM-7B-alpha",
#     context_window=3900,
#     max_new_tokens=256,
#     # model_kwargs={"quantization_config": quantization_config},
#     # tokenizer_kwargs={},
#     generate_kwargs={"temperature": 0.8},
#     device_map="auto",
# )

# Settings.llm = Gemini(model_name="models/gemini-pro")
# Settings.llm = llm
# Use Local embeddings model to save costs as by default llamaindex use text-embedding-ada-002 from OpenAI
Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5",
   
    # Use GPU for embedding and specify a large enough batch size to maximize GPU utilization.
    # Remove the "device": "cuda" to use CPU instead.
    # encode_kwargs={"device": "cuda", "batch_size": 100}
)



def serialize_node_with_score(node_with_score):
    """
    Serialize a NodeWithScore instance to a dictionary.
    """
    # Initial structure of the node with score.
    serialized = {
        'score': node_with_score.get_score(),
        'node': {
            'node_id': node_with_score.node_id,
            'id_': node_with_score.id_,
            'metadata': node_with_score.metadata,
            'embedding': node_with_score.embedding
        }
    }

    # Check if the node is a TextNode to include text-specific properties.
    if isinstance(node_with_score.node, TextNode):
        serialized['node'].update({
            'text': node_with_score.text,
            'content': node_with_score.get_content(),
        })

    return serialized






# Generate index, and embeddings
def get_index(data, index_name):
    index = None
    if not os.path.exists(index_name):
        print("building index", index_name)
        index = VectorStoreIndex.from_documents(data, show_progress=True)
        index.storage_context.persist(persist_dir=index_name)
    else:
        index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir=index_name)
        )

    return index



# jazz_packages_path = os.path.join("data", "packages.csv")
# print(jazz_packages_path)

def BotInitialize():
    load_dotenv()

    Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5",
   
    # Use GPU for embedding and specify a large enough batch size to maximize GPU utilization.
    # Remove the "device": "cuda" to use CPU instead.
    # encode_kwargs={"device": "cuda", "batch_size": 100}
    )


def Chat(prompt):
    
    #Jazz Packages
    packages_csv = CSVReader().load_data(Path("./data/packages.csv"))
    packages_index = get_index(packages_csv, "packages")
    packages_engine = packages_index.as_query_engine()

    #Jazz Offers
    offers_csv = CSVReader().load_data(Path("./data/offers.csv"))
    offers_index = get_index(offers_csv, "offers")
    offers_engine = offers_index.as_query_engine()
    #Jazz Data Offers
    dataoffers_csv = CSVReader().load_data(Path("./data/dataoffers.csv"))
    dataoffers_index = get_index(dataoffers_csv, "dataoffers")
    dataoffers_engine = dataoffers_index.as_query_engine()

    #Jazz SOPS & Complaints
    complaints_csv = CSVReader().load_data(Path("./data/complaints.csv"))
    complaints_index = get_index(complaints_csv, "complaints")
    complaints_engine = complaints_index.as_query_engine()



    # jazz_packages_query_engine = PandasQueryEngine(df=jazz_packages_df, verbose= True, instruction_str=instruction_str)
    # jazz_packages_query_engine.update_prompts({"pandas_prompt": new_prompt})
    # jazz_packages_query_engine.query("What are the total rows?")

    tools = [
        note_engine,
        QueryEngineTool(query_engine=packages_engine, metadata=ToolMetadata(
            name="jazz_packages",
            description="this gives information about different jazz packages in both English and Urdu scripts.",
        ),
        ),
        QueryEngineTool(query_engine=offers_engine, metadata=ToolMetadata(
            name="jazz_offers",
            description="this gives information about different jazz offers in both English and Urdu scripts.",
        ),
        ),
        QueryEngineTool(query_engine=dataoffers_engine, metadata=ToolMetadata(
            name="jazz_dataoffers",
            description="this gives information about different jazz data offers in both English and Urdu scripts.",
        ),
        ),
        QueryEngineTool(query_engine=complaints_engine, metadata=ToolMetadata(
            name="jazz_complaints",
            description="this gives help about frequent jazz complaints, SOPs, information about Sims, and Jazz WhatsApp in both English and Urdu scripts.",
        ),
        ),
        ]


    #print(jazz_packages_query_engine.query("What are the off network charges for Jazz One"))
    # 



    # llm_name = st.selectbox(
    #      "Which LLM?", ["text-davinci-003", "gpt-3.5-turbo", "gpt-4"]
    # )
    # # llm_name = st.selectbox(
    # #      "Which LLM?", ["models/gemini-pro"]
    # # )

    # llm = OpenAI(llm_name)
    llm = OpenAI("gpt-3.5-turbo")
    agent = ReActAgent.from_tools(tools, llm = llm, verbose= True, context=context)

    response = agent.query(prompt)
    print(response)
    return str(response)
    # if "messages" not in st.session_state:
    #     st.session_state.messages = []



    # for message in st.session_state.messages:
    #     with st.chat_message(message["role"]):
    #         st.markdown(message["content"])

    # if prompt := st.chat_input("What is up?"):

    #     with st.chat_message("user"):
    #         st.markdown(prompt)

    #     st.session_state.messages.append({"role": "user", "content":prompt})
    
    #     agent = ReActAgent.from_tools(tools, llm = llm, verbose= True, context=context)

    #     response = agent.query(string.lower(prompt))
    
    #     with st.chat_message("assistant"):
    #         st.markdown(response)

    #     st.session_state.messages.append({"role": "assistant", "content":response})
    # agent = ReActAgent.from_tools(tools, llm = llm, verbose= True, context=context)
    # while (prompt := input("Enter a prompt (q to quit): ")) != "q":
    #    result = agent.query(prompt)
    #    print(result)

    # print(jazz_packages_df.head())

