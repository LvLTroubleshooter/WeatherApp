from django.shortcuts import render
import requests
from .models import Cities


def weather_app(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=15a7aa2d38a57f4e0fc8b03819bb76a9'
    weather_data= []
    
    cities_list = Cities.objects.all()

    for city in cities_list:
        get_weather = requests.get(url.format(city)).json()

        print(get_weather)

    return render(request, 'weather/weather_page.html')
