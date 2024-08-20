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

#CLIENT_ID = 'by462onfaxsc3ynv8b951ako0o1n99'
#CLIENT_SECRET = '3vmdqjd5m9wtd1u9lhqwb9byq2qcdv'
#
#def get_twitch_access_token():
#    url = 'https://id.twitch.tv/oauth2/token'
#    params = {
#        'client_id': CLIENT_ID,
#        'client_secret': CLIENT_SECRET,
#        'grant_type': 'client_credentials'
#    }
#    response = requests.post(url, params=params)
#    data = response.json()
#    return data['access_token']

#def get_twitch_streams(game_name):
#    access_token = get_twitch_access_token()
#    headers = {
#        'Client-ID': CLIENT_ID,
#        'Authorization': f'Bearer {access_token}'
#    }
#    url = 'https://api.twitch.tv/helix/streams'
#    params = {
#        'game_name': game_name,  # Game name to search for
#        'first': 5  # Number of streams to retrieve
#    }
#    response = requests.get(url, headers=headers, params=params)
#    return response.json()['data']


