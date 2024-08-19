import requests
from django.conf import settings


def get_weather_data_main(nairobi):
    api_key = settings.OPENWEATHERMAP_API_KEY
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': nairobi,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
    return response.json() if response.status_code == 200 else None
