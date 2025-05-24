# Dokumentacja Systemu Rekomendacji Szlaków Turystycznych

## 1. Opis Projektu
System rekomendacji szlaków turystycznych to aplikacja, która pomaga użytkownikom znaleźć odpowiednie szlaki turystyczne na podstawie różnych kryteriów, takich jak lokalizacja, data, poziom trudności, typ terenu, długość trasy oraz warunki pogodowe.

## 2. Główne Komponenty

### 2.1. TrailRecommender
Klasa odpowiedzialna za rekomendowanie szlaków turystycznych.

#### 2.1.1. Elementy Programowania Funkcyjnego

1. **Funkcja filter() i wyrażenia lambda**
```python
filtered_trails = list(filter(lambda t: filter_trail(t), trails))
```
- `filter()` - funkcja wbudowana w Python, która filtruje elementy sekwencji
- `lambda t: filter_trail(t)` - wyrażenie lambda tworzące anonimową funkcję
- Działanie: Przechodzi przez każdą trasę i sprawdza, czy spełnia wszystkie kryteria

2. **Funkcja sorted() i wyrażenia lambda**
```python
sorted_trails = sorted(
    filtered_trails,
    key=lambda x: (x.get('difficulty', 0), x.get('length_km', 0))
)
```
- `sorted()` - funkcja sortująca elementy
- `lambda x: (x.get('difficulty', 0), x.get('length_km', 0))` - wyrażenie lambda określające klucz sortowania
- Działanie: Sortuje trasy najpierw według poziomu trudności, a następnie według długości

3. **Funkcja reduce() i wyrażenia lambda**
```python
total_length = reduce(
    lambda acc, trail: acc + trail.get('length_km', 0),
    sorted_trails,
    0
)
```
- `reduce()` - funkcja z modułu `functools`, która redukuje sekwencję do pojedynczej wartości
- `lambda acc, trail: acc + trail.get('length_km', 0)` - wyrażenie lambda sumujące długości tras
- Działanie: Sumuje długości wszystkich tras, aby obliczyć średnią długość

### 2.2. WeatherAPI
Klasa odpowiedzialna za pobieranie danych pogodowych.

#### 2.2.1. Pobieranie Danych Pogodowych
1. **Dane historyczne**
- Używa endpointu `https://archive-api.open-meteo.com/v1/archive`
- Pobiera dane dla dat z przeszłości
- Zawiera informacje o temperaturze, opadach, zachmurzeniu itp.

2. **Prognoza pogody**
- Używa endpointu `https://api.open-meteo.com/v1/forecast`
- Pobiera dane dla dat przyszłych
- Zawiera podobne informacje jak dane historyczne

#### 2.2.2. Przetwarzanie Danych
- Konwersja jednostek (np. sekundy na godziny dla czasu nasłonecznienia)
- Agregacja danych (np. średnia temperatura)
- Obsługa błędów i brakujących danych

### 2.3. TrailDataHandler
Klasa odpowiedzialna za zarządzanie danymi o szlakach.

#### 2.3.1. Pobieranie Danych
- Pobiera dane z API szlaków turystycznych
- Przetwarza odpowiedź JSON
- Waliduje dane (sprawdza wymagane pola)

#### 2.3.2. Filtrowanie Danych
- Filtruje szlaki według miasta/regionu
- Sprawdza poprawność danych (np. czy długość jest liczbą)
- Obsługuje brakujące dane

## 2.4. Lokalizacja i Działanie Kluczowych Funkcji

### 2.4.1. Obliczanie Długości Trasy
**Lokalizacja**: `data_handlers/trail_data.py` - metoda `_validate_trail_data()`
```python
def _validate_trail_data(self, trail: Dict[str, Any]) -> bool:
    # Konwersja długości trasy na kilometry
    if 'length_km' in trail:
        try:
            trail['length_km'] = float(trail['length_km'])
        except (ValueError, TypeError):
            return False
    return True
```
- Długość trasy jest pobierana bezpośrednio z API
- Konwertowana jest na typ float
- Walidowana jest poprawność wartości

