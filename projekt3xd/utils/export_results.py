import json
import csv
from typing import List, Dict, Any, Optional
from datetime import datetime

class ResultExporter:
    @staticmethod
    def export_results(city: str, date: str, trails: List[Dict[str, Any]], 
                      weather: Optional[Dict[str, Any]] = None):
        """
        Eksportuje wyniki rekomendacji do różnych formatów plików.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Zapisz do TXT
        ResultExporter._save_to_txt(city, date, trails, weather, timestamp)
        
        # Zapisz do JSON
        ResultExporter._save_to_json(city, date, trails, weather, timestamp)
        
        # Zapisz do CSV
        ResultExporter._save_to_csv(city, date, trails, weather, timestamp)
        
    @staticmethod
    def _save_to_txt(city: str, date: str, trails: List[Dict[str, Any]], 
                     weather: Dict[str, Any], timestamp: str):
        """Zapisuje rekomendacje do pliku result.txt."""
        try:
            with open("result.txt", "a", encoding="utf-8") as f:
                f.write(f"\n=== Rekomendacje dla {city} na dzień {date} ===\n")
                f.write(f"Data wygenerowania: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                if weather:
                    f.write("Dane pogodowe:\n")
                    f.write(f"Temperatura średnia: {weather.get('temperature', 'N/A')}°C\n")
                    f.write(f"Minimalna temperatura: {weather.get('temperature_min', 'N/A')}°C\n")
                    f.write(f"Maksymalna temperatura: {weather.get('temperature_max', 'N/A')}°C\n")
                    f.write(f"Opady: {weather.get('precipitation', 'N/A')} mm\n")
                    f.write(f"Zachmurzenie: {weather.get('cloud_cover', 'N/A')}%\n")
                    f.write(f"Godziny słoneczne: {weather.get('sunshine_hours', 'N/A')} h\n")
                    f.write(f"Prędkość wiatru: {weather.get('wind_speed', 'N/A')} km/h\n\n")

                f.write(f"Znaleziono {len(trails)} tras:\n\n")
                for i, trail in enumerate(trails, 1):
                    f.write(f"{i}. {trail['name']}\n")
                    f.write(f"   Miasto: {trail.get('region', 'brak danych')}\n")
                    f.write(f"   Długość: {trail.get('length_km', 'N/A')} km\n")
                    f.write(f"   Poziom trudności: {trail.get('difficulty', 'N/A')}/3\n")
                    f.write(f"   Typ terenu: {trail.get('terrain_type', 'N/A')}\n")
                    f.write(f"   Kategoria: {trail.get('category', 'nieskategoryzowana').upper()}\n")
                    if 'comfort_index' in trail:
                        f.write(f"   Indeks komfortu: {trail['comfort_index']}/100\n")
                    if 'weighted_score' in trail:
                        f.write(f"   Wynik ważony: {trail['weighted_score']}/100\n")
                    if 'estimated_time' in trail:
                        hours = int(trail['estimated_time'])
                        minutes = int((trail['estimated_time'] - hours) * 60)
                        if hours > 0 and minutes > 0:
                            f.write(f"   Szacowany czas przejścia: {hours}h {minutes}min\n")
                        elif hours > 0:
                            f.write(f"   Szacowany czas przejścia: {hours}h\n")
                        else:
                            f.write(f"   Szacowany czas przejścia: {minutes}min\n")
                    f.write("\n")
                f.write("=" * 50 + "\n")
            
            print("\nRekomendacje zostały zapisane do pliku result.txt")
            
        except Exception as e:
            print(f"Błąd podczas zapisywania do pliku TXT: {e}")
            
    @staticmethod
    def _save_to_json(city: str, date: str, trails: List[Dict[str, Any]], 
                      weather: Dict[str, Any], timestamp: str):
        """Zapisuje rekomendacje do pliku JSON."""
        try:
            data = {
                "metadata": {
                    "city": city,
                    "date": date,
                    "generated_at": datetime.now().isoformat()
                },
                "weather": weather,
                "trails": trails
            }
            
            filename = f"recommendations_{timestamp}.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                
            print(f"Rekomendacje zostały zapisane do pliku {filename}")
            
        except Exception as e:
            print(f"Błąd podczas zapisywania do pliku JSON: {e}")
            
    @staticmethod
    def _save_to_csv(city: str, date: str, trails: List[Dict[str, Any]], 
                     weather: Dict[str, Any], timestamp: str):
        """Zapisuje rekomendacje do pliku CSV."""
        try:
            filename = f"recommendations_{timestamp}.csv"
            with open(filename, "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                
                # Zapisz nagłówki
                headers = ["Nazwa", "Miasto", "Długość (km)", "Trudność", "Typ terenu", 
                          "Kategoria", "Indeks komfortu", "Wynik ważony", "Szacowany czas (h)"]
                writer.writerow(headers)
                
                # Zapisz dane tras
                for trail in trails:
                    row = [
                        trail.get('name', ''),
                        trail.get('region', ''),
                        trail.get('length_km', ''),
                        f"{trail.get('difficulty', '')}/3",
                        trail.get('terrain_type', ''),
                        trail.get('category', '').upper(),
                        f"{trail.get('comfort_index', '')}/100" if 'comfort_index' in trail else '',
                        f"{trail.get('weighted_score', '')}/100" if 'weighted_score' in trail else '',
                        f"{trail.get('estimated_time', '')}"
                    ]
                    writer.writerow(row)
                    
            print(f"Rekomendacje zostały zapisane do pliku {filename}")
            
        except Exception as e:
            print(f"Błąd podczas zapisywania do pliku CSV: {e}")
