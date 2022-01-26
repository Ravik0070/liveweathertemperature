from django.shortcuts import redirect, render
import requests
from django.conf import settings
import datetime

def home(request):
     # -------------location------
        api = settings.API_KEY
        res = requests.get(settings.IP_FIND)
        data = res.json()
        city = data['city']
        country = data['country']
        region = data['region']
        timezones = data['timezone']
        lat1 , long1  = data['loc'].split(',',1)
        lat = float(lat1)
        lon = float(long1)
        # -------------location end------

        url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api}'
        response = requests.get(url).json()
        temp = response['main']['temp']
        temp = kelvinToCelcius(temp)
        desc = response['weather'][0]['description']
        city = data['city']
        humidity = response['main']['humidity']

        # livecontext = {'temp':temp,'desc':desc,'city':city,'country':country,'region':region}
        forecastDate = [] 
        forecastTemp = [] 
        forecastWind = []
        forecastDesc = []

        url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=hourly&appid={api}'
        response = requests.get(url).json()
        t = response['daily'] 
        d = datetime.datetime.fromtimestamp(t[0]['dt'])
        d = d.strftime('%d %b,%Y')
        for i in range(5):
                forecastDate.append(datetime.datetime.fromtimestamp(t[i]['dt']))
                forecastTemp.append(kelvinToCelcius(temp = t[i]['temp']['day']))
                forecastWind.append(t[i]['wind_speed']) #m/s
                forecastDesc.append(t[i]['weather'][0]['description'])
        # forecast = {'fdate':forecastDate,'ftemp':forecastTemp,'fwind':forecastWind,'fdesc':forecastDesc}
        
        for i in range(len(forecastDate)):
                forecastDate[i] = forecastDate[i].strftime('%d %b, %Y')

        return render(request,'base.html',{'fdate':forecastDate,'ftemp':forecastTemp,'fwind':forecastWind,'fdesc':forecastDesc
        ,'temp':temp,'desc':desc,'city':city,'country':country,'region':region,'humidity':humidity,'date':d})

def searchcity(request):
        api = settings.API_KEY
        if request.method == "POST":
                citys = request.POST['searchcity']
                if not citys:
                        return render(request,'result.html')
                else:
                        url1 = f"http://api.openweathermap.org/data/2.5/weather?q={citys}&appid={api}"
                        url2 = f"http://api.openweathermap.org/data/2.5/forecast?q={citys}&appid={api}"
                        response1 = requests.get(url1).json()
                        response2 = requests.get(url2).json()
                        # print(response2)
                        forecastDate = [] 
                        forecastTemp = [] 
                        forecastWind = []
                        forecastDesc = []
                        if "city not found"  not in response1.values() and response2.values():
                                tempcity = response1['main']['temp']
                                tempcity = kelvinToCelcius(tempcity)
                                t = response2['list'] 
                                d = datetime.datetime.fromtimestamp(t[0]['dt'])
                                d = d.strftime('%d %b,%Y')
                                humidity =  t[0]['main']['humidity']
                                desc = t[0]['weather'][0]['description']
                                for i in range(5):
                                        forecastDate.append(datetime.datetime.fromtimestamp((t[i]['dt'])))
                                        forecastTemp.append(kelvinToCelcius(temp = t[i]['main']['temp']))
                                        forecastWind.append(t[i]['wind']['speed']) #m/s
                                        forecastDesc.append(t[i]['weather'][0]['description'])

                                for i in range(len(forecastDate)):
                                        forecastDate[i] = forecastDate[i].strftime('%H : %m %p')
                                return render(request,'result.html',{'tempcity':tempcity,'citys':citys ,'fdesc':forecastDesc,'ftemp':forecastTemp,
                                'desc':desc,'humidity':humidity,'fwind':forecastWind,'fdate':forecastDate,'date':d})
                        else:
                                return render(request,'result.html')
        else:
                return render(request,'result.html')
        
                


def kelvinToCelcius(temp):
        temp = temp - 273.15  #kelvin to celcius 
        temp = "{:.2f}".format(temp)
        return temp

