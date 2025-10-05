# config.py
from dotenv import load_dotenv
import os

# Load environment variables first, before any other imports
load_dotenv()

# Validate required environment variables
required_vars = ["OPENAI_API_KEY", "PINECONE_API_KEY", "INDEX_NAME"]
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    raise EnvironmentError(
        f"Missing required environment variables: {', '.join(missing_vars)}\n"
        f"Please check your .env file."
    )

# Export for use in other modules
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("INDEX_NAME")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")