### 2.4.2. Poziom Trudności
**Lokalizacja**: `data_handlers/trail_data.py` - metoda `_validate_trail_data()`
```python
def _validate_trail_data(self, trail: Dict[str, Any]) -> bool:
    # Walidacja poziomu trudności
    if 'difficulty' in trail:
        try:
            difficulty = int(trail['difficulty'])
            if not 1 <= difficulty <= 3:
                return False
            trail['difficulty'] = difficulty
        except (ValueError, TypeError):
            return False
    return True
```
- Poziom trudności jest skalą od 1 do 3
- 1 - łatwy
- 2 - średni
- 3 - trudny
- Wartość jest konwertowana na integer i walidowana

#### 2.4.2.1. Obliczanie Poziomu Trudności
Poziom trudności trasy jest określany na podstawie następujących czynników:

1. **Długość trasy**:
   - Trasy do 5 km - poziom łatwy (1)
   - Trasy od 5 do 15 km - poziom średni (2)
   - Trasy powyżej 15 km - poziom trudny (3)

2. **Typ terenu**:
   - Teren płaski (np. "równinna") - poziom łatwy (1)
   - Teren pagórkowaty (np. "pagórkowata") - poziom średni (2)
   - Teren górski (np. "górska") - poziom trudny (3)

3. **Sumaryczna ocena**:
   - Jeśli długość i typ terenu wskazują na ten sam poziom trudności, jest to ostateczny poziom
   - Jeśli wskazują na różne poziomy, wybierany jest wyższy z nich
   - Na przykład:
     * Trasa 4 km na terenie górskim = poziom trudny (3)
     * Trasa 10 km na terenie płaskim = poziom średni (2)
     * Trasa 20 km na terenie pagórkowatym = poziom trudny (3)

4. **Dodatkowe czynniki**:
   - Wysokość nad poziomem morza
   - Nachylenie terenu
   - Dostępność ścieżki
   - Warunki pogodowe w danym sezonie

Ostateczny poziom trudności jest zapisywany w bazie danych i wykorzystywany do filtrowania tras zgodnie z preferencjami użytkownika.

### 2.4.3. Filtrowanie Tras
**Lokalizacja**: `recommendation/trail_recommender.py` - metoda `recommend_trails()`
```python
def filter_trail(trail: Dict[str, Any]) -> bool:
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
```
- Filtrowanie odbywa się na podstawie wszystkich podanych kryteriów
- Używa funkcji `filter()` z programowania funkcyjnego
- Sprawdza każdy warunek osobno

### 2.4.4. Pobieranie Danych Pogodowych
**Lokalizacja**: `api/weather_api.py` - metoda `get_weather_forecast()`
```python
def get_weather_forecast(self, city: str, date: str) -> Optional[Dict[str, Any]]:
    # Wybór odpowiedniego endpointu w zależności od daty
    if datetime.strptime(date, "%Y-%m-%d").date() < datetime.now().date():
        return self._get_historical_weather(city, date)
    else:
        return self._get_future_weather(city, date)
```
- Automatycznie wybiera odpowiedni endpoint API
- Dla dat przeszłych używa endpointu historycznego
- Dla dat przyszłych używa endpointu prognozy

### 2.4.5. Sortowanie Tras
**Lokalizacja**: `recommendation/trail_recommender.py` - metoda `recommend_trails()`
```python
sorted_trails = sorted(
    filtered_trails,
    key=lambda x: (x.get('difficulty', 0), x.get('length_km', 0))
)
```
- Sortuje trasy według poziomu trudności
- W ramach tego samego poziomu trudności sortuje według długości
- Używa funkcji `sorted()` z programowania funkcyjnego

### 2.4.6. Obliczanie Statystyk
**Lokalizacja**: `recommendation/trail_recommender.py` - metoda `recommend_trails()`
```python
total_length = reduce(
    lambda acc, trail: acc + trail.get('length_km', 0),
    sorted_trails,
    0
)
avg_length = total_length / len(sorted_trails)
```
- Oblicza sumę długości wszystkich tras
- Oblicza średnią długość trasy
- Używa funkcji `reduce()` z programowania funkcyjnego

