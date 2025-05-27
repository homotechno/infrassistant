"""
RAG (Retrieval-Augmented Generation) helper module.

This module queries the ChromaDB collection to retrieve similar historical
PostgreSQL incident solutions based on input text.
"""

from backend.db.chroma import collection


def find_similar_solution(query_text: str, top_k: int = 3, metadata_filter: dict = None) -> list[str]:
    """
    Finds the most similar solutions from the ChromaDB knowledge base.

    Args:
        query_text (str): The user's query or prompt.
        top_k (int): Number of top results to retrieve. Default is 3.
        metadata_filter (dict, optional): Optional filter for metadata fields.

    Returns:
        list[str]: A list of retrieved solution texts.
    """
    query_args = {"query_texts": [query_text], "n_results": top_k}
    if metadata_filter:
        query_args["where"] = metadata_filter

    results = collection.query(**query_args)
    metadatas = results.get("metadatas", [[]])[0]

    return [meta.get("solution") for meta in metadatas if meta.get("solution")]
