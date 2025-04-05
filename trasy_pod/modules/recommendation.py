def generate_recommendations(trails_data, weather_data, user_preferences):
    recommendations = []

    # Zakładając, że weather_data jest słownikiem z kluczem 'daily'
    daily_weather = weather_data.get('daily', {})

    # Sprawdzamy, czy istnieją dane dla 'time', 'temperature_2m_min', itd.
    if not daily_weather:
        print("Brak danych pogodowych w 'daily'.")
        return recommendations

    # Przechodzimy po trasach
    for trail in trails_data:
        trail_region = trail['region']

        # Zakładając, że 'time' to lista dat, iterujemy po niej
        for i, date in enumerate(daily_weather.get('time', [])):
            # Jeśli 'region' jest dostępny w danych pogodowych, filtrujemy po regionie
            if 'region' in daily_weather and daily_weather['region'] == trail_region:
                # Sprawdzamy, czy dane pogodowe pasują do preferencji użytkownika
                if (user_preferences['temperature'][0] <= daily_weather['temperature_2m_min'][i] <= user_preferences['temperature'][1] and
                    user_preferences['sunshine_hours'][0] <= daily_weather['sunshine_duration'][i] <= user_preferences['sunshine_hours'][1] and
                    user_preferences['precipitation'][0] <= daily_weather['precipitation_sum'][i] <= user_preferences['precipitation'][1]):
                    recommendations.append({
                        'trail_name': trail['name'],
                        'region': trail['region'],
                        'date': date,
                        'temperature_min': daily_weather['temperature_2m_min'][i],
                        'temperature_max': daily_weather['temperature_2m_max'][i],
                        'precipitation': daily_weather['precipitation_sum'][i],
                        'sunshine_duration': daily_weather['sunshine_duration'][i]
                    })
                    break  # Po znalezieniu pierwszej pasującej trasy przerywamy pętlę

    return recommendations


