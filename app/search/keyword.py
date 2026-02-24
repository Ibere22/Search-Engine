from app.search.client import get_client

index = get_client().index('products')

def keyword_search(query: str, filters: dict, limit: int = 50) -> list[tuple[int, int]]:
    filter_list = build_filters(filters)
    
    results = index.search(query, {
        'limit': limit,
        'filter': filter_list
    })
    
    formatted_results = []

    for rank, hit in enumerate(results['hits'], start=1):
        
        product_tuple = (hit['id'], rank)
        
        formatted_results.append(product_tuple)
        
    return formatted_results


def build_filters(filters: dict) -> list[str]:
    filter_list = []
    
    if filters.get('min_price') is not None:
        filter_list.append(f"price >= {filters['min_price']}")
    if filters.get('max_price') is not None:
        filter_list.append(f"price <= {filters['max_price']}")
    if filters.get('country'):
        filter_list.append(f'country = "{filters["country"]}"')
    if filters.get('brand'):
        filter_list.append(f'brand = "{filters["brand"]}"')
    if filters.get('inStock') is not None:
        filter_list.append(f"inStock = {str(filters['inStock']).lower()}")
    
    return filter_list