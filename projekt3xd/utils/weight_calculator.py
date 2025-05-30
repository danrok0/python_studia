from typing import Dict, Any, List

class WeightCalculator:
    """
    Klasa do obliczania ważonych wyników rekomendacji tras.
    """
    
    def __init__(self):
        self.weights = {
            'trudność': 0.0,
            'długość': 0.0,
            'pogoda': 0.0,
            'teren': 0.0
        }
    def get_weights_from_user(self) -> Dict[str, float]:
        """
        Pobiera wagi od użytkownika dla różnych kryteriów.
        Suma wag musi wynosić 1.0.
        """
        print("\nPodaj wagi dla kryteriów (liczby dziesiętne, suma musi wynosić 1.0):")
        remaining = 1.0
        criteria = list(self.weights.keys())
        
        for i, criterion in enumerate(criteria):
            if i == len(criteria) - 1:  # Ostatnie kryterium
                if remaining > 0:
                    self.weights[criterion] = remaining
                    print(f"{criterion.capitalize()}: {remaining:.2f} (automatycznie przypisana pozostała waga)")
                else:
                    self.weights[criterion] = 0.0
                    print(f"{criterion.capitalize()}: 0.00 (brak pozostałej wagi)")
                break
                
            while True:
                try:
                    if remaining <= 0:
                        self.weights[criterion] = 0.0
                        print(f"{criterion.capitalize()}: 0.00 (brak pozostałej wagi)")
                        break
                        
                    weight = float(input(f"{criterion.capitalize()} (pozostało {remaining:.2f}): "))
                    if weight < 0 or weight > remaining:
                        print(f"Waga musi być między 0 a {remaining:.2f}")
                        continue
                        
                    self.weights[criterion] = weight
                    remaining = round(remaining - weight, 2)  # Zaokrąglamy do 2 miejsc po przecinku
                    break
                except ValueError:
                    print("Podaj poprawną liczbę dziesiętną")
        
        return self.weights
    
    def calculate_weighted_score(self, trail: Dict[str, Any], weather: Dict[str, Any]) -> float:
        """
        Oblicza ważony wynik dla trasy na podstawie ustalonych wag.
        """
        score = 0.0
        
        # Składnik trudności (1-3 -> przekształcone na 0-100)
        if self.weights['trudność'] > 0:
            difficulty_score = (4 - trail.get('difficulty', 1)) * 33.33  # Odwrócona skala: łatwiejsze trasy = wyższy wynik
            score += difficulty_score * self.weights['trudność']
        
        # Składnik długości (optymalna długość 5-15km)
        if self.weights['długość'] > 0:
            length = trail.get('length_km', 0)
            if length < 5:
                length_score = 70  # Krótkie trasy
            elif length <= 15:
                length_score = 100  # Optymalna długość
            elif length <= 25:
                length_score = 80  # Dłuższe trasy
            else:
                length_score = 60  # Bardzo długie trasy
            score += length_score * self.weights['długość']
        
        # Składnik pogody (używa indeksu komfortu)
        if self.weights['pogoda'] > 0 and 'comfort_index' in trail:
            score += trail['comfort_index'] * self.weights['pogoda']
        
        # Składnik terenu (bonus dla preferowanego typu)
        if self.weights['teren'] > 0:
            terrain_scores = {
                'górski': 90,    # Trasy górskie
                'leśny': 85,     # Trasy leśne
                'nizinny': 80,   # Trasy nizinne
                'miejski': 70    # Trasy miejskie
            }
            terrain_type = trail.get('terrain_type', '').lower()
            terrain_score = terrain_scores.get(terrain_type, 75)  # Domyślnie 75 dla innych typów
            score += terrain_score * self.weights['teren']
            
        return round(score, 2)
    
    def sort_trails_by_weights(self, trails: List[Dict[str, Any]], weather: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Sortuje trasy według ich ważonych wyników.
        """
        for trail in trails:
            trail['weighted_score'] = self.calculate_weighted_score(trail, weather)
            
        return sorted(trails, key=lambda x: x.get('weighted_score', 0), reverse=True)
