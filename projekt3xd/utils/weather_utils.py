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
                'min': round(weather_data.get('temperature_min', 0), 1),
                'max': round(weather_data.get('temperature_max', 0), 1),
                'średnia': round(weather_data.get('temperature', 0), 1)
            },
            'opady': round(weather_data.get('precipitation', 0), 1),
            'zachmurzenie': round(weather_data.get('cloud_cover', 0), 1),
            'godziny_słoneczne': round(weather_data.get('sunshine_hours', 0), 1),
            'prędkość_wiatru': round(weather_data.get('wind_speed', 0), 1)
        }
    
    @staticmethod
    def is_weather_suitable(weather_data: Dict[str, Any], 
                          max_precipitation: float,
                          min_temperature: float,
                          max_temperature: float) -> bool:
        """Sprawdza czy warunki pogodowe są odpowiednie dla wycieczki."""
        if not weather_data:
            return False
            
        avg_temp = weather_data.get('temperature', 0)
        precipitation = weather_data.get('precipitation', 0)
        
        return (min_temperature <= avg_temp <= max_temperature and 
                precipitation <= max_precipitation)
    
    @staticmethod
    def get_weather_summary(weather_data: Dict[str, Any]) -> str:
        """Tworzy podsumowanie warunków pogodowych."""
        if not weather_data:
            return "Brak danych pogodowych"
            
        temp_min = weather_data.get('temperature_min', 0)
        temp_max = weather_data.get('temperature_max', 0)
        precipitation = weather_data.get('precipitation', 0)
        cloud_cover = weather_data.get('cloud_cover', 0)
        sunshine = weather_data.get('sunshine_hours', 0)
        
        return (f"Temperatura: {temp_min:.1f}°C - {temp_max:.1f}°C\n"
                f"Opady: {precipitation:.1f} mm\n"
                f"Zachmurzenie: {cloud_cover:.1f}%\n"
                f"Godziny słoneczne: {sunshine:.1f} h")
    
    @staticmethod
    def get_weather_condition(weather_data: Dict[str, Any]) -> str:
        """Określa ogólny stan pogody."""
        if not weather_data:
            return "nieznany"
            
        precipitation = weather_data.get('precipitation', 0)
        cloud_cover = weather_data.get('cloud_cover', 0)
        sunshine = weather_data.get('sunshine_hours', 0)
        
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
        Oblicza indeks komfortu dla wędrówek (0-100) na podstawie warunków pogodowych.
        
        Parametry brane pod uwagę:
        - Temperatura (optymalna: 15-20°C)
        - Opady (brak opadów najlepszy)
        - Zachmurzenie (lekkie do umiarkowanego optymalne)
        """
        if not weather_data:
            return 50.0  # Wartość domyślna przy braku danych
            
        # Oblicz średnią temperaturę z min i max jeśli dostępne
        temp_min = weather_data.get('temperature_min')
        temp_max = weather_data.get('temperature_max')
        
        if temp_min is not None and temp_max is not None:
            temp = (temp_min + temp_max) / 2
        else:
            temp = weather_data.get('temperature', 20)
            
        # Temperatura (waga: 40%)
        # Zmniejszony optymalny zakres i bardziej surowe kary
        if 15 <= temp <= 18:  # Zmniejszony górny próg z 20°C do 18°C
            temp_score = 100
        elif temp < 15:
            temp_score = max(0, 100 - abs(15 - temp) * 15)  # Zwiększona kara z 12 do 15 punktów za każdy stopień poniżej 15°C
        else:
            temp_score = max(0, 100 - abs(temp - 18) * 18)  # Zwiększona kara z 15 do 18 punktów za każdy stopień powyżej 18°C
            
        # Opady (waga: 35%)
        # Bardziej surowe kary za opady
        precip = weather_data.get('precipitation', 0)
        precip_score = max(0, 100 - (precip * 40))  # Zwiększona kara z 30 do 40 punktów za każdy mm opadów
            
        # Zachmurzenie (waga: 25%)
        # Bardziej surowa ocena zachmurzenia
        cloud = weather_data.get('cloud_cover', 50)
        if cloud < 20:
            cloud_score = 80  # Prawie bezchmurnie (nie idealne - może być za gorąco)
        elif 20 <= cloud <= 40:
            cloud_score = 100  # Lekkie zachmurzenie - idealne
        elif cloud < 60:
            cloud_score = 60  # Umiarkowane zachmurzenie
        else:
            cloud_score = max(0, 100 - ((cloud - 60) * 2))  # Liniowy spadek punktów dla dużego zachmurzenia
            
        # Oblicz końcowy wynik (ważona średnia)
        comfort_index = (
            temp_score * 0.4 +  # Temperatura ma największy wpływ
            precip_score * 0.35 +  # Opady mają duży wpływ
            cloud_score * 0.25  # Zachmurzenie ma najmniejszy wpływ
        )
            
        return round(comfort_index, 1)