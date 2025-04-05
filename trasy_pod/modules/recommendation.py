def generate_recommendations(trails_data, weather_data, user_preferences):
    recommendations = []

    daily_weather = weather_data.get('daily', {})

    
    if not daily_weather:
        print("Brak danych pogodowych w 'daily'.")
        return recommendations

    
    for trail in trails_data:
        trail_region = trail['region']

        
        for i, date in enumerate(daily_weather.get('time', [])):
            # Jeśli 'region' jest dostępny w danych pogodowych, filtrujemy po regionie
            if 'region' in daily_weather and daily_weather['region'] == trail_region:
                
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


