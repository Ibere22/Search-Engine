Feb 20, 18:00–20:00:
Did: Read the assignment
Decided I should aim for a realistic search stack (semantic + keyword) instead of a minimal “just works” solution so it better aligns with Briano’s AI/vector‑search focus.

Feb 21, 12:00–14:00:
Did: Re‑read the task, brainstormed possible approaches (pure text search, SQLite FTS5, Meilisearch, vector/semantic search) and searched online/docs for each option. Asked AI for pros/cons of Meilisearch vs SQLite and how FAISS/embeddings fit in.
Confused about: Whether simpler SQLite FTS5 + FAISS would be easier to learn and debug than Meilisearch + FAISS given my experience, and how much typo tolerance vs semantic matching really matters for the interview.
Changed: Narrowed the stack options down to two serious candidates: (1) SQLite FTS5 + FAISS and (2) Meilisearch + FAISS, with FAISS/vector embeddings as the “AI layer” in both.

Feb 21, 15:00–17:00:
Did: Finalized a detailed multi‑day plan (stack, architecture, schedule). Designed a clean folder layout with `app/`, `api/`, `services/`, `search/`, `data/`, and `front/`. Read focused docs and quickstarts for Meilisearch, embeddings, FAISS, and RRF to get familiar with those themes before coding.
Confused about: Whether to introduce Docker at all, how much of Meilisearch’s features I really needed, and if I should rely on Meilisearch’s built‑in hybrid search instead of building my own FAISS + RRF pipeline.
Changed: Decided to use Docker only for Meilisearch (for a better reviewer experience) but keep the FastAPI app as a normal process. Chose to implement my own FAISS + RRF hybrid search pipeline instead of Meilisearch’s built‑in hybrid mode so the project wouldn't be just 3 files and too simple.

Feb 21, 17:00–19:00:
Did: Created the git repo and local project structure (`app`, `data`, `front` etc.), set up a virtual environment, wrote `requirements.txt`, and created `docker-compose.yml` for Meilisearch. Launched Meilisearch via Docker and confirmed the dashboard at `localhost:7700`.
Confused about: How much Docker adds for this small project versus just running the Meilisearch binary, and how index persistence behave across `docker compose down` vs `down -v`.
Changed: Kept Docker for Meilisearch because it simplifies the reviewer experience and added volume handling notes (using `down -v` only when I want a full clean slate).

Feb 21, 19:00–21:00:
Did: Implemented the first version of `app/indexer.py` to load `data/products.json`, push all 10k products to Meilisearch, and configure searchable/filterable attributes and typo tolerance. Ran it and verified documents appear in the Meilisearch dashboard.
Confused about: Meilisearch’s async task model (why `add_documents` returns a TaskInfo) and whether settings like searchable attributes and typo tolerance need `wait_for_task` as well.
Changed: Updated `indexer.py` to capture the returned TaskInfo from every operation and call `wait_for_task(task.task_uid)` for each step so indexing and settings apply in order.

Feb 21, 21:00–23:00:
Did: Tuned Meilisearch settings: chose `['name', 'description', 'brand', 'country']` as searchable, `['price', 'country', 'brand', 'inStock']` as filterable, and added typo tolerance config for 4+ character words. Wrote `.env` for URL/master key.
Confused about: Which fields should be searchable vs only filterable (especially `country` and `brand`), and what typo tolerance thresholds avoid too many false positives on short words.
Changed: Lowered `oneTypo` threshold to 4 characters to catch common brand/product typos, added `country` and `brand` to both searchable and filterable attributes, and moved Meilisearch credentials from code into `.env`.

Feb 22, 12:00–14:00:
Did: Read Meilisearch quickstart and the Python client README more carefully, and experimented in the dashboard with manual document inserts and queries. Started `app/search/client.py` as a single place to create the Meilisearch client from `.env`.
Settled on a shared `get_client()` helper, decided to always configure searchable/filterable/sortable attributes via the indexer.

