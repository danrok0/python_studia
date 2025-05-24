from typing import Dict, Any, Optional
from datetime import datetime

class WeatherUtils:
    """Klasa narzędzi do przetwarzania danych pogodowych."""

    @staticmethod
    def format_weather_data(weather_data: Dict[str, Any]) -> Dict[str, Any]:
        """Formatuje dane pogodowe do bardziej czytelnej postaci."""
        if not weather_data:
            return {}
            
        return {
            'temperatura': {
                'min': round(weather_data.get('temperature_2m_min', 0), 1),
                'max': round(weather_data.get('temperature_2m_max', 0), 1),
                'średnia': round(weather_data.get('temperature_2m_mean', 0), 1)
            },
            'opady': round(weather_data.get('precipitation_sum', 0), 1),
            'zachmurzenie': round(weather_data.get('cloud_cover_mean', 0), 1),
            'godziny_słoneczne': round(weather_data.get('sunshine_duration', 0) / 3600, 1),
            'prędkość_wiatru': round(weather_data.get('wind_speed_10m_max', 0), 1)
        }
    
    @staticmethod
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
    
    @staticmethod
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
    
    @staticmethod
    def get_weather_condition(weather_data: Dict[str, Any]) -> str:
        """Określa ogólny stan pogody."""
        if not weather_data:
            return "nieznany"
            
        precipitation = weather_data.get('precipitation_sum', 0)
        cloud_cover = weather_data.get('cloud_cover_mean', 0)
        sunshine = weather_data.get('sunshine_duration', 0) / 3600
        
        if precipitation > 5:
            return "deszczowo"
        elif cloud_cover > 70:
            return "pochmurno"
        elif sunshine > 6:
            return "słonecznie"
        else:
            return "umiarkowanie"
    
    @staticmethod
    def calculate_hiking_comfort(weather_data: Dict[str, Any]) -> float:
        """
        Oblicza indeks komfortu wędrówki w skali 0-100.
        
        Czynniki wpływające na komfort:
        - Temperatura (35%): idealna między 18-22°C
        - Opady (25%): im mniejsze tym lepiej
        - Zachmurzenie (20%): umiarkowane zachmurzenie jest korzystne
        - Wiatr (10%): umiarkowany wiatr jest korzystny
        - Godziny słoneczne (10%): optymalne 4-8 godzin
        """
        if not weather_data:
            return 0.0

        # Temperatura (waga: 35%)
        temp = weather_data.get('temperature_2m_mean', 0)
        temp_comfort = 100
        if temp < 18:
            temp_comfort = max(0, 100 - (18 - temp) * 8)  # Zimniej niż ideał
        elif temp > 22:
            temp_comfort = max(0, 100 - (temp - 22) * 10)  # Cieplej niż ideał

        # Opady (waga: 25%)
        precipitation = weather_data.get('precipitation_sum', 0)
        precip_comfort = max(0, 100 - precipitation * 25)  # 4mm = 0 komfortu

        # Zachmurzenie (waga: 20%)
        cloud_cover = weather_data.get('cloud_cover_mean', 50)
        cloud_comfort = 100
        if cloud_cover < 20:  # Za słonecznie
            cloud_comfort = max(0, 100 - (20 - cloud_cover) * 3)
        elif cloud_cover > 60:  # Za pochmurno
            cloud_comfort = max(0, 100 - (cloud_cover - 60) * 2.5)

        # Wiatr (waga: 10%)
        wind_speed = weather_data.get('wind_speed_10m_max', 0)
        wind_comfort = 100
        if wind_speed < 5:  # Za mało wiatru
            wind_comfort = max(0, 100 - (5 - wind_speed) * 12)
        elif wind_speed > 15:  # Za wietrznie
            wind_comfort = max(0, 100 - (wind_speed - 15) * 8)

        # Godziny słoneczne (waga: 10%)
        sunshine_hours = weather_data.get('sunshine_hours', 0)
        sunshine_comfort = 100
        if sunshine_hours < 4:
            sunshine_comfort = max(0, sunshine_hours * 25)
        elif sunshine_hours > 8:
            sunshine_comfort = max(0, 100 - (sunshine_hours - 8) * 15)

        # Obliczenie końcowego indeksu komfortu
        comfort_index = (
            temp_comfort * 0.35 +      # 35% waga temperatury
            precip_comfort * 0.25 +    # 25% waga opadów
            cloud_comfort * 0.20 +     # 20% waga zachmurzenia
            wind_comfort * 0.10 +      # 10% waga wiatru
            sunshine_comfort * 0.10     # 10% waga godzin słonecznych
        )

        return round(comfort_index, 1)