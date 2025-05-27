"""
ChromaDB vector store setup for Retrieval-Augmented Generation (RAG).
Initializes a persistent client and collection with a multilingual embedding model.
"""

from backend.config import CHROMA_PATH
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# Initialize the sentence transformer embedding model
embedding_function = SentenceTransformerEmbeddingFunction(
    model_name="paraphrase-multilingual-MiniLM-L12-v2"
)

# Initialize ChromaDB persistent client
client = chromadb.PersistentClient(path=str(CHROMA_PATH))

# Create or load the 'postgres' collection for storing embedded documents
collection = client.get_or_create_collection(
    name="postgres",
    embedding_function=embedding_function
)
