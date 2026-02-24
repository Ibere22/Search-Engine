import time
from fastapi import APIRouter
from app.service import search_service
from app.models import SearchResponse
from app.service.search_service import get_filter_options

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.get("/filters")
def get_filters():
    return get_filter_options()


@router.get("/search", response_model=SearchResponse)
def search_endpoint(
        q: str = "",
        min_price: float | None = None,
        max_price: float | None = None,
        country: str | None = None,
        brand: str | None = None,
        inStock: bool | None = None,
        limit: int = 10

):
    start_time = time.time()

    filters = {
        "min_price": min_price,
        "max_price": max_price,
        "country": country,
        "brand": brand,
        "inStock": inStock
    }

    results = search_service.search(query=q, limit=limit, filters=filters)

    end_time = time.time()
    duration = int((end_time - start_time) * 1000)

    return SearchResponse(
        query=q,
        total_hits=len(results),
        took_ms=duration,
        results=results
    )