from typing import List, Dict, Any

class TrailFilter:
    @staticmethod
    def filter_trails(
        trails: List[Dict[str, Any]],
        min_length: float = 0,
        max_length: float = float('inf'),
        difficulty: int = None
    ) -> List[Dict[str, Any]]:
        """
        Filtruje szlaki na podstawie podanych kryteriów.
        
        Args:
            trails: Lista słowników z danymi o szlakach
            min_length: Minimalna długość szlaku w km
            max_length: Maksymalna długość szlaku w km
            difficulty: Wymagany poziom trudności (1-3)
            
        Returns:
            Lista przefiltrowanych szlaków
        """
        filtered = trails

        # Filtrowanie po długości
        filtered = [
            trail for trail in filtered
            if min_length <= trail.get('length_km', 0) <= max_length
        ]

        # Filtrowanie po trudności jeśli określona
        if difficulty is not None:
            filtered = [
                trail for trail in filtered
                if trail.get('difficulty') == difficulty
            ]

        return filtered 