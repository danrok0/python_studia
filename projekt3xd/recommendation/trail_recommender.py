from typing import List, Dict, Any, Optional
from data_handlers.trail_data import TrailDataHandler
from functools import reduce
from datetime import datetime

class TrailRecommender:
    def __init__(self):
        """Inicjalizuje obiekt TrailRecommender z obsługą danych."""
        self.data_handler = TrailDataHandler()

    def _save_recommendations_to_file(self, city: str, date: str, trails: List[Dict[str, Any]], weather: Optional[Dict[str, Any]] = None):
        """Zapisuje rekomendacje do pliku result.txt.
        
        Args:
            city (str): Nazwa miasta
            date (str): Data w formacie YYYY-MM-DD
            trails (List[Dict[str, Any]]): Lista znalezionych tras
            weather (Optional[Dict[str, Any]]): Dane pogodowe
        """
        try:
            with open("result.txt", "a", encoding="utf-8") as f:
                f.write(f"\n=== Rekomendacje dla {city} na dzień {date} ===\n")
                f.write(f"Data wygenerowania: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                if weather:
                    f.write("Dane pogodowe:\n")
                    f.write(f"Temperatura: {weather.get('temperature_min', 'N/A')}°C - {weather.get('temperature_max', 'N/A')}°C\n")
                    f.write(f"Średnia temperatura: {weather.get('temperature_avg', 'N/A')}°C\n")
                    f.write(f"Opady: {weather.get('precipitation', 'N/A')} mm\n")
                    f.write(f"Zachmurzenie: {weather.get('cloud_cover', 'N/A')}%\n")
                    f.write(f"Godziny słoneczne: {weather.get('sunshine_hours', 'N/A')} h\n")
                    f.write(f"Prędkość wiatru: {weather.get('wind_speed', 'N/A')} km/h\n\n")
                
                f.write(f"Znaleziono {len(trails)} tras:\n\n")
                for i, trail in enumerate(trails, 1):
                    f.write(f"{i}. {trail['name']}\n")
                    f.write(f"   Długość: {trail.get('length_km', 'N/A')} km\n")
                    f.write(f"   Poziom trudności: {trail.get('difficulty', 'N/A')}/3\n")
                    f.write(f"   Typ terenu: {trail.get('terrain_type', 'N/A')}\n")
                    if 'description' in trail:
                        f.write(f"   Opis: {trail['description']}\n")
                    f.write("\n")
                f.write("=" * 50 + "\n")
            print("\nRekomendacje zostały zapisane do pliku result.txt")
        except Exception as e:
            print(f"Błąd podczas zapisywania rekomendacji do pliku: {e}")

    def recommend_trails(
        self,
        city: str,
        date: str,
        difficulty: Optional[int] = None,
        terrain_type: Optional[str] = None,
        min_length: Optional[float] = None,
        max_length: Optional[float] = None,
        min_sunshine: Optional[float] = None,
        max_precipitation: Optional[float] = None,
        min_temperature: Optional[float] = None,
        max_temperature: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """Rekomenduje trasy na podstawie różnych kryteriów.
        
        Args:
            city (str): Nazwa miasta
            date (str): Data w formacie YYYY-MM-DD
            difficulty (Optional[int]): Poziom trudności (1-3)
            terrain_type (Optional[str]): Typ terenu
            min_length (Optional[float]): Minimalna długość trasy
            max_length (Optional[float]): Maksymalna długość trasy
            min_sunshine (Optional[float]): Minimalna liczba godzin słonecznych
            max_precipitation (Optional[float]): Maksymalne opady
            min_temperature (Optional[float]): Minimalna temperatura
            max_temperature (Optional[float]): Maksymalna temperatura
            
        Returns:
            List[Dict[str, Any]]: Lista znalezionych tras
        """
        try:
            # Pobieranie wszystkich tras dla danego miasta
            trails = self.data_handler.get_trails_for_city(city)
            if not trails:
                print(f"Nie znaleziono tras dla miasta {city}")
                return []

            print(f"\nZnaleziono {len(trails)} szlaków dla miasta {city}")

            # Pobieranie prognozy pogody
            print(f"\nPobieranie danych pogodowych dla {city} na dzień {date}...")
            weather = self.data_handler.weather_api.get_weather_forecast(city, date)
            
            if weather:
                print("\nDane pogodowe:")
                print(f"Temperatura: {weather.get('temperature_min', 'N/A')}°C - {weather.get('temperature_max', 'N/A')}°C")
                print(f"Średnia temperatura: {weather.get('temperature_avg', 'N/A')}°C")
                print(f"Opady: {weather.get('precipitation', 'N/A')} mm")
                print(f"Zachmurzenie: {weather.get('cloud_cover', 'N/A')}%")
                print(f"Godziny słoneczne: {weather.get('sunshine_hours', 'N/A')} h")
                print(f"Prędkość wiatru: {weather.get('wind_speed', 'N/A')} km/h")
            else:
                print("Brak dostępnych danych pogodowych")

            # Funkcja pomocnicza do filtrowania tras
            def filter_trail(trail: Dict[str, Any]) -> bool:
                """Sprawdza czy trasa spełnia wszystkie kryteria.
                
                Args:
                    trail (Dict[str, Any]): Dane trasy
                    
                Returns:
                    bool: True jeśli trasa spełnia kryteria, False w przeciwnym razie
                """
                # Sprawdzanie poziomu trudności
                if difficulty is not None and trail.get('difficulty') != difficulty:
                    return False
                
                # Sprawdzanie typu terenu
                if terrain_type and trail.get('terrain_type') != terrain_type:
                    return False
                
                # Sprawdzanie długości
                if min_length is not None and trail.get('length_km', 0) < min_length:
                    return False
                if max_length is not None and trail.get('length_km', 0) > max_length:
                    return False
                
                # Sprawdzanie warunków pogodowych
                if weather:
                    if min_sunshine is not None and weather.get('sunshine_hours', 0) < min_sunshine:
                        return False
                    if max_precipitation is not None and weather.get('precipitation', 0) > max_precipitation:
                        return False
                    if min_temperature is not None and weather.get('temperature_avg', 0) < min_temperature:
                        return False
                    if max_temperature is not None and weather.get('temperature_avg', 0) > max_temperature:
                        return False
                
                return True

            # Filtrowanie tras używając funkcji filter() i wyrażenia lambda
            filtered_trails = list(filter(lambda t: filter_trail(t), trails))

            # Sortowanie tras używając funkcji sorted() i wyrażenia lambda
            sorted_trails = sorted(
                filtered_trails,
                key=lambda x: (x.get('difficulty', 0), x.get('length_km', 0))
            )

            # Obliczanie średniej długości tras używając funkcji reduce() i wyrażenia lambda
            if sorted_trails:
                total_length = reduce(
                    lambda acc, trail: acc + trail.get('length_km', 0),
                    sorted_trails,
                    0
                )
                avg_length = total_length / len(sorted_trails)
                print(f"\nŚrednia długość znalezionych tras: {avg_length:.1f} km")

            if not sorted_trails:
                print("\nNie znaleziono tras spełniających podane kryteria.")
            else:
                print(f"\nZnaleziono {len(sorted_trails)} tras spełniających kryteria:")

            # Zapisanie rekomendacji do pliku
            self._save_recommendations_to_file(city, date, sorted_trails, weather)

            return sorted_trails

        except Exception as e:
            print(f"Błąd podczas rekomendacji tras: {e}")
            return [] 