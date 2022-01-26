from django.urls import path 
from weatherapi.views import home,searchcity,livehome

app_name = 'weatherapi'

urlpatterns = [
    path('',home,name="home"),
    path('livetemp/',livehome,name="livehome"),
    path('searchcity/',searchcity,name="searchcity"),
]
