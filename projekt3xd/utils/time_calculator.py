from typing import Dict, Any

class TimeCalculator:
    """
    Klasa do obliczania szacowanego czasu przejścia trasy.
    """
    
    @staticmethod
    def calculate_time(trail: Dict[str, Any]) -> float:
        """
        Oblicza szacowany czas przejścia trasy w godzinach.
        
        Args:
            trail: Słownik z danymi trasy
            
        Returns:
            float: Szacowany czas w godzinach
        """
        # Bazowa prędkość: 4 km/h
        base_speed = 4.0
        
        # Modyfikator trudności (im trudniejsza trasa, tym wolniejsze tempo)
        difficulty_multipliers = {
            1: 1.0,  # Łatwa trasa - normalne tempo
            2: 0.8,  # Średnia trasa - 80% normalnego tempa
            3: 0.7   # Trudna trasa - 70% normalnego tempa
        }
        
        # Modyfikator terenu
        terrain_multipliers = {
            'górski': 0.6,      # Góry - 60% normalnego tempa
            'leśny': 0.9,       # Las - 90% normalnego tempa
            'miejski': 1.0,     # Miasto - normalne tempo
            'nizinny': 1.0,     # Teren nizinny - normalne tempo
            'riverside': 0.9,    # Wzdłuż rzeki - 90% normalnego tempa
            'mixed': 0.8        # Teren mieszany - 80% normalnego tempa
        }
        
        difficulty = trail.get('difficulty', 1)
        terrain_type = trail.get('terrain_type', 'mixed').lower()
        length = trail.get('length_km', 0)
        
        # Oblicz efektywną prędkość
        effective_speed = (base_speed * 
                         difficulty_multipliers.get(difficulty, 1.0) * 
                         terrain_multipliers.get(terrain_type, 0.8))
        
        # Oblicz czas w godzinach
        time = length / effective_speed
        
        return round(time, 2)