### 2.4.7. Pobieranie Tras dla Miasta
**Lokalizacja**: `data_handlers/trail_data.py` - metoda `get_trails_for_city()`
```python
def get_trails_for_city(self, city: str) -> List[Dict[str, Any]]:
    # Pobieranie tras dla danego miasta
    trails = self._fetch_trails_from_api(city)
    # Walidacja i filtrowanie tras
    valid_trails = [trail for trail in trails if self._validate_trail_data(trail)]
    return valid_trails
```
- Pobiera trasy z API dla konkretnego miasta
- Filtruje i waliduje dane
- Zwraca listę poprawnych tras

### 2.4.8. Walidacja Danych Pogodowych
**Lokalizacja**: `data_handlers/weather_data.py` - metoda `_validate_weather_data()`
```python
def _validate_weather_data(self, weather_data: Dict[str, Any]) -> bool:
    required_fields = ['temperature', 'precipitation', 'cloud_cover']
    return all(field in weather_data for field in required_fields)
```
- Sprawdza obecność wymaganych pól w danych pogodowych
- Waliduje format danych
- Zapewnia poprawność danych przed ich użyciem

### 2.4.9. Zapisywanie Rekomendacji
**Lokalizacja**: `recommendation/trail_recommender.py` - metoda `_save_recommendations_to_file()`
```python
def _save_recommendations_to_file(self, city: str, date: str, trails: List[Dict[str, Any]], weather: Optional[Dict[str, Any]] = None):
    with open("result.txt", "a", encoding="utf-8") as f:
        f.write(f"\n=== Rekomendacje dla {city} na dzień {date} ===\n")
        # Zapis danych pogodowych
        if weather:
            f.write("Dane pogodowe:\n")
            f.write(f"Temperatura: {weather.get('temperature_min')}°C - {weather.get('temperature_max')}°C\n")
        # Zapis tras
        for trail in trails:
            f.write(f"\n{trail['name']}\n")
            f.write(f"Długość: {trail.get('length_km')} km\n")
```
- Zapisuje rekomendacje do pliku tekstowego
- Formatuje dane w czytelny sposób
- Obsługuje kodowanie UTF-8 dla polskich znaków

### 2.4.10. Pobieranie Współrzędnych Miasta
**Lokalizacja**: `api/weather_api.py` - metoda `_get_city_coordinates()`
```python
def _get_city_coordinates(self, city: str) -> Optional[Tuple[float, float]]:
    if city in CITY_COORDINATES:
        return CITY_COORDINATES[city]
    return None
```
- Zwraca współrzędne geograficzne dla danego miasta
- Używa predefiniowanej mapy miast
- Obsługuje brakujące dane

### 2.4.11. Konwersja Jednostek Pogodowych
**Lokalizacja**: `api/weather_api.py` - metoda `_convert_weather_units()`
```python
def _convert_weather_units(self, data: Dict[str, Any]) -> Dict[str, Any]:
    # Konwersja sekund na godziny dla czasu nasłonecznienia
    if 'sunshine_duration' in data:
        data['sunshine_hours'] = data['sunshine_duration'] / 3600
    # Konwersja m/s na km/h dla prędkości wiatru
    if 'wind_speed' in data:
        data['wind_speed'] = data['wind_speed'] * 3.6
    return data
```
- Konwertuje jednostki z systemu metrycznego
- Przetwarza dane pogodowe na bardziej czytelne formaty
- Obsługuje różne typy danych pogodowych

### 2.4.12. Filtrowanie Według Warunków Pogodowych
**Lokalizacja**: `recommendation/trail_recommender.py` - metoda `_filter_by_weather()`
```python
def _filter_by_weather(self, trails: List[Dict[str, Any]], weather: Dict[str, Any]) -> List[Dict[str, Any]]:
    return list(filter(
        lambda trail: self._check_weather_conditions(trail, weather),
        trails
    ))
```
- Filtruje trasy na podstawie warunków pogodowych
- Używa funkcji `filter()` z programowania funkcyjnego
- Sprawdza kompatybilność tras z aktualną pogodą

