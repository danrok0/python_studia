from typing import List, Dict, Any
import json
from datetime import datetime

def save_results_to_file(trails: List[Dict[str, Any]], region: str) -> None:
    """
    Save recommended trails to result.txt file.
    
    Args:
        trails: List of recommended trail dictionaries
        region: Selected region name
    """
    try:
        with open('result.txt', 'w', encoding='utf-8') as f:
            f.write(f"=== Rekomendacje szlaków dla regionu {region} ===\n")
            f.write(f"Data wygenerowania: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            if not trails:
                f.write("Nie znaleziono szlaków spełniających podane kryteria.\n")
                return
                
            for i, trail in enumerate(trails, 1):
                f.write(f"\n{i}. {trail['name']}\n")
                f.write(f"   Długość: {trail.get('length_km', 'brak danych')} km\n")
                f.write(f"   Trudność: {trail.get('difficulty', 'brak danych')}/3\n")
                f.write(f"   Przewidywane godziny słoneczne: {trail.get('sunshine_hours', 'brak danych')}\n")
                
            f.write(f"\nŁącznie znaleziono {len(trails)} tras spełniających kryteria.\n")
            
    except Exception as e:
        print(f"Błąd podczas zapisywania wyników do pliku: {e}") 