import requests

def fetch_trails_from_api(region="Tatry"):
    api_url = f"http://overpass-api.de/api/interpreter?data=[out:json][timeout:25];area[name=\"{region}\"][boundary=administrative]->.searchArea;relation[type=\"route\"][route=\"hiking\"](area.searchArea);out body;>;out skel qt;"
    
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()  
        else:
            print(f"Nie udało się pobrać danych z Overpass API: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error podczas pobierania danych z Overpass API: {e}")
        return []

def fetch_weather_from_api(lat, lon, start_date, end_date):
    api_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}&daily=temperature_2m_min,temperature_2m_max,temperature_2m_mean,precipitation_sum,sunshine_duration&timezone=Europe%2FWarsaw"
    
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()  
        else:
            print(f"Nie udało się pobrać danych pogodowych z API: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error podczas pobierania danych pogodowych z API: {e}")
        return []

