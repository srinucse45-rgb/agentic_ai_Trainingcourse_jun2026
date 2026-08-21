# This example demonstrates only vector search
# This is bad when you are looking for exact keyword based search
# So, we should build a hybrid retrieval that combines both vector search and keyword search (FTS)

from app.core.db import get_vector_store


def retrieve(query: str, k: int = 5):
    """gets the query and searches the vector db and
    finds top-k most similar document chunks for a given query"""
    print(query)
    vector_store = get_vector_store(collection_name="hr_support_desk")
    results = vector_store.similarity_search(query, k)
    print(results)
    return results


if __name__ == "__main__":
    user_query = "Give me home loan plan Loan123"
    retrieve(user_query)


# uv run python -m app.retrieval.retrieval