### 2.4.13. Zapisywanie Danych do Plików JSON
**Lokalizacja**: `data_handlers/trail_data.py` - metoda `_save_trails_to_file()`
```python
def _save_trails_to_file(self, trails: List[Dict[str, Any]]) -> None:
    try:
        with open('api/trails_data.json', 'w', encoding='utf-8') as f:
            json.dump(trails, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Błąd podczas zapisywania tras do pliku: {e}")
```
- Zapisuje dane o trasach do pliku `trails_data.json`
- Używa kodowania UTF-8 dla polskich znaków
- Formatuje dane z wcięciami dla lepszej czytelności

**Lokalizacja**: `data_handlers/weather_data.py` - metoda `_save_weather_to_file()`
```python
def _save_weather_to_file(self, weather_data: Dict[str, Any], city: str, date: str) -> None:
    try:
        with open('api/weather_dataa.json', 'w', encoding='utf-8') as f:
            json.dump({
                'city': city,
                'date': date,
                'weather': weather_data
            }, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Błąd podczas zapisywania danych pogodowych do pliku: {e}")
```
- Zapisuje dane pogodowe do pliku `weather_dataa.json`
- Dodaje informacje o mieście i dacie
- Obsługuje błędy podczas zapisu

### 2.4.14. Wczytywanie Danych z Plików JSON
**Lokalizacja**: `data_handlers/trail_data.py` - metoda `_load_trails_from_file()`
```python
def _load_trails_from_file(self) -> List[Dict[str, Any]]:
    try:
        with open('api/trails_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Błąd podczas odczytu pliku JSON z trasami")
        return []
```
- Wczytuje dane o trasach z pliku `trails_data.json`
- Obsługuje brak pliku i błędy dekodowania JSON
- Zwraca pustą listę w przypadku błędów

**Lokalizacja**: `data_handlers/weather_data.py` - metoda `_load_weather_from_file()`
```python
def _load_weather_from_file(self, city: str, date: str) -> Optional[Dict[str, Any]]:
    try:
        with open('api/weather_dataa.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            if data['city'] == city and data['date'] == date:
                return data['weather']
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return None
```
- Wczytuje dane pogodowe z pliku `weather_dataa.json`
- Sprawdza zgodność miasta i daty
- Zwraca dane pogodowe tylko jeśli pasują do zapytania

## 3. Przepływ Danych

1. **Inicjalizacja**
- Tworzenie instancji `TrailRecommender`
- Inicjalizacja `TrailDataHandler` i `WeatherAPI`

2. **Pobieranie Danych**
- Pobranie listy szlaków dla danego miasta
- Pobranie danych pogodowych dla wybranej daty

3. **Filtrowanie i Sortowanie**
- Filtrowanie szlaków według kryteriów użytkownika
- Sortowanie wyników
- Obliczanie statystyk (np. średnia długość)

4. **Zapisywanie Wyników**
- Zapis rekomendacji do pliku `result.txt`
- Formatowanie danych do czytelnego wyświetlenia

## 4. Obsługa Błędów

1. **Błędy API**
- Obsługa błędów połączenia
- Obsługa błędów parsowania JSON
- Obsługa brakujących danych

2. **Błędy Walidacji**
- Sprawdzanie poprawności danych wejściowych
- Obsługa nieprawidłowych formatów dat
- Obsługa nieprawidłowych wartości kryteriów

3. **Błędy Zapisów**
- Obsługa błędów podczas zapisywania do pliku
- Obsługa problemów z kodowaniem znaków

## 5. Przykład Użycia

```python
recommender = TrailRecommender()
trails = recommender.recommend_trails(
    city="Kraków",
    date="2024-03-20",
    difficulty=2,
    terrain_type="górska",
    min_length=5.0,
    max_length=15.0,
    min_sunshine=4.0,
    max_precipitation=5.0,
    min_temperature=10.0,
    max_temperature=25.0
)
```

## 6. Wymagania Systemowe

- Python 3.8+
- Biblioteki:
  - requests (do komunikacji z API)
  - datetime (do obsługi dat)
  - typing (do typowania)
  - functools (do funkcji reduce)

## 7. Instalacja i Konfiguracja Środowiska

### 7.1. Wymagane Narzędzia
- Python 3.8 lub nowszy
- pip (menedżer pakietów Pythona)
- Git (opcjonalnie, do klonowania repozytorium)

### 7.2. Instalacja Środowiska Wirtualnego
1. Utworzenie środowiska wirtualnego:
```bash
python -m venv venv
```

