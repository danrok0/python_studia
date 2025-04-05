def filter_trails(trails_data, min_length=5, max_difficulty=3):
    """
    Filtruje trasy według minimalnej długości i maksymalnej trudności.
    """
    filtered_trails = []

    if not trails_data:
        print("Brak danych o trasach.")
        return []

    for trail in trails_data:
        
        trail_length = trail.get('length', 0)  # Używamy 'length', bo dane JSON mają 'length'
        trail_difficulty = trail.get('difficulty', 0)  # Sprawdzamy 'difficulty'

        
        if not isinstance(trail_length, (int, float)) or not isinstance(trail_difficulty, (int, float)):
            print(f"Nieprawidłowy format danych: {trail}")
            continue

        
        if trail_length >= min_length and trail_difficulty <= max_difficulty:
            filtered_trails.append(trail)
    
    return filtered_trails

def filter_weather(weather_data, min_temperature, max_temperature):
    """
    Filtrowanie danych pogodowych według temperatury.
    """
    if 'daily' not in weather_data:
        print("Brak sekcji 'daily' w danych pogodowych!")
        return []

    # Pobieramy dane pogodowe z sekcji 'daily'
    time = weather_data['daily']['time']
    temperature_min = weather_data['daily']['temperature_2m_min']
    temperature_max = weather_data['daily']['temperature_2m_max']
    precipitation = weather_data['daily']['precipitation_sum']
    sunshine = weather_data['daily']['sunshine_duration']
    
    
    filtered_weather = []
    for i in range(len(time)):
        if min_temperature <= temperature_min[i] <= max_temperature:
            filtered_weather.append({
                'date': time[i],
                'temperature_min': temperature_min[i],
                'temperature_max': temperature_max[i],
                'precipitation': precipitation[i],
                'sunshine_duration': sunshine[i]
            })

    return filtered_weather



