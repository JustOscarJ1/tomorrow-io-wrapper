# TOMORROW.IO

### What is this repository?
This repository is a simple API wrapper whos intention is to allow programmers to get temperature information about their respective areas. It also includes examples of how the wrapper can be used programmatically.

------------

### Features
Programmers who use this wrapper will be using a Weather class to perform everything they need. This class contains four attributes and a simple "update_information" method.
These attributes are as follows:
- time `Returns the current date-time hour.`
- hours_in_day `Returns how many hours are left in the day, and how many temperature nodes are left for the day.`
- heat `Returns a Temperature class with both Celsius and Fahrenheit attributes.`

------------

### Quickstart
If you are simply trying to obtain the current temperature in your area, you can use this code.

```python
from tomorrow_io_wrapper import *
from weather_io_wrapper import *
weather_handler = Weather()
get_weather_information(['location1', 'location2'], 'api_key', timezone_shift(int))
weather_handler.update_information()
print(weather_handler.heat.celsius)
```

------------
### Examples
We provide one example of how this wrapper can be used programmatically. In this example the script would run every hour with Task Scheduler, when ran this script gets the current temperature then assigns a heat condition, `(Extremely Cold, Warm... etc)`.

The temperature and heat condition is written to a file (result.png), that file is then sent to be the computer's desktop background. This updates you on the temperature every hour in the background with nice images.

Try out this example.

------------
*If you have any ideas for new features or bugs/problems, make an issue and I will add them.*