2. Aktywacja środowiska wirtualnego:
- Windows:
```bash
.\venv\Scripts\activate
```
- Linux/MacOS:
```bash
source venv/bin/activate
```

### 7.3. Instalacja Wymaganych Pakietów
```bash
pip install requests
```

### 7.4. Struktura Projektu
Po instalacji, struktura projektu powinna wyglądać następująco:
```
projekt/
├── api/
│   ├── weather_api.py
│   ├── trails_data.json
│   └── weather_dataa.json
├── data_handlers/
│   ├── trail_data.py
│   └── weather_data.py
├── recommendation/
│   └── trail_recommender.py
├── main.py
└── DOCUMENTATION.md
```

### 7.5. Uruchomienie Aplikacji
1. Upewnij się, że jesteś w głównym katalogu projektu
2. Uruchom aplikację komendą:
```bash
python main.py
```

### 7.6. Rozwiązywanie Problemów
1. **Błąd: Brak modułu requests**
```bash
pip install requests
```

2. **Błąd: Nieprawidłowa wersja Pythona**
- Sprawdź wersję Pythona:
```bash
python --version
```
- Jeśli wersja jest niższa niż 3.8, zainstaluj nowszą wersję

3. **Błąd: Brak plików JSON**
- Upewnij się, że pliki `trails_data.json` i `weather_dataa.json` znajdują się w katalogu `api/`
- Jeśli pliki nie istnieją, system automatycznie pobierze dane z API przy pierwszym uruchomieniu

### 7.7. Testowanie Instalacji
Aby sprawdzić, czy wszystko działa poprawnie, uruchom testowe zapytanie:
```python
from recommendation.trail_recommender import TrailRecommender

recommender = TrailRecommender()
trails = recommender.recommend_trails(
    city="Kraków",
    date="2024-03-20"
)
print(f"Znaleziono {len(trails)} tras")
```

## 8. Rozwój i Rozszerzenia

1. **Możliwe Rozszerzenia**
- Dodanie nowych kryteriów wyszukiwania
- Implementacja systemu ocen szlaków
- Dodanie map i zdjęć szlaków
- Integracja z systemami rezerwacji

2. **Optymalizacje**
- Buforowanie danych pogodowych
- Asynchroniczne pobieranie danych
- Optymalizacja zapytań do API

## 9. Podsumowanie

System wykorzystuje elementy programowania funkcyjnego do efektywnego przetwarzania i filtrowania danych. Główne funkcje (`filter`, `sorted`, `reduce`) w połączeniu z wyrażeniami lambda pozwalają na zwięzły i czytelny kod, który jednocześnie jest wydajny i łatwy w utrzymaniu. System jest rozszerzalny i może być łatwo modyfikowany w celu dodania nowych funkcjonalności. 

## 10. Przewodnik po Strukturze Projektu

### 10.1. Główna Struktura Katalogów
```
projekt/
├── api/                    # Katalog z API i danymi
│   ├── weather_api.py      # Implementacja API pogodowego
│   ├── trails_data.json    # Dane o trasach
│   └── weather_dataa.json  # Dane pogodowe
├── data_handlers/          # Obsługa danych
│   ├── trail_data.py       # Obsługa danych o trasach
│   └── weather_data.py     # Obsługa danych pogodowych
├── recommendation/         # Logika rekomendacji
│   └── trail_recommender.py # Główna klasa rekomendera
├── main.py                # Główny plik aplikacji
└── DOCUMENTATION.md       # Dokumentacja
```

### 10.2. Przewodnik po Funkcjach

#### 10.2.1. API i Dane Pogodowe (`api/weather_api.py`)
- `get_weather_forecast()` - główna metoda pobierania prognozy
- `_get_historical_weather()` - pobieranie danych historycznych
- `_get_future_weather()` - pobieranie prognozy
- `_get_city_coordinates()` - pobieranie współrzędnych miasta
- `_convert_weather_units()` - konwersja jednostek pogodowych

