## Technical Documentation
This document provides a deeper, more technical explanation of how the search engine works, what was built vs. reused, and its strengths and limitations.

---

### How the Search Works (High Level)

1. The frontend calls `GET /search` with the query and optional filters.
2. The backend runs **two searches**:
   - **Meilisearch** keyword search over `name`, `description`, `brand`, `country` (with typo tolerance and filters).
   - **FAISS** semantic search over embeddings of `name + description` using a pretrained sentence-transformer model.
3. Each engine returns a ranked list of product IDs.
4. These lists are merged with **Reciprocal Rank Fusion (RRF)**:
   \[
   score = \sum \frac{1}{60 + rank}
   \]
   Products that are high in both lists get the highest final scores.
5. The backend looks up full product details, applies final filters, and returns the top N products with timing info.
6. The frontend renders product cards and meta information (hits, time, query).

---

### What I Built vs. What I Reused

- **Built myself**
  - API layer (`app/main.py`, `app/api/routes.py`) and request/response models (`app/models.py`).
  - Search service orchestration (`app/service/search_service.py`) and RRF fusion (`app/search/hybrid.py`).
  - Indexer for Meilisearch (`app/indexer.py`) and Meilisearch client wrapper (`app/search/client.py`).
  - Semantic integration and FAISS index lifecycle (`app/search/semantic.py`).
  - Frontend structure and wiring in `front/index.html` (layout, filters, calls to the API), **with AI assistance for the design and styling**.

- **Reused on purpose**
  - **Meilisearch** for keyword search, filtering, and typo tolerance.
  - **sentence-transformers** (`all-MiniLM-L6-v2`) for text embeddings.
  - **FAISS** for fast nearest-neighbor search over embeddings.
  - **FastAPI + Pydantic** for the web API and validation.
  - **Docker Compose** to run Meilisearch reliably.

---

### What Works Well vs. What’s Weak / Unfinished

- **Works well**
  - Hybrid ranking that combines keyword search with semantic understanding.
  - Practical filters (price, country, brand, in-stock).
  - Clear layering: API → service → search backends → data.
  - Simple local setup with Docker + one indexing script.

- **Weak / unfinished**
  - First-time startup does a heavy embedding + FAISS build step.
  - Sorting can be added.
  - Tests are mostly manual scripts rather than a full automated test suite.
  

