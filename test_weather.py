"""Test script for weather_data.py module"""

from hko.weather_data import (
    local_weather, rainfall_nowcast, uv_index, 
    weather_warning, several_days_weather_forecast
)

def test_local_weather():
    print("\n=== Testing Local Weather ===")
    # Test with Hong Kong coordinates
    result = local_weather(22.3, 114.2)
    print(f"Status: {result['status']}")
    if result['status'] == 1:
        print(f"Place: {result['place']}")
        print(f"Weather Data: {result['result']}")
    else:
        print("Failed to get local weather data")

def test_rainfall_nowcast():
    print("\n=== Testing Rainfall Nowcast ===")
    # Test with Hong Kong coordinates
    result = rainfall_nowcast(22.3, 114.2)
    print(f"Status: {result['status']}")
    if result['status'] == 1:
        print("Rainfall Forecast:")
        for period, data in result['result'].items():
            if period not in ['description_en', 'description_tc', 'description_sc']:
                print(f"{period} minutes: {data['value']} mm")
        print(f"Description (EN): {result['result']['description_en']}")
    else:
        print("Failed to get rainfall forecast")

def test_uv_index():
    print("\n=== Testing UV Index ===")
    # Test in both languages
    for lang in ['UC', 'EN']:
        print(f"\nLanguage: {lang}")
        result = uv_index(lang)
        print(f"Status: {result['status']}")
        if result['status'] == 1:
            print(f"Date: {result['result']['date']}")
            print(f"Max UV Index: {result['result']['max_uv_index']}")
            print(f"Intensity: {result['result']['intensity']}")
        else:
            print("Failed to get UV index data")

def test_weather_warning():
    print("\n=== Testing Weather Warnings ===")
    # Test in both languages
    for lang in ['UC', 'EN']:
        print(f"\nLanguage: {lang}")
        result = weather_warning(lang)
        print(f"Status: {result['status']}")
        if result['status'] == 1:
            print("Warnings:")
            for warning in result['result'].get('warning', []):
                print(f"- {warning}")
        else:
            print("Failed to get weather warnings")

def test_several_days_forecast():
    print("\n=== Testing Several Days Weather Forecast ===")
    # Test in both languages
    for lang in ['UC', 'EN']:
        print(f"\nLanguage: {lang}")
        result = several_days_weather_forecast(lang)
        print(f"Status: {result['status']}")
        if result['status'] == 1:
            forecast_data = result['result']
            print("Forecast Data:")
            print(f"General Situation: {forecast_data.get('generalSituation', 'N/A')}")
            forecasts = forecast_data.get('weatherForecast', [])
            for day in forecasts:
                print(f"\nDate: {day.get('forecastDate', 'N/A')}")
                print(f"Week: {day.get('week', 'N/A')}")
                print(f"Temperature: {day.get('forecastMintemp', 'N/A')}°C - {day.get('forecastMaxtemp', 'N/A')}°C")
                print(f"Humidity: {day.get('forecastMinrh', 'N/A')}% - {day.get('forecastMaxrh', 'N/A')}%")
                print(f"Weather: {day.get('forecastWeather', 'N/A')}")
        else:
            print("Failed to get several days forecast data")

if __name__ == "__main__":
    print("Starting weather data tests...")
    test_local_weather()
    test_rainfall_nowcast()
    test_uv_index()
    test_weather_warning()
    test_several_days_forecast()
    print("\nAll tests completed!") 