from sentence_transformers import SentenceTransformer

from app.config import settings
from app.services.query_cache_service import query_cache

_model_cache: dict[str, SentenceTransformer] = {}


def _get_model(model_name: str) -> SentenceTransformer:
    if model_name not in _model_cache:
        _model_cache[model_name] = SentenceTransformer(model_name)
    return _model_cache[model_name]


def embed_texts(texts: list[str], model: str | None = None) -> list[list[float]]:
    if not texts:
        return []
    if model is None:
        model = settings.embedding_model  # e.g. "all-MiniLM-L6-v2"

    results: list[list[float] | None] = [None] * len(texts)

    miss_indices: list[int] = []
    miss_texts: list[str] = []

    for i, text in enumerate(texts):
        cached = query_cache.get_embedding(text)
        if cached is not None:
            results[i] = cached
        else:
            miss_indices.append(i)
            miss_texts.append(text)  # fixed: was appending i (index) instead of text

    if miss_texts:
        st_model = _get_model(model)
        vectors = st_model.encode(miss_texts, convert_to_numpy=True).tolist()
        for idx_in_misses, vector in enumerate(vectors):
            original_idx = miss_indices[idx_in_misses]
            results[original_idx] = vector
            query_cache.set_embedding(miss_texts[idx_in_misses], vector)

    return [r for r in results if r is not None]