from django.shortcuts import get_object_or_404, render, redirect
import requests
from .models import Cities

def weather_app(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=15a7aa2d38a57f4e0fc8b03819bb76a9'
    weather_data = []
    cities_list = Cities.objects.all()
    
    if request.method == 'POST':
        if 'city' in request.POST:
            city_name = request.POST.get('city')
            if city_name:
                response = requests.get(url.format(city_name)).json()
                if response.get('cod') == 200:  # Success
                    _, created = Cities.objects.get_or_create(city=city_name)
                else:
                    err_msg = 'City does not exist!'
        elif 'city_id' in request.POST:  # New block for deletion
            city_id = request.POST.get('city_id')
            city = get_object_or_404(Cities, id=city_id)
            city.delete()
    
    for city in cities_list:
        get_weather = requests.get(url.format(city)).json()
        if get_weather.get('cod') == 200:  # Check for a successful response
            weather = {
                'city': city,
                'temp': get_weather['main']['temp'],
                'desc': get_weather['weather'][0]['description'],
                'icon': get_weather['weather'][0]['icon'],
            }
            weather_data.append(weather)
        else:
            # Here, handle what happens if the API request was not successful
            print(f"Error getting weather for {city.city}: {get_weather.get('message', '')}")
    
    context = {'weather_data': weather_data}

    return render(request, 'weather/weather_page.html', context)
