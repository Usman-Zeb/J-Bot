# app/main.py
from fastapi import FastAPI
from app.index_generator import generate_indexes
from app.index_listener import start_listener
from typing import Dict
from app.api import router as api_router
from llama_index.core import VectorStoreIndex

app = FastAPI()
indexes: Dict[str, VectorStoreIndex] = {}

def update_indexes(csv_path):
    global indexes
    indexes = generate_indexes(csv_path=csv_path)
    print("Indexes updated")

@app.on_event("startup")
def startup_event():
    # update_indexes()
    start_listener(update_indexes)
app.include_router(api_router)
