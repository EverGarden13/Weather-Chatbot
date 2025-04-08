from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from dotenv import load_dotenv
from weather_data import local_weather, rainfall_nowcast, uv_index, weather_warning, several_days_weather_forecast

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# District coordinates mapping
DISTRICT_COORDINATES = {
    'central': {'lat': 22.2828, 'lng': 114.1588},
    'wan chai': {'lat': 22.2783, 'lng': 114.1747},
    'causeway bay': {'lat': 22.2829, 'lng': 114.1837},
    'tai po': {'lat': 22.4501, 'lng': 114.1694},
    'shatin': {'lat': 22.3833, 'lng': 114.1833},
    'tuen mun': {'lat': 22.3911, 'lng': 113.9714},
    'yuen long': {'lat': 22.4445, 'lng': 114.0225}
}

def is_greeting(text):
    """Check if the text is a greeting"""
    greetings = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening']
    return any(greeting in text.lower() for greeting in greetings)

def is_weather_query(text):
    """Check if the text contains weather-related keywords"""
    weather_keywords = ['weather', 'temperature', 'rain', 'humidity', 'uv', 'forecast', 'wind']
    return any(keyword in text.lower() for keyword in weather_keywords)

def extract_district(text):
    """Extract Hong Kong district from text"""
    for district in DISTRICT_COORDINATES.keys():
        if district in text.lower():
            return district
    return None

def get_forecast_period(text):
    """Extract forecast period from text"""
    text = text.lower()
    if '3 day' in text or '3-day' in text or '3day' in text:
        return '3day'
    elif '2 day' in text or '2-day' in text or '2day' in text:
        return '2day'
    elif 'tomorrow' in text:
        return 'tomorrow'
    elif 'today' in text:
        return 'today'
    return None

def get_weather_info_type(text):
    """Extract specific weather information type from text"""
    text = text.lower()
    if 'wind' in text:
        return 'wind'
    elif 'temperature' in text:
        return 'temperature'
    elif 'humidity' in text:
        return 'humidity'
    elif 'uv' in text:
        return 'uv'
    elif 'overall' in text or 'general' in text:
        return 'overall'
    return 'overall'

def get_weather_recommendations(weather_info, info_type):
    """Get recommendations based on weather conditions"""
    recommendations = {
        'temperature': {
            'hot': ['Stay hydrated', 'Wear light clothing', 'Use sunscreen', 'Avoid outdoor activities between 11am-3pm'],
            'moderate': ['Perfect for outdoor activities', 'Light jacket might be needed', 'Great time for sightseeing'],
            'cold': ['Wear warm clothing', 'Bring an umbrella', 'Indoor activities recommended']
        },
        'humidity': {
            'high': ['Use dehumidifier indoors', 'Stay in air-conditioned areas', 'Drink plenty of water'],
            'moderate': ['Perfect for outdoor activities', 'Good time for hiking', 'Enjoy the weather'],
            'low': ['Use moisturizer', 'Stay hydrated', 'Use humidifier indoors']
        },
        'wind': {
            'strong': ['Secure loose objects', 'Be careful when walking', 'Indoor activities recommended'],
            'moderate': ['Good for flying kites', 'Perfect for sailing', 'Enjoy the breeze'],
            'light': ['Good for outdoor activities', 'Perfect for picnics', 'Enjoy the calm weather']
        },
        'uv': {
            'extreme': ['Avoid sun exposure', 'Use SPF 50+ sunscreen', 'Wear protective clothing'],
            'high': ['Use sunscreen', 'Wear a hat', 'Limit sun exposure'],
            'moderate': ['Use SPF 30+ sunscreen', 'Safe for outdoor activities with protection'],
            'low': ['Safe for outdoor activities', 'Basic sun protection recommended']
        },
        'overall': {
            'sunny': ['Bring sunglasses', 'Wear sunscreen', 'Stay hydrated'],
            'cloudy': ['Perfect for outdoor activities', 'Bring a light jacket', 'Good for photography'],
            'rainy': ['Bring an umbrella', 'Wear waterproof shoes', 'Indoor activities recommended']
        }
    }

    if info_type == 'temperature':
        temp = float(weather_info['Temp']['Value']) if isinstance(weather_info, dict) else float(weather_info)
        if temp >= 28:
            return recommendations['temperature']['hot']
        elif temp <= 15:
            return recommendations['temperature']['cold']
        return recommendations['temperature']['moderate']
    
    elif info_type == 'humidity':
        humidity = float(weather_info['RH']['Value']) if isinstance(weather_info, dict) else float(weather_info)
        if humidity >= 80:
            return recommendations['humidity']['high']
        elif humidity <= 40:
            return recommendations['humidity']['low']
        return recommendations['humidity']['moderate']
    
    elif info_type == 'wind':
        wind_speed = float(weather_info['Wind']['WindSpeed']) if isinstance(weather_info, dict) else float(weather_info)
        if wind_speed >= 30:
            return recommendations['wind']['strong']
        elif wind_speed <= 10:
            return recommendations['wind']['light']
        return recommendations['wind']['moderate']
    
    elif info_type == 'uv':
        uv_index = float(weather_info['max_uv_index'])
        if uv_index >= 11:
            return recommendations['uv']['extreme']
        elif uv_index >= 8:
            return recommendations['uv']['high']
        elif uv_index >= 3:
            return recommendations['uv']['moderate']
        return recommendations['uv']['low']
    
    # For overall weather, base it on temperature and description
    temp = float(weather_info['Temp']['Value']) if isinstance(weather_info, dict) else 25
    if temp >= 28:
        return recommendations['overall']['sunny']
    elif temp <= 15:
        return recommendations['overall']['rainy']
    return recommendations['overall']['cloudy']

