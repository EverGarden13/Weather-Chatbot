from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from dotenv import load_dotenv
from weather_data import local_weather, rainfall_nowcast, uv_index, weather_warning, several_days_weather_forecast

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Helper functions
def is_weather_query(text):
    """Check if the text contains weather-related keywords"""
    weather_keywords = ['weather', 'temperature', 'rain', 'humidity', 'uv', 'forecast']
    return any(keyword in text.lower() for keyword in weather_keywords)

def extract_district(text):
    """Extract Hong Kong district from text"""
    hk_districts = ['central', 'wan chai', 'causeway bay', 'tai po', 'shatin', 'tuen mun', 'yuen long']
    for district in hk_districts:
        if district in text.lower():
            return district
    return None

def get_time_period(text):
    """Extract time period from text"""
    if 'tomorrow' in text.lower():
        return 'tomorrow'
    elif 'today' in text.lower():
        return 'today'
    return 'current'

def get_weather_type(text):
    """Extract weather type from text"""
    if 'temperature' in text.lower():
        return 'temperature'
    elif 'rain' in text.lower():
        return 'rainfall'
    elif 'humidity' in text.lower():
        return 'humidity'
    elif 'uv' in text.lower():
        return 'uv'
    elif 'warning' in text.lower():
        return 'warning'
    return None

def format_weather_response(district, time_period, weather_type, data):
    """Format weather data into a dialogue-friendly response"""
    if weather_type == 'temperature':
        temp = data['result']['temperature']
        return f"In {district.capitalize()}, the {time_period} temperature is {temp}°C."
    elif weather_type == 'rainfall':
        rainfall = data['result']['0-30']['value']
        return f"In {district.capitalize()}, the {time_period} rainfall is {rainfall}mm."
    elif weather_type == 'uv':
        uv = data['result']['max_uv_index']
        intensity = data['result']['intensity']
        return f"In {district.capitalize()}, the {time_period} UV index is {uv}, which is {intensity}."
    elif weather_type == 'warning':
        warnings = data['result']
        if warnings:
            return f"In {district.capitalize()}, there are active weather warnings: {warnings}"
        return f"In {district.capitalize()}, there are no active weather warnings."
    else:
        # Format the forecast data into a readable dialogue
        forecast = data['result']
        response = f"Here's the 3-day weather forecast for {district.capitalize()}:\n\n"
        
        # Add forecast details
        for day in forecast['forecast_detail'][:3]:  # Show next 3 days
            date = day['forecast_date']
            day_of_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][day['forecast_day_of_week']]
            
            # Translate weather descriptions
            weather_desc = day['wx_desc']
            if '大致多雲，局部地區有驟雨。日間短暫時間有陽光。' in weather_desc:
                weather_desc = 'Mostly cloudy with local showers. Sunny intervals during the day.'
            elif '部分時間有陽光。' in weather_desc:
                weather_desc = 'Partly sunny.'
            elif '短暫時間有陽光，局部地區有驟雨。日間相當溫暖。' in weather_desc:
                weather_desc = 'Sunny intervals with local showers. Quite warm during the day.'
            
            # Translate wind information
            wind = day['wind_info']
            if '東至東北風3至4級。' in wind:
                wind = 'East to northeast wind force 3 to 4'
            elif '東風4級。' in wind:
                wind = 'East wind force 4'
            elif '東風2至3級。' in wind:
                wind = 'East wind force 2 to 3'
            
            response += f"{day_of_week} ({date[4:6]}/{date[6:8]}):\n"
            response += f"• {weather_desc}\n"
            response += f"• Temperature: {day['min_temp']}°C to {day['max_temp']}°C\n"
            response += f"• Humidity: {day['min_rh']}% to {day['max_rh']}%\n"
            response += f"• Wind: {wind}\n\n"
        
        return response

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message', '').lower()
    
    # Initialize response
    response = {
        'message': '',
        'status': 'success',
        'needs_district': False
    }
    
    # Check if it's a greeting
    if any(greeting in user_input for greeting in ['hi', 'hello', 'hey']):
        response['message'] = 'Hello! How can I help you with the weather today?'
        return jsonify(response)
    
    # Check if it's a goodbye
    if any(goodbye in user_input for goodbye in ['bye', 'goodbye', 'see you']):
        response['message'] = 'Goodbye! Have a great day!'
        return jsonify(response)
    
    # Check if it's a weather query
    if is_weather_query(user_input):
        district = extract_district(user_input)
        if not district:
            response['message'] = 'Which district in Hong Kong would you like to know the weather for?'
            response['needs_district'] = True
            return jsonify(response)
        
        time_period = get_time_period(user_input)
        weather_type = get_weather_type(user_input)
        
        # Get weather data based on the query
        if weather_type == 'temperature':
            # Get temperature data
            weather_data = local_weather(22.3, 114.2)  # Example coordinates for Hong Kong
            response['message'] = format_weather_response(district, time_period, weather_type, weather_data)
        elif weather_type == 'rainfall':
            # Get rainfall data
            rainfall_data = rainfall_nowcast(22.3, 114.2)
            response['message'] = format_weather_response(district, time_period, weather_type, rainfall_data)
        elif weather_type == 'uv':
            # Get UV index
            uv_data = uv_index()
            response['message'] = format_weather_response(district, time_period, weather_type, uv_data)
        elif weather_type == 'warning':
            # Get weather warnings
            warning_data = weather_warning()
            response['message'] = format_weather_response(district, time_period, weather_type, warning_data)
        else:
            # Get general weather forecast
            forecast_data = several_days_weather_forecast()
            response['message'] = format_weather_response(district, time_period, weather_type, forecast_data)
    else:
        response['message'] = 'I can help you with weather information. What would you like to know?'
    
    return jsonify(response)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 