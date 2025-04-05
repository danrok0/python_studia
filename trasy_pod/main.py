from modules.loader import load_trails_data, load_weather_data
from modules.api_loader import fetch_trails_from_api, fetch_weather_from_api
from modules.recommendation import generate_recommendations
from modules.data_processing import filter_trails, filter_weather
from modules.output_handler import save_to_json
import json

def get_user_preferences():
    print("Podaj preferencje użytkownika:")
    try:
        temp_min = float(input("Minimalna temperatura [°C]: "))
        temp_max = float(input("Maksymalna temperatura [°C]: "))
        sun_min = float(input("Minimalna liczba godzin słonecznych: "))
        sun_max = float(input("Maksymalna liczba godzin słonecznych: "))
        precip_min = float(input("Minimalna ilość opadów [mm]: "))
        precip_max = float(input("Maksymalna ilość opadów [mm]: "))
    except ValueError:
        print("Błąd: Wprowadź poprawne wartości liczbowe.")
        return None

    return {
        "temperature": (temp_min, temp_max),
        "sunshine_hours": (sun_min, sun_max),
        "precipitation": (precip_min, precip_max),
    }

def main():
    trails_data = load_trails_data('data/trails_data.json')
    weather_data = load_weather_data('data/weather_data.json')

    if not trails_data:
        print("Brak danych o trasach w plikach. Pobieranie z API...")
        trails_data = fetch_trails_from_api()
        save_to_json(trails_data, 'data/trails_data.json')

    if not weather_data:
        print("Brak danych pogodowych w plikach. Pobieranie z API...")
        weather_data = fetch_weather_from_api()
        save_to_json(weather_data, 'data/weather_data.json')

    # Sprawdzamy, czy dane pogodowe zostały prawidłowo wczytane
    if weather_data is None:
        print("Brak poprawnych danych pogodowych.")
        return

    print("Dane pogodowe:", weather_data)  # Logowanie danych pogodowych w celu diagnozy

    # Filtrujemy dane
    trails_data = filter_trails(trails_data, min_length=5, max_difficulty=3)
    weather_data = filter_weather(weather_data, min_temperature=10, max_temperature=35)

    # Sprawdzamy, czy dane pogodowe zostały poprawnie przefiltrowane
    print("Przefiltrowane dane pogodowe:", weather_data)

    user_preferences = get_user_preferences()
    if not user_preferences:
        return

    recommendations = generate_recommendations(trails_data, weather_data, user_preferences)

    if recommendations:
        print(f"Znaleziono {len(recommendations)} rekomendacji tras:")
        for recommendation in recommendations:
            print(f"Trasa: {recommendation['name']}, Region: {recommendation['region']}")
        save_to_json(recommendations, 'data/recommendations.json')
    else:
        print("Brak tras pasujących do podanych preferencji.")



if __name__ == '__main__':
    main()

