# weather_fetcher.py
# ---
# Fetches current weather data from the Weatherstack API.

import requests
from config import Config

BASE_URL = "http://api.weatherstack.com/current"

def get_current_weather(city=None):
    """
    Fetches the current weather for a specified city or the default city.
    
    Args:
        city (str, optional): The city name. Defaults to Config.DEFAULT_LOCATION.
        
    Returns:
        str: A formatted string describing the weather, or an error message.
    """
    
    query_location = city if city else Config.DEFAULT_LOCATION
    
    params = {
        'access_key': Config.WEATHERSTACK_API_KEY,
        'query': query_location,
        'units': 'm'  # 'm' for Metric (Celsius, km/h)
    }
    
    try:
        # Make the API request
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        
        data = response.json()
        
        # Check for API error (e.g., invalid key, non-existent city)
        if 'current' not in data:
            if 'error' in data:
                return f"Weather Error: {data['error']['info']}"
            return "Weather Error: Could not parse response."

        # Extract relevant data
        location = data['location']['name']
        temp = data['current']['temperature']
        description = data['current']['weather_descriptions'][0]
        feels_like = data['current']['feelslike']
        
        # Format the output string
        weather_string = (
            f"The current weather in {location} is {description}, "
            f"with a temperature of {temp} degrees Celsius. "
            f"It feels like {feels_like} degrees."
        )
        return weather_string

    except requests.exceptions.HTTPError as errh:
        return f"Weather Request Error (HTTP): {errh}"
    except requests.exceptions.ConnectionError as errc:
        return "Weather Request Error: Could not connect to the internet."
    except requests.exceptions.Timeout as errt:
        return "Weather Request Error: Request timed out."
    except requests.exceptions.RequestException as err:
        return f"Weather Request Error: An unexpected error occurred. {err}"
    except Exception as e:
        return f"An unexpected processing error occurred: {e}"