#### 10.2.2. Obsługa Danych o Trasach (`data_handlers/trail_data.py`)
- `get_trails_for_city()` - pobieranie tras dla miasta
- `_validate_trail_data()` - walidacja danych o trasie
- `_save_trails_to_file()` - zapisywanie tras do JSON
- `_load_trails_from_file()` - wczytywanie tras z JSON
- `_fetch_trails_from_api()` - pobieranie tras z API

#### 10.2.3. Obsługa Danych Pogodowych (`data_handlers/weather_data.py`)
- `_validate_weather_data()` - walidacja danych pogodowych
- `_save_weather_to_file()` - zapisywanie pogody do JSON
- `_load_weather_from_file()` - wczytywanie pogody z JSON

#### 10.2.4. Rekomendacja Tras (`recommendation/trail_recommender.py`)
- `recommend_trails()` - główna metoda rekomendacji
- `_filter_by_weather()` - filtrowanie według pogody
- `_save_recommendations_to_file()` - zapisywanie rekomendacji
- `_check_weather_conditions()` - sprawdzanie warunków pogodowych

### 10.3. Przewodnik po Plikach Danych

#### 10.3.1. Pliki JSON
- `api/trails_data.json` - zawiera dane o wszystkich trasach
  * Struktura: lista obiektów z danymi tras
  * Kluczowe pola: name, length_km, difficulty, terrain_type
- `api/weather_dataa.json` - zawiera dane pogodowe
  * Struktura: obiekt z danymi pogodowymi dla miasta i daty
  * Kluczowe pola: temperature, precipitation, cloud_cover

#### 10.3.2. Pliki Wyjściowe
- `result.txt` - plik z rekomendacjami
  * Format: tekstowy z sekcjami dla każdego zapytania
  * Zawiera: dane pogodowe i listę rekomendowanych tras

### 10.4. Przewodnik po Funkcjjonalnościach

#### 10.4.1. Pobieranie Danych
1. **Trasy**:
   - Lokalizacja: `data_handlers/trail_data.py`
   - Główne funkcje: `get_trails_for_city()`, `_fetch_trails_from_api()`
   - Dane zapisywane w: `api/trails_data.json`

2. **Pogoda**:
   - Lokalizacja: `api/weather_api.py`
   - Główne funkcje: `get_weather_forecast()`, `_get_historical_weather()`
   - Dane zapisywane w: `api/weather_dataa.json`

#### 10.4.2. Przetwarzanie Danych
1. **Filtrowanie**:
   - Lokalizacja: `recommendation/trail_recommender.py`
   - Główne funkcje: `recommend_trails()`, `_filter_by_weather()`
   - Używa: `filter()`, wyrażenia lambda

2. **Sortowanie**:
   - Lokalizacja: `recommendation/trail_recommender.py`
   - Główne funkcje: `recommend_trails()`
   - Używa: `sorted()`, wyrażenia lambda

3. **Obliczanie Statystyk**:
   - Lokalizacja: `recommendation/trail_recommender.py`
   - Główne funkcje: `recommend_trails()`
   - Używa: `reduce()`, wyrażenia lambda

#### 10.4.3. Zapisywanie Wyników
1. **Rekomendacje**:
   - Lokalizacja: `recommendation/trail_recommender.py`
   - Główna funkcja: `_save_recommendations_to_file()`
   - Plik wyjściowy: `result.txt`

2. **Dane Cache**:
   - Lokalizacja: odpowiednie pliki w `data_handlers/`
   - Funkcje: `_save_trails_to_file()`, `_save_weather_to_file()`
   - Pliki: `api/trails_data.json`, `api/weather_dataa.json`

### 10.5. Przykłady Użycia

#### 10.5.1. Pobieranie Tras
```python
from data_handlers.trail_data import TrailDataHandler

handler = TrailDataHandler()
trails = handler.get_trails_for_city("Kraków")
```

#### 10.5.2. Pobieranie Pogody
```python
from api.weather_api import WeatherAPI

api = WeatherAPI()
weather = api.get_weather_forecast("Kraków", "2024-03-20")
```

#### 10.5.3. Generowanie Rekomendacji
```python
from recommendation.trail_recommender import TrailRecommender

recommender = TrailRecommender()
trails = recommender.recommend_trails(
    city="Kraków",
    date="2024-03-20",
    difficulty=2
)
```

## 11. Pliki Nieużywane

