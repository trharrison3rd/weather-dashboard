import requests

def fetch_weather(location, api_key):
    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}")
    return response.json()