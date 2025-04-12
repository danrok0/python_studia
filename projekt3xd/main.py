import os
import sys
import json
from datetime import datetime

# Dodaj katalog projektu do ścieżki Pythona
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

from data_handlers.trail_data import TrailDataHandler
from data_handlers.weather_data import WeatherDataHandler
from utils.trail_filter import TrailFilter
from utils.storage import save_results_to_file
from config import CITY_COORDINATES
from recommendation.trail_recommender import TrailRecommender

def main():
    recommender = TrailRecommender()
    
    print("\n=== System rekomendacji szlaków turystycznych ===")
    print("Dostępne miasta: Gdańsk, Warszawa, Kraków, Wrocław")
    city = input("Wybierz miasto: ").strip()
    
    if city not in CITY_COORDINATES:
        print(f"Nieprawidłowe miasto. Wybierz jedno z: {', '.join(CITY_COORDINATES.keys())}")
        return

    # Choose data type
    print("\nWybierz typ danych pogodowych:")
    print("1. Dane historyczne (przeszłość)")
    print("2. Prognoza pogody (teraźniejszość i przyszłość)")
    data_type = input("Wybierz opcję (1 lub 2): ").strip()
    
    if data_type not in ["1", "2"]:
        print("Nieprawidłowy wybór. Wybierz 1 lub 2.")
        return

    # Get date input
    while True:
        date = input("\nPodaj datę (RRRR-MM-DD) lub wciśnij ENTER dla dzisiejszej daty: ").strip()
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
            break
        try:
            input_date = datetime.strptime(date, "%Y-%m-%d")
            today = datetime.now()
            
            if data_type == "1" and input_date.date() > today.date():
                print("Dla danych historycznych wybierz datę z przeszłości.")
                continue
            elif data_type == "2" and input_date.date() < today.date():
                print("Dla prognozy pogody wybierz datę dzisiejszą lub przyszłą.")
                continue
                
            break
        except ValueError:
            print("Nieprawidłowy format daty. Użyj formatu RRRR-MM-DD (np. 2024-03-20)")

    print("\nPodaj kryteria wyszukiwania (naciśnij ENTER, aby pominąć):")
    difficulty = input("Poziom trudności (1-3): ")
    terrain_type = input("Typ terenu (górski, nizinny, leśny, miejski): ")
    min_length = input("Minimalna długość trasy (km): ")
    max_length = input("Maksymalna długość trasy (km): ")
    min_sunshine = input("Minimalna liczba godzin słonecznych: ")
    max_precipitation = input("Maksymalne opady (mm): ")
    min_temperature = input("Minimalna temperatura (°C): ")
    max_temperature = input("Maksymalna temperatura (°C): ")
    
    # Konwersja parametrów
    difficulty = int(difficulty) if difficulty else None
    terrain_type = terrain_type.lower() if terrain_type else None
    min_length = float(min_length) if min_length else None
    max_length = float(max_length) if max_length else None
    min_sunshine = float(min_sunshine) if min_sunshine else None
    max_precipitation = float(max_precipitation) if max_precipitation else None
    min_temperature = float(min_temperature) if min_temperature else None
    max_temperature = float(max_temperature) if max_temperature else None
    
    trails = recommender.recommend_trails(
        city=city,
        date=date,
        difficulty=difficulty,
        terrain_type=terrain_type,
        min_length=min_length,
        max_length=max_length,
        min_sunshine=min_sunshine,
        max_precipitation=max_precipitation,
        min_temperature=min_temperature,
        max_temperature=max_temperature
    )
    
    if trails:
        print("\nZnalezione trasy:")
        for i, trail in enumerate(trails, 1):
            print(f"\n{i}. {trail['name']}")
            print(f"   Długość: {trail['length_km']} km")
            print(f"   Poziom trudności: {trail['difficulty']}/3")
            print(f"   Typ terenu: {trail['terrain_type']}")
            if 'description' in trail:
                print(f"   Opis: {trail['description']}")
    else:
        print("\nNie znaleziono tras spełniających podane kryteria.")

if __name__ == "__main__":
    main() 