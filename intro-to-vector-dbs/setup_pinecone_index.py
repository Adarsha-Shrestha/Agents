import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

# Load from .env
api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("INDEX_NAME")

# Initialize Pinecone client
pc = Pinecone(api_key=api_key)

# Create index if it doesn't exist
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",        # or "gcp"
            region="us-east-1"       # must match your project setting
        )
    )
    print(f"Index '{index_name}' created.")
else:
    print(f"Index '{index_name}' already exists.")
