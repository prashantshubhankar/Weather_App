import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm


# Create your views here.


def index(request):

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={API_token}'
    cities = City.objects.all()

    error_msg = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            city_count = City.objects.filter(name=new_city).count()

            if city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    error_msg = 'City does not exist in the world!'
            else:
                error_msg = 'City already exists in the database!'

    form = CityForm()

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()
        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon']
        }

        weather_data.append(city_weather)

    context = {'weather_data': weather_data, 'form': form}

    return render(request, 'index.html', context)


def delete_city(request, city_name):

    City.objects.get(name=city_name).delete()

    return redirect('index')
