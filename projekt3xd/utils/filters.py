from typing import List, Dict, Any

def filter_trails_by_criteria(
    trails: List[Dict[str, Any]],
    region: str = None,
    min_length: float = None,
    max_length: float = None,
    difficulty: int = None
) -> List[Dict[str, Any]]:
    filtered_trails = trails

    if region:
        filtered_trails = list(filter(
            lambda x: x['region'].lower() == region.lower(),
            filtered_trails
        ))

    if min_length is not None:
        filtered_trails = list(filter(
            lambda x: x['length_km'] >= min_length,
            filtered_trails
        ))

    if max_length is not None:
        filtered_trails = list(filter(
            lambda x: x['length_km'] <= max_length,
            filtered_trails
        ))

    if difficulty is not None:
        filtered_trails = list(filter(
            lambda x: x['difficulty'] == difficulty,
            filtered_trails
        ))

    return filtered_trails 