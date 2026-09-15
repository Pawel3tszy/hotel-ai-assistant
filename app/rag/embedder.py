from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


model = SentenceTransformer(MODEL_NAME)


def create_embeddings(chunks):
    texts = [chunk["content"] for chunk in chunks]

    embeddings = model.encode(texts)

    for chunk, embedding in zip(chunks, embeddings):
        chunk["embedding"] = embedding

    return chunks