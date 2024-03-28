from dotenv import load_dotenv
import os
import streamlit as st
import pandas as pd
from llama_index.core.query_engine import PandasQueryEngine
from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.readers.file import CSVReader
from prompts import new_prompt, instruction_str, context
from note_engine import note_engine
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from pathlib import Path
from llama_index.llms.gemini import Gemini


load_dotenv()

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

#Jazz Packages
packages_csv = CSVReader().load_data(Path("./data/packages.csv"))
packages_index = get_index(packages_csv, "packages")
packages_engine = packages_index.as_query_engine()



#Jazz Offers
offers_csv = CSVReader().load_data(Path("./data/offers.csv"))
offers_index = get_index(offers_csv, "offers")
offers_engine = packages_index.as_query_engine()

complaints_csv = CSVReader().load_data(Path("./data/complaints.csv"))
complaints_index = get_index(complaints_csv, "complaints")
complaints_engine = complaints_index.as_query_engine()

# jazz_packages_df = pd.read_csv(jazz_packages_path)

# desired_order = ['ID', 'Package Name', 'Type', 'Subscription Code', 'On Network Calls Base Rate',
#        'On Network Calls Tax', 'PTCL Calls Base Rate', 'PTCL Calls Tax',
#        'FNF Calls Base Rate', 'FNF Calls Tax', 'Off Network Calls Base Rate',
#        'Off Network Calls Tax', 'Off Network Calls 2nd Pulse',
#        'Off Network SMS Base Rate', 'Off Network SMS Tax',
#        'Off Network SMS 2nd Pulse', 'On Network SMS Base Rate',
#        'On Network SMS Tax', 'On Network SMS 2nd Pulse',
#        'International SMS Base Rate', 'International SMS Tax',
#        'International SMS 2nd Pulse', 'MMS 50KB', 'Data MB',
#        'Total Incentives Minutes', 'PTCL Incentives Minutes',
#        'FNF Incentives Minutes', 'On Network Incentives Minutes',
#        'Off Network Incentives Minutes', '2G/3G Incentives Minutes',
#        'Local Network SMS', 'SMS Line Rental', 'NWD Security Deposit',
#        'ISD Security Deposit', 'IR Security Deposit', 'Notes', 'Remarks',
#        'FNF Numbers', 'FNF Base Rate', 'FNF Tax', 'FNF 2nd Pulse',
#        'Calls Pulse Rate', 'Setup Calls Charges', 'GPRS MB', 'Daily Charges',
#        'Importance Level', 'Work Code', 'Offers',
#        'Data Offers', 'IDD Offers']

# jazz_packages_df = jazz_packages_df[desired_order]

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
    QueryEngineTool(query_engine=complaints_engine, metadata=ToolMetadata(
        name="jazz_complaints",
        description="this gives help about frequent jazz complaints, SOPs, information about Sims, and Jazz WhatsApp in both English and Urdu scripts.",
    ),
    ),
    ]


#print(jazz_packages_query_engine.query("What are the off network charges for Jazz One"))
st.title("Ask J-Bot")



# llm_name = st.selectbox(
#      "Which LLM?", ["text-davinci-003", "gpt-3.5-turbo", "gpt-4"]
# )
llm_name = st.selectbox(
     "Which LLM?", ["models/gemini-pro"]
)

llm = Gemini(model_name = llm_name)

if "messages" not in st.session_state:
    st.session_state.messages = []



for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):

    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content":prompt})
    
    agent = ReActAgent.from_tools(tools, llm = llm, verbose= True, context=context)

    response = agent.query(prompt)
    
    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content":response})
#while (prompt := input("Enter a prompt (q to quit): ")) != "q":
 #   result = agent.query(prompt)
  #  print(result)

# print(jazz_packages_df.head())

