

def hybrid_search(
    keyword_results: list[tuple[int, int]], 
    semantic_results: list[tuple[int, int]],
    limit: int = 10
) -> list[int]:

    scores = {}
    for product_id, rank in keyword_results:
        scores[product_id] = scores.get(product_id, 0) + 1 / (60 + rank)
    for product_id, rank in semantic_results:
        scores[product_id] = scores.get(product_id, 0) + 1 / (60 + rank)
    sorted_ids = sorted(scores, key=lambda id: scores[id], reverse=True)
    return sorted_ids[:limit]

