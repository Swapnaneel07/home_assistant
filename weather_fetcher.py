# weather_fetcher.py
# ---
# Fetches current weather data from the free Open-Meteo API.

import requests
from config import Config

FORECAST_BASE_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODING_BASE_URL = "https://geocoding-api.open-meteo.com/v1/search"

def _get_coordinates(city_name):
    """
    Uses the Open-Meteo Geocoding API to find the latitude and longitude for a city name.
    """
    params = {
        'name': city_name,
        'count': 1,
        'language': 'en',
        'format': 'json'
    }
    
    try:
        response = requests.get(GEOCODING_BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        results = data.get('results')
        if results:
            # Return the coordinates of the first match
            return results[0]['latitude'], results[0]['longitude'], results[0]['name']
            
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Geocoding failed: {e}")
        
    return None, None, None


def get_current_weather(city=None):
    """
    Fetches the current weather for a specified city or the default city.
    """
    
    # 1. Determine location and get coordinates
    query_location = city if city else Config.DEFAULT_LOCATION_NAME
    
    lat, lon, location_name = _get_coordinates(query_location)
    
    if lat is None or lon is None:
        # Fallback to defaults if geocoding fails
        lat = Config.DEFAULT_LATITUDE
        lon = Config.DEFAULT_LONGITUDE
        location_name = Config.DEFAULT_LOCATION_NAME
        
        if query_location != Config.DEFAULT_LOCATION_NAME:
            # If the user specified a city that failed, report it
            return f"Sorry, I couldn't find coordinates for {query_location}. Checking the weather for {location_name} instead."

    # 2. Make the main weather API request
    params = {
        'latitude': lat,
        'longitude': lon,
        'current': 'temperature_2m,apparent_temperature,weather_code,wind_speed_10m',
        'temperature_unit': 'celsius',
        'wind_speed_unit': 'kmh',
        'timezone': 'auto'
    }
    
    try:
        response = requests.get(FORECAST_BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        current = data.get('current', {})
        
        if not current:
            return "Weather Error: Could not retrieve current data."

        # Extract data
        temp = current.get('temperature_2m', 'N/A')
        feels_like = current.get('apparent_temperature', 'N/A')
        weather_code = current.get('weather_code', 0)
        wind_speed = current.get('wind_speed_10m', 'N/A')
        
        # Simple WMO weather code description lookup (partial list)
        WMO_CODES = {
            0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
            45: "Fog", 51: "Drizzle", 61: "Rain", 71: "Snow", 95: "Thunderstorm"
        }
        description = WMO_CODES.get(weather_code, "Unknown conditions")
        
        # Format the output string
        weather_string = (
            f"The weather in {location_name} is currently {description}, "
            f"with a temperature of {temp} degrees Celsius. "
            f"It feels like {feels_like} degrees and the wind is {wind_speed} km/h."
        )
        return weather_string

    except requests.exceptions.RequestException as err:
        return f"Weather Request Error: Could not connect to the service. {err}"
    except Exception as e:
        return f"An unexpected processing error occurred: {e}"