Feb 22, 14:00–16:00:
Did: Implemented `app/search/keyword.py` with `keyword_search(query, filters, limit)` that calls Meilisearch and returns `(product_id, rank)` tuples. Added a `build_filters(filters)` helper to convert a Python dict into Meilisearch filter strings.
Confused about: How to correctly pass filters (dict vs list of strings) and why I needed to preserve rank instead of just returning product IDs.
Changed: Refactored `keyword_search` to build the proper `filter` list and to use `enumerate(results['hits'], start=1)` so each result carries an explicit rank for later use in the RRF formula.

Feb 22, 16:00–18:00:
Did: Read sentence‑transformers and FAISS “getting started” docs to understand embeddings and vector indexes. Started `app/search/semantic.py` with helpers to load products, build `name + description` texts, and embed them with `all-MiniLM-L6-v2`.
Confused about: FAISS terminology (xb vs xq) and how to map FAISS internal positions back to real product IDs from the JSON file.
Changed: Designed the semantic indexing flow to build a vector matrix (xb) and a parallel `product_ids` list, and decided to save both with `faiss.write_index` and `np.save` so I can reload them quickly instead of recomputing embeddings on every startup.

Feb 22, 18:00–20:00:
Did: Finished `semantic.py` with `build_index`, `save_index`, `load_index`, `embed_query`, and `semantic_search`. Built the initial FAISS index over all 10k products and wrote a basic test script to query `"warm winter jacket"`.
Confused about: Data types and shapes expected by FAISS (`float32`, `(1, dim)` vs `(dim,)`) and why `_faiss_index` remained `None` after loading.
Changed: Enabled `convert_to_numpy=True` and `astype('float32')` on all embedding calls, introduced module‑level variables for `_faiss_index` and `_product_ids`, and used `global` in `load_index()` so they remain available across calls to `semantic_search`.


Feb 23, 12:00–14:00:
Did: Implemented `app/models.py` with `ProductResult`, `SearchRequest`, and `SearchResponse` using Pydantic.
Confused about: Whether to accept a generic `filters` dict in the API vs explicit typed query parameters for each filter.
Changed: Chose explicit fields in `SearchRequest` and in the route signature (typed `min_price`, `max_price`, `country`, `brand`, `inStock`, `limit`) so FastAPI/Pydantic can validate input types and avoid injection attacks.

Feb 23, 14:00–16:00:
Did: Implemented `app/service/search_service.py` to combine keyword search, semantic search, RRF hybrid merging, and mapping product IDs to full product dicts. Added an `apply_filters` step after RRF to enforce filters on the merged result set.
Confused about: how to correctly handle empty queries and FAISS (which doesn’t support filters directly).
Changed: Loaded treated empty `q` as “keyword only” (just show everything) and applied filters twice (once in Meilisearch via filter strings, once in Python after RRF) to ensure the final results respect give filter constraints.

Feb 23, 16:00–18:00:
Did: Wrote `app/main.py` with a FastAPI `lifespan` context that builds the FAISS index if needed and always calls `load_index()` on startup. Added CORS middleware so the static HTML frontend can talk to the API without browser errors.
Confused about: Whether to rebuild FAISS every time the app starts vs only when the index file is missing, and the best place (startup vs first request) to pay the semantic startup cost.
Changed: Implemented a “build once, load on every startup” pattern: if `faiss.index` is missing, build it; otherwise just load. This keeps first user searches fast and makes the behavior easy to explain.

Feb 23, 18:00–20:00:
Did: Implemented `app/api/routes.py` with `/health`, `/filters`, and `/search` endpoints.
Confused about: Handling empty queries from the UI (should filters alone be allowed?)
Changed: Made `q` optional (default empty string) and treated empty queries as  using only keyword results.

Feb 23, 20:00–23:00:
Did: Built `front/index.html` (with AI help for design and CSS) as a single‑page UI: search bar, country/brand dropdowns, price range inputs, in‑stock toggle, loading and error states, and result cards. Hooked it up to `/filters` and `/search`, added initial “load all” behavior, and tested a variety of queries and filter combinations end‑to‑end.

Feb 24, 12:00–16:00:
Did: Wrote and refined `README.md` (what I built, how to run, example queries) and `DOCS.md` (high‑level search explanation, what I built vs reused, and strengths/weaknesses).Did a fresh run from scratch following the README to validate the setup.
