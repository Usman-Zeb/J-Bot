# app/index_generator.py
from pathlib import Path
from llama_index.readers.file import CSVReader
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage

# Determine the directory of the current script
script_dir = Path(__file__).resolve().parent


def get_index(data, index_name):
    if not Path(index_name).exists():
        print("Building index", index_name)
        index = VectorStoreIndex.from_documents(data, show_progress=True)
        index.storage_context.persist(persist_dir=index_name)
    else:
        # Remove existing index before creating a new one
        index_dir = Path(index_name)
        for file in index_dir.glob('*'):
            file.unlink()
        
        index = VectorStoreIndex.from_documents(data, show_progress=True)
        index.storage_context.persist(persist_dir=index_name)
        
    return index

def load_index(data, index_name):
    index = None
    if not Path(index_name).exists():
        print("Building index", index_name)
        index = VectorStoreIndex.from_documents(data, show_progress=True)
        index.storage_context.persist(persist_dir=index_name)
    else:
        index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir=index_name)
        )
    return index


def init_indexes():
    indexes = {}
    # Define the CSV files and their corresponding index names
    csv_files = {
        "packages": script_dir / ".." / "data" / "packages.csv",
        "offers": script_dir / ".." / "data" / "offers.csv",
        "data_offers": script_dir.parent / "data" / "dataoffers.csv",
        "complaints": script_dir / ".." / "data" / "complaints.csv"
    }
    
    # Generate indexes for each CSV file
    for index_name, csv_file in csv_files.items():
        csv_data = CSVReader().load_data(csv_file)
        indexes[index_name] = load_index(csv_data, index_name)
    return indexes

def generate_indexes(csv_path):
    indexes = {}
    
    # Define the CSV files and their corresponding index names
    csv_files = {
        "packages": Path(csv_path).parent / "packages.csv",
        "offers": Path(csv_path).parent / "offers.csv",
        "data_offers": Path(csv_path).parent / "dataoffers.csv",
        "complaints": Path(csv_path).parent / "complaints.csv"
    }
    
    # Generate indexes for the modified CSV file only
    if Path(csv_path).name in csv_files.values():
        index_name = [name for name, path in csv_files.items() if path == Path(csv_path).name][0]
        csv_data = CSVReader().load_data(csv_path)
        indexes[index_name] = get_index(csv_data, index_name)
    
    return indexes
