from typing import Dict, Any, Optional
from datetime import datetime

def format_weather_data(weather_data: Dict[str, Any]) -> Dict[str, Any]:
    """Formatuje dane pogodowe do bardziej czytelnej postaci."""
    formatted_data = {
        'temperatura': {
            'min': round(weather_data.get('temperature_2m_min', 0), 1),
            'max': round(weather_data.get('temperature_2m_max', 0), 1),
            'średnia': round(weather_data.get('temperature_2m_mean', 0), 1)
        },
        'opady': round(weather_data.get('precipitation_sum', 0), 1),
        'zachmurzenie': round(weather_data.get('cloud_cover_mean', 0), 1),
        'godziny_słoneczne': round(weather_data.get('sunshine_duration', 0) / 3600, 1),  # Konwersja sekund na godziny
        'prędkość_wiatru': round(weather_data.get('wind_speed_10m_max', 0), 1)
    }
    return formatted_data

def is_weather_suitable(weather_data: Dict[str, Any], 
                       max_precipitation: float,
                       min_temperature: float,
                       max_temperature: float) -> bool:
    """Sprawdza czy warunki pogodowe są odpowiednie dla wycieczki."""
    if not weather_data:
        return False
        
    avg_temp = weather_data.get('temperature_2m_mean', 0)
    precipitation = weather_data.get('precipitation_sum', 0)
    
    return (min_temperature <= avg_temp <= max_temperature and 
            precipitation <= max_precipitation)

def get_weather_summary(weather_data: Dict[str, Any]) -> str:
    """Tworzy podsumowanie warunków pogodowych."""
    if not weather_data:
        return "Brak danych pogodowych"
        
    temp_min = weather_data.get('temperature_2m_min', 0)
    temp_max = weather_data.get('temperature_2m_max', 0)
    precipitation = weather_data.get('precipitation_sum', 0)
    cloud_cover = weather_data.get('cloud_cover_mean', 0)
    sunshine = weather_data.get('sunshine_duration', 0) / 3600  # Konwersja sekund na godziny
    
    return (f"Temperatura: {temp_min:.1f}°C - {temp_max:.1f}°C\n"
            f"Opady: {precipitation:.1f} mm\n"
            f"Zachmurzenie: {cloud_cover:.1f}%\n"
            f"Godziny słoneczne: {sunshine:.1f} h") 