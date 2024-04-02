from django.shortcuts import render, redirect
import requests
from .models import Cities


def weather_app(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=15a7aa2d38a57f4e0fc8b03819bb76a9'
    weather_data= []
    cities_list = Cities.objects.all()
    
    if request.method == 'POST':
        city = request.POST.get('city')
        if city:
            add_city = Cities.objects.create(city=city)
            add_city.save()
            return redirect('/')

    for city in cities_list:
        get_weather = requests.get(url.format(city)).json()

        weather = {
           'city': city,
           'temp': get_weather['main']['temp'],
           'desc': get_weather['weather'][0]['description'],
           'icon': get_weather['weather'][0]['icon'],
       }
        weather_data.append(weather)
    
    context = {'weather_data': weather_data}

    return render(request, 'weather/weather_page.html', context)
