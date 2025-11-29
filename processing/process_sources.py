from dotenv import load_dotenv
from sqlalchemy import create_engine
import os
from contextlib import contextmanager
import pandas as pd 

@contextmanager
def get_engine():
    load_dotenv()
    database_url = os.getenv('DATABASE_URL')
    engine = create_engine(database_url)
    try:
        yield engine    
    finally:
        engine.dispose() #Close connection

def load_source():
    load_dotenv()
    sources = {}
    raw_sources = {}
    for key in os.environ:
        if key.startswith("SOURCE_") and key.endswith("_TYPE"):
            prefix = key.replace("_TYPE", "")
            source_type = os.getenv(f"{prefix}_TYPE")
            source_path = os.getenv(f"{prefix}_PATH")
            if source_type and source_path:
                name = prefix.replace("SOURCE_", "")
                sources[name] = {'type':source_type,
                                'path':source_path}
        elif key.startswith("RAW_") and key.endswith("_TYPE"):
            prefix = key.replace("_TYPE", "")
            raw_type = os.getenv(f"{prefix}_TYPE")
            raw_path = os.getenv(f"{prefix}_PATH")
            if source_type and source_path:
                name = prefix.replace("RAW_", "")
                raw_sources[name] = {'type':raw_type,
                                'path':raw_path}
    return [raw_sources, sources]

def read_source(source):
    if source['type'] == 'csv':
        return pd.read_csv(source['path']) 
    if source['type'] == 'json':
        return pd.read_json(source['path'])
    raise ValueError(f"Source type {source['type']} is not supported")