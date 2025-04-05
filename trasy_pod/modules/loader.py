import json


def load_trails_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Plik {file_path} nie został znaleziony.")
        return []
    except json.JSONDecodeError:
        print(f"Błąd wczytywania danych z pliku {file_path}.")
        return []

def load_weather_data(filepath):
    """
    Wczytuje dane pogodowe z pliku JSON.
    """
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
            if not data.get("daily"):
                print("Brak danych o pogodzie w sekcji 'daily'. Sprawdź format pliku.")
                return None
            return data
    except FileNotFoundError:
        print(f"Plik {filepath} nie został znaleziony.")
        return None
    except json.JSONDecodeError:
        print(f"Błąd wczytywania pliku JSON {filepath}. Sprawdź jego poprawność.")
        return None
