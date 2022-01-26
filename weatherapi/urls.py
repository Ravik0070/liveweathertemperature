from django.urls import path 
from weatherapi.views import home,searchcity

app_name = 'weatherapi'

urlpatterns = [
    path('',home,name="home"),
    path('searchcity/',searchcity,name="searchcity"),
]
