from datetime import datetime, timezone
import requests, json
from urllib2 import urlopen
import pytz

url = 'http://ipinfo.io/json'
response = urlopen(url)
data = json.load(response)
api_key = "9e70d3c23540669ff1c632376b427228"
base_url = "http://api.openweathermap.org/data/2.5/weather?"
IP = data['ip']
org = data['org']
city = data['city']
country = data['country']
region = data['region']
timezone = ['timezone']


def time_by_timezone():
    tz = pytz.timezone(timezone)
    time = datetime.now(tz)
    return time


def your_location():
    return city + "," + country


def get_weather():
    pass
