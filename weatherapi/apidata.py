from django.http import requests
import datetime

def currentLocation():
    def __init__(self):
        # -------------location------
        res = requests.get('https://ipinfo.io/')
        data = res.json()
        city = data['city']
        country = data['country']
        postal = int(data['postal'])
        region = data['region']
        timezones = data['timezone']
        lat1 , long1  = data['loc'].split(',',1)
        lat = float(lat1)
        lon = float(long1)
        # -------------location end------

        def currentLocationTemp(self):
            url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api}'
            response = requests.get(url).json()
            temp = response['main']['temp']
            temp = kelvinToCelcius(temp)
            desc = response['weather'][0]['description']
            cloudiness = response['clouds']['all']
            print(temp , desc , cloudiness)

    def kelvinToCelcius(temp):
        temp = temp - 273.15  #kelvin to celcius 
        temp = "{:.2f}".format(temp)
        return temp
