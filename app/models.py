from pydantic import BaseModel, Field
from typing import Optional, List
class ProductResult(BaseModel):
    id: int
    name: str
    description: str
    price: float
    country: str
    brand: str
    inStock: bool

class SearchRequest(BaseModel):
    query: str
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    country: Optional[str] = None
    brand: Optional[str] = None
    inStock: Optional[bool] = None
    limit: int = 10

class SearchResponse(BaseModel):
    query: str
    total_hits: int
    took_ms: int
    results: List[ProductResult]


