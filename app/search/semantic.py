import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


model = SentenceTransformer("all-MiniLM-L6-v2")
_faiss_index = None
_product_ids = None

def load_products() -> list[dict]:
    with (open('data/products.json')) as file:
        products = json.load(file)
    return products

def create_embedding_texts(products: list[dict]) -> list[str]:
    texts = []
    for product in products:
        texts.append(product['name'] + ' ' + product['description'])
    return texts

def embed_texts(texts: list[str]) -> np.ndarray:
    embeddings = model.encode(texts)
    return embeddings.astype('float32')

def save_index(vectors: np.ndarray, product_ids: list[int]) -> None:
    # create FAISS index, add vectors, save to disk
    # save product_ids list to disk
    dimension = vectors.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(vectors)
    faiss.write_index(index, "faiss.index")
    np.save("product_ids.npy", product_ids)

def build_index(products: list[dict]) -> None:
    texts = create_embedding_texts(products)
    vectors = embed_texts(texts)
    ids = [p['id'] for p in products]
    save_index(vectors, ids)

def load_index() -> None:
    global _faiss_index, _product_ids  # add this
    _faiss_index = faiss.read_index("faiss.index")
    _product_ids = np.load("product_ids.npy")

def embed_query(query: str) -> np.ndarray:
    query_vector = model.encode([query], convert_to_numpy=True)
    return query_vector.astype('float32')

def semantic_search(query: str, limit: int = 50) -> list[tuple[int, int]]:
    query_vector = embed_query(query)
    distances, indices = _faiss_index.search(query_vector, limit)
    results = []
    for rank, ind in enumerate(indices[0], start=1):
        product_id = int(_product_ids[ind])
        results.append((product_id, rank))
    return results