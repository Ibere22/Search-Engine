import app.search.keyword as keyword
import app.search.semantic as semantic
import app.search.hybrid as hybrid
import json

with (open('data/products.json')) as file:
    _products = json.load(file)


_products_map = {}
for product in _products:
    _products_map[product['id']] = product

_unique_countries = sorted(set(p['country'] for p in _products))
_unique_brands = sorted(set(p['brand'] for p in _products))


def get_filter_options() -> dict:
    return {
        "countries": _unique_countries,
        "brands": _unique_brands
    }


def search(query: str, filters: dict, limit: int = 10) -> list[dict]:
    keyword_results = keyword.keyword_search(query, filters, limit = 50)
    if query.strip():
        semantic_results = semantic.semantic_search(query, limit = 50)
        product_ids = hybrid.hybrid_search(keyword_results, semantic_results, limit = limit)
    else:
        product_ids = [pid for pid, rank in keyword_results]

    results = []
    for product_id in product_ids:
        product = _products_map[product_id]
        results.append(product)
    results = apply_filters(results, filters)
    return results[:limit]


def apply_filters(products: list[dict], filters: dict) -> list[dict]:
    if filters.get('min_price') is not None:
        products = [p for p in products if p['price'] >= filters['min_price']]
    if filters.get('max_price') is not None:
        products = [p for p in products if p['price'] <= filters['max_price']]
    if filters.get('country'):
        products = [p for p in products if p['country'] == filters['country']]
    if filters.get('brand'):
        products = [p for p in products if p['brand'] == filters['brand']]
    if filters.get('inStock') is not None:
        products = [p for p in products if p['inStock'] == filters['inStock']]
    return products