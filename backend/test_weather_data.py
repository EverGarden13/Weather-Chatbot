from weather_data import local_weather, rainfall_nowcast, uv_index, weather_warning, several_days_weather_forecast

def test_all_functions():
    # Test local_weather with Hong Kong coordinates
    print("\n=== Testing local_weather ===")
    hk_lat, hk_lng = 22.3193, 114.1694  # Hong Kong coordinates
    local_weather_result = local_weather(hk_lat, hk_lng)
    print(f"Local Weather Result: {local_weather_result}")

    # Test rainfall_nowcast
    print("\n=== Testing rainfall_nowcast ===")
    rainfall_result = rainfall_nowcast(hk_lat, hk_lng)
    print(f"Rainfall Nowcast Result: {rainfall_result}")

    # Test uv_index in both languages
    print("\n=== Testing uv_index ===")
    uv_en = uv_index('EN')
    print(f"UV Index (English): {uv_en}")
    uv_tc = uv_index('UC')
    print(f"UV Index (Traditional Chinese): {uv_tc}")

    # Test weather_warning in both languages
    print("\n=== Testing weather_warning ===")
    warning_en = weather_warning('EN')
    print(f"Weather Warning (English): {warning_en}")
    warning_tc = weather_warning('UC')
    print(f"Weather Warning (Traditional Chinese): {warning_tc}")

    # Test several_days_weather_forecast in both languages
    print("\n=== Testing several_days_weather_forecast ===")
    forecast_en = several_days_weather_forecast('EN')
    print(f"Weather Forecast (English): {forecast_en}")
    forecast_tc = several_days_weather_forecast('UC')
    print(f"Weather Forecast (Traditional Chinese): {forecast_tc}")

if __name__ == "__main__":
    test_all_functions() 