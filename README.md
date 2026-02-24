## Search Engine

A hybrid product search engine over 10,000 items that combines **keyword search (Meilisearch)** with **semantic search (FAISS + sentence-transformers)**.  
Users can search by text, filter by price/country/brand/stock, and see results in a modern single-page UI.

---

### What I Built

This project is a small, production-style search stack for an online shop:

- A **FastAPI backend** that exposes `/search`, `/filters`, and `/health` endpoints.
- A **hybrid search pipeline** that:
  - Uses **Meilisearch** for fast keyword search and typo tolerance.
  - Uses **FAISS + sentence-transformers** for semantic similarity search.
  - Merges both with **Reciprocal Rank Fusion (RRF)**.
- A **single-page frontend** (`front/index.html`) that calls the API and renders product cards with filters and loading/error states.

The goal is to provide a realistic search experience (not just a simple SQL `LIKE`) while keeping the setup simple enough to run locally.

---

### Tech Stack

- **Backend**: FastAPI, Pydantic
- **Keyword Search**: Meilisearch (Docker)
- **Semantic Search**: FAISS, `sentence-transformers` (`all-MiniLM-L6-v2`)
- **Data / ETL**: JSON products file, Python indexing script
- **Frontend**: Vanilla HTML/CSS/JS single page
- **Infra / Config**: Docker Compose, `.env` for Meilisearch config

---

## How to Run It (Step by Step)

### 1. Prerequisites

- **Python** 3.13  
- **Docker** and **docker compose**
- Internet access the first time (to download the embedding model)

### 2. Clone and enter the project

```bash
git clone <your-repo-url> Search-Engine
cd Search-Engine
```

### 3. Create and activate a virtual environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
# source .venv/bin/activate
```

### 4. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Meilisearch connection

Create a `.env` file in the project root:

```env
URL=http://localhost:7700
MASTER_KEY=masterkey123
```

Docker starts Meilisearch with this master key, and the app connects using these values.

### 6. Start Meilisearch with Docker

```bash
docker compose up -d
```

You can verify it’s running by opening `http://localhost:7700` in your browser.

### 7. Index the products into Meilisearch

This loads `data/products.json` into Meilisearch and configures searchable/filterable fields.

```bash
python app/indexer.py
```

### 8. Start the FastAPI backend

On first run, the app will also build the FAISS index if it doesn’t find `faiss.index` yet (this can take a couple of minutes the first time).

```bash
uvicorn app.main:app --reload --port 8000
```

- API base URL: `http://localhost:8000`  
- Docs: `http://localhost:8000/docs`

### 9. Open the frontend

Open `front/index.html` in your browser (double-click or serve it via a simple static server).

It will call:

- `GET http://localhost:8000/filters`
- `GET http://localhost:8000/search?...`

---

## Example Queries to Try

- **Keyword-focused**
  - `laptop`
  - `running shoes`
  - `bluetooth speaker`
- **Semantic / “idea” queries**
  - `something for cold weather`
  - `office supplies`
  - `music listening`
- **Typos / messy input**
  - `wireles headphons`
  - `laptp`
  - `   bluetooth   speaker   `
  - `LAPTOP`
- **With filters**
  - Laptop bags under `$500` (set max price)
  - In-stock products from `Belgium`
  - filter with brand name Cipher

