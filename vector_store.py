import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
def create_vector_store(chunks):
    if not chunks:
        raise ValueError("No text chunks available to index.")
    model = SentenceTransformer(MODEL_NAME)
    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True
    )
    embeddings = np.asarray(embeddings, dtype=np.float32)
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)
    return index, model
def search_similar(query, index, model, chunks, k=4):
    if not chunks:
        return []
    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    )
    query_embedding = np.asarray(
        query_embedding,
        dtype=np.float32
    )
    number_to_search = min(k, len(chunks))
    scores, indices = index.search(
        query_embedding,
        number_to_search
    )
    results = []
    for score, chunk_index in zip(scores[0], indices[0]):
        if chunk_index == -1:
            continue
        result = chunks[int(chunk_index)].copy()
        result["score"] = float(score)
        results.append(result)
    return results