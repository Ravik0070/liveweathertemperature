from django.shortcuts import redirect, render
import requests
from django.conf import settings
import datetime
from geopy.geocoders import Nominatim

def home(request):
     # -------------location------
        api = settings.API_KEY
        res = requests.get('https://ipinfo.io/')
        data = res.json()
        lat1 , long1  = data['loc'].split(',',1)
        lat = float(lat1)
        lon = float(long1)
        city = data['city']
        country = data['country']
        # -------------location end------
        url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api}'
        response = requests.get(url).json()
        temp = response['main']['temp']
        temp = kelvinToCelcius(temp)
        desc = response['weather'][0]['description']
        humidity = response['main']['humidity']
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
        for i in range(len(forecastDate)):
                forecastDate[i] = forecastDate[i].strftime('%d %b, %Y')
        return render(request,'base.html',{'fdate':forecastDate,'ftemp':forecastTemp,'fwind':forecastWind,'fdesc':forecastDesc
        ,'temp':temp,'desc':desc,'humidity':humidity,'date':d,'city':city,'country':country})

def livehome(request):
        api = settings.API_KEY
        geolocator = Nominatim(user_agent="geoapiExercises")
        if request.method == "GET":
                l1 = request.GET.get('latitude','28.6504')  
                l2 = request.GET.get('longitude','77.2372')
                if(not l1 and not l2):
                        return render(request,"error.html")
                else:
                        print(l1)
                        lat = float(l1)
                        lon = float(l2)
                        city = str(geolocator.reverse(f'{lat},{lon}'))
                        city_list = city.split(',')
                        city = city_list[0]
                        city1 = city_list[3]
                        url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api}'
                        response = requests.get(url).json()
                        temp = response['main']['temp']
                        temp = kelvinToCelcius(temp)
                        desc = response['weather'][0]['description']
                        humidity = response['main']['humidity']
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
                        for i in range(len(forecastDate)):
                                forecastDate[i] = forecastDate[i].strftime('%d %b, %Y')
                        return render(request,'livelocation.html',{'fdate':forecastDate,'ftemp':forecastTemp,'fwind':forecastWind,'fdesc':forecastDesc
                        ,'temp':temp,'desc':desc,'city':city,'city1':city1,'humidity':humidity,'date':d})
        else:
                return render(request,'result.html')

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

