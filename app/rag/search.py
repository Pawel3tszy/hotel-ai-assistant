import numpy as np

from app.rag.embedder import model


def cosine_similarity(vector_a, vector_b):
    vector_a = np.array(vector_a)
    vector_b = np.array(vector_b)

    return np.dot(vector_a, vector_b) / (
        np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    )


def search_chunks(query, chunks, top_k=3):
    query_embedding = model.encode(query)

    results = []

    for chunk in chunks:
        similarity = cosine_similarity(
            query_embedding,
            chunk["embedding"]
        )

        results.append({
            "source": chunk["source"],
            "content": chunk["content"],
            "score": float(similarity)
        })

    results.sort(
        key=lambda result: result["score"],
        reverse=True
    )

    return results[:top_k]