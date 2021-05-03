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

    for index, node in enumerate(nodes):
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

class Temperature:
    def __init__(self):
        self.celsius = 0
        self.fahrenheit = 0


class Weather:
    def __init__(self, location, api_key, timezone_shift):
        self.heat = Temperature()
        self.time = 0
        self.hours_in_day = 0
        self.temperature_information = []
        self.nodes = get_weather_information(location, api_key, timezone_shift)

    def update_information(self):
        self.heat.fahrenheit = abs([i[1] for i in self.nodes if i[0] == datetime.now().hour][0])
        self.heat.celsius = convert_temperatures(self.heat.fahrenheit, 'f')
        self.time = datetime.now().hour
        self.hours_in_day = len(self.nodes)
        self.temperature_information = self.nodes


weather_handler = Weather(location, api_key, timezone_shift)

weather_handler.update_information()

print(weather_handler.hours_in_day, weather_handler.heat.celsius, weather_handler.heat.fahrenheit, weather_handler.time)

temp = weather_handler.heat.celsius
image_path = 'path' #path images are located
font_path = 'path' #path fonnt & result.png is
if temp < -10:
    temp_condition = 'Unbearably Cold'
    picture = 'cold.png'
    color = '#EC9A29'
elif temp < 0:
    temp_condition = 'Extremely Cold'
    picture = 'cold.png'
    color = '#EC9A29'
elif temp < 10:
    temp_condition = 'Cold'
    picture = 'cold.png'
    color = '#EC9A29'
elif temp < 15:
    temp_condition = 'Cool'
    picture = 'cold.png'
    color = '#EC9A29'
elif temp < 20:
    temp_condition = 'Warm'
    picture = 'warm.png'
    color = '#45b6d9'
elif temp < 25:
    temp_condition = 'Hot'
    picture = 'warm.png'
    color = '#f24c27'
elif temp < 37:
    temp_condition = 'Very Hot'
    picture = 'hot.png'
    color = '#f24c27'
elif temp < 50:
    temp_condition = 'Extremely Hot'
    picture = 'hot.png'
    color = '#f24c27'
elif temp < 60:
    temp_condition = 'Unbearably Hot'
    picture = 'hot.png'
    color = '#f24c27'
elif temp < 90:
    temp_condition = 'Deathly Hot'
    picture = 'hot.png'
    color = '#f24c27'
elif temp < 500:
    temp_condition = 'You are not reading this.'
    picture = 'hot.png'
    color = '#f24c27'

print(color)

def add_text(text,file, font_color):
    img_fraction = 0.50
    image = Image.open(file)

    fontsize = 1
    font = ImageFont.truetype(font_path + "bestfont.ttf", fontsize)
    while font.getsize(text)[0] < img_fraction * image.size[0]:
        fontsize += 1
        font = ImageFont.truetype(font_path + "bestfont.ttf", fontsize)
    W, H = image.size
    draw = ImageDraw.Draw(image)
    w, h = draw.textsize(text, font)
    print(W,H,w,h)
    draw.text(((W-w)/2,(H-h)/2), text, fill=color, font=font)

    image.save("result.png", "PNG")
add_text(f'It is currently {round(weather_handler.heat.celsius)}c. {temp_condition}', image_path + picture, color)

ctypes.windll.user32.SystemParametersInfoW(20,0,font_path + 'result.png',0)
