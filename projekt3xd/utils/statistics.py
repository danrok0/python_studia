from typing import List, Dict, Any
from functools import reduce

def calculate_weather_stats(weather_data: List[Dict[str, float]]) -> Dict[str, float]:
    """Oblicza statystyki pogodowe używając funkcji reduce."""
    if not weather_data:
        return {
            "avg_temp": 0.0,
            "total_precipitation": 0.0,
            "sunshine_hours": 0.0
        }

    count = len(weather_data)
    
    # Obliczanie średniej temperatury używając reduce
    total_temp = reduce(lambda acc, x: acc + x['temperature'], weather_data, 0.0)
    avg_temp = total_temp / count

    # Obliczanie całkowitych opadów używając reduce
    total_precipitation = reduce(lambda acc, x: acc + x['precipitation'], weather_data, 0.0)

    # Obliczanie średniej liczby godzin słonecznych używając reduce
    total_sunshine = reduce(lambda acc, x: acc + x['sunshine_hours'], weather_data, 0.0)
    avg_sunshine = total_sunshine / count

    return {
        "avg_temp": round(avg_temp, 2),
        "total_precipitation": round(total_precipitation, 2),
        "sunshine_hours": round(avg_sunshine, 2)
    } 