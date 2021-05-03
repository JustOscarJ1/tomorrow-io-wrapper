import requests
from datetime import datetime
import ctypes
from PIL import Image, ImageDraw, ImageFont

def get_weather_information(location, api_key, timezone_shift):
    weather_information = requests.get(f'https://api.tomorrow.io/v4/timelines?location={location[0]},{location[1]}&fields=temperature&timesteps=1h&units=imperial&apikey={api_key}').json()
    nodes = []
    for node in weather_information['data']['timelines'][0]['intervals']:
        node_alpha = [node['startTime'][11:13], node['values']['temperature']]
        nodes.append(node_alpha)

    for index, node in enumerate(nodes): # conversion from UTC to AEST
        nodes[index][0] = int(int(nodes[index][0]) + timezone_shift)%24 # converts UTC to local timezone using the shift of the timezone relative to UTC

        if node[0] == 0 and index != 0: # removes all past the day
            nodes = nodes[:index]
            break
    return nodes

def convert_temperatures(temp, system_f_c):
    if system_f_c.lower() == 'f': # if the temperature system is fahrenheit
        return (temp-32) * 5/9 # conversion
    elif system_f_c.lower() == 'c': # if system is celsius
        return (temp * 9/5) + 32 # conversion
    else:
        raise TypeError # if system is wrong

nodes = get_weather_information(['COORDINATE1', 'COORDINATE2'], 'API_KEY_HERE', TIMEZONE_SHIFT)

class Temperature:
    def __init__(self):
        self.celsius = 0
        self.fahrenheit = 0

class Weather:
    def __init__(self):
        self.heat = Temperature()
        self.time = 0
        self.hours_in_day = 0
        self.temperature_information = []

    def update_information(self):
        self.heat.fahrenheit = abs([i[1] for i in nodes if i[0] == datetime.now().hour][0])
        self.heat.celsius = convert_temperatures(self.heat.fahrenheit, 'f')
        self.time = datetime.now().hour
        self.hours_in_day = len(nodes)
        self.temperature_information = nodes



weather_handler = Weather()

weather_handler.update_information()

print(weather_handler.hours_in_day, weather_handler.heat.celsius, weather_handler.heat.fahrenheit, weather_handler.time)