def format_weather_response(district, coords, period, info_type):
    """Format weather data into a dialogue-friendly response"""
    try:
        # Get local weather data
        local_data = local_weather(coords['lat'], coords['lng'])
        
        # Get UV index data
        uv_data = uv_index('EN')
        
        # Get forecast data
        forecast_data = several_days_weather_forecast('EN')
        
        # Get any active warnings
        warning_data = weather_warning('EN')
        
        if period == 'today':
            weather = local_data['result']['RegionalWeather']
            
            if info_type == 'wind':
                wind_info = weather['Wind']
                response = f"Current wind conditions in {district.capitalize()}: {wind_info['WindSpeed']} km/h from the {wind_info['WindDirection']} ({wind_info['WindDirectionCode']})"
                recommendations = get_weather_recommendations(weather, 'wind')
                response += "\n\nRecommendations:\n" + "\n".join(f"• {rec}" for rec in recommendations)
                return response
                
            elif info_type == 'temperature':
                temp_info = weather['Temp']
                response = f"Current temperature in {district.capitalize()} is {temp_info['Value']}°C"
                recommendations = get_weather_recommendations(weather, 'temperature')
                response += "\n\nRecommendations:\n" + "\n".join(f"• {rec}" for rec in recommendations)
                return response
                
            elif info_type == 'humidity':
                rh_info = weather['RH']
                response = f"Current humidity in {district.capitalize()} is {rh_info['Value']}%"
                recommendations = get_weather_recommendations(weather, 'humidity')
                response += "\n\nRecommendations:\n" + "\n".join(f"• {rec}" for rec in recommendations)
                return response
                
            elif info_type == 'uv':
                response = f"Current UV index in {district.capitalize()}: {uv_data['result']['max_uv_index']} ({uv_data['result']['intensity']})"
                recommendations = get_weather_recommendations(uv_data['result'], 'uv')
                response += "\n\nRecommendations:\n" + "\n".join(f"• {rec}" for rec in recommendations)
                return response
                
            else:  # overall
                response = f"Current weather in {district.capitalize()}:\n"
                response += f"• Temperature: {weather['Temp']['Value']}°C\n"
                response += f"• Humidity: {weather['RH']['Value']}%\n"
                response += f"• Wind: {weather['Wind']['WindSpeed']} km/h from the {weather['Wind']['WindDirection']} ({weather['Wind']['WindDirectionCode']})\n"
                response += f"• UV Index: {uv_data['result']['max_uv_index']} ({uv_data['result']['intensity']})"
                
                # Add any active warnings
                active_warnings = [w['Name'] for w in warning_data['result'].values() if w['InForce'] == 1]
                if active_warnings:
                    response += "\n\nActive Warnings:\n"
                    response += "\n".join(f"• {w}" for w in active_warnings)
                
                # Add recommendations
                recommendations = get_weather_recommendations(weather, 'overall')
                response += "\n\nRecommendations:\n" + "\n".join(f"• {rec}" for rec in recommendations)
                return response
        
        else:
            # Format multi-day forecast
            forecast = forecast_data['result']['forecast_detail']
            days_to_show = 3 if period == '3day' else (2 if period == '2day' else 1)
            
            if info_type != 'overall':
                # For specific info types in multi-day forecast
                response = f"{days_to_show}-day {info_type} forecast for {district.capitalize()}:\n\n"
                
                for i, day in enumerate(forecast[:days_to_show]):
                    date = day['forecast_date']
                    day_name = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][day['forecast_day_of_week']]
                    
                    response += f"{day_name} ({date[4:6]}/{date[6:8]}):\n"
                    if info_type == 'wind':
                        response += f"• Wind: {day['wind_info']}\n"
                    elif info_type == 'temperature':
                        response += f"• Temperature: {day['min_temp']}°C to {day['max_temp']}°C\n"
                    elif info_type == 'humidity':
                        response += f"• Humidity: {day['min_rh']}% to {day['max_rh']}%\n"
                    if i < days_to_show - 1:
                        response += "\n"
                
                return response
            else:
                # Overall forecast
                response = f"{days_to_show}-day forecast for {district.capitalize()}:\n\n"
                
                for i, day in enumerate(forecast[:days_to_show]):
                    date = day['forecast_date']
                    day_name = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][day['forecast_day_of_week']]
                    
                    response += f"{day_name} ({date[4:6]}/{date[6:8]}):\n"
                    response += f"• {day['wx_desc']}\n"
                    response += f"• Temperature: {day['min_temp']}°C to {day['max_temp']}°C\n"
                    response += f"• Humidity: {day['min_rh']}% to {day['max_rh']}%\n"
                    response += f"• Wind: {day['wind_info']}\n"
                    if i < days_to_show - 1:
                        response += "\n"
                
                return response
            
    except Exception as e:
        print(f"Error in format_weather_response: {str(e)}")  # Add logging
        return f"Sorry, I couldn't get the weather information for {district.capitalize()} at the moment. Please try again later."

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message', '').lower()
    
    # Initialize response
    response = {
        'message': '',
        'status': 'success',
        'needs_location': False,
        'needs_forecast_period': False,
        'needs_info_type': False,
        'selected_location': None,
        'selected_period': None
    }
    
    # Handle greeting
    if is_greeting(user_input):
        response['message'] = "Hello! I'm your Hong Kong Weather Assistant. How can I help you today?"
        return jsonify(response)
    
    # Extract district and period from input
    district = extract_district(user_input)
    period = get_forecast_period(user_input)
    
    # Check if this is just a location selection without any weather terms
    if district and not is_weather_query(user_input):
        response['message'] = f"You've selected {district.capitalize()}. Would you like to know the weather for today, tomorrow, 2-day forecast, or 3-day forecast?"
        response['needs_forecast_period'] = True
        response['selected_location'] = district
        return jsonify(response)
    
    # Handle weather query
    if is_weather_query(user_input):
        # If no district is mentioned, ask for location
        if not district:
            response['message'] = 'Which district in Hong Kong would you like to know the weather for?'
            response['needs_location'] = True
            return jsonify(response)
        
        # Get coordinates for the district
        coords = DISTRICT_COORDINATES[district]
        
        # If we have a location but no time period specified, ask for it
        if not period:
            response['message'] = f"For {district.capitalize()}, would you like to know the weather for today, tomorrow, 2-day forecast, or 3-day forecast?"
            response['needs_forecast_period'] = True
            response['selected_location'] = district
            return jsonify(response)
        
        # If we have location and time but no specific info type, ask for it
        info_type = get_weather_info_type(user_input)
        if info_type == 'overall' and not any(keyword in user_input for keyword in ['overall', 'general', 'temperature', 'humidity', 'wind', 'uv']):
            response['message'] = f"What specific information would you like to know? (overall weather, temperature, humidity, wind, or UV index)"
            response['needs_info_type'] = True
            response['selected_location'] = district
            response['selected_period'] = period
            return jsonify(response)
        
        # If we have all information, format the response
        response['message'] = format_weather_response(district, coords, period, info_type)
    else:
        response['message'] = "I can help you with weather information for different districts in Hong Kong. What would you like to know?"
    
    return jsonify(response)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 