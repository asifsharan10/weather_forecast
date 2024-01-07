from django.shortcuts import render
from django.contrib import messages
import requests
import datetime


def home(request):
    # Get the entered city from the form or default to 'indore'
    city = request.POST.get('city', 'Dhaka')

    # OpenWeatherMap API URL
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=08dc298e7d368edf06ad003a788f342a'
    # Parameters for OpenWeatherMap API
    weather_params = {'units': 'metric'}

    # Google Custom Search API parameters
    API_KEY = 'AIzaSyDLyTJJ7T7GaEPelgio_O2ViHO6-7semg0'
    SEARCH_ENGINE_ID = '46246e9e96d0b4631'
    query = city + " 1920x1080"
    start = 1
    searchType = 'image'
    search_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"

    try:
        # Fetch weather data from OpenWeatherMap
        weather_data = requests.get(weather_url, params=weather_params).json()
        description = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
        temp = weather_data['main']['temp']
        day = datetime.date.today()

        # Fetch image URL from Google Custom Search
        image_data = requests.get(search_url).json()
        search_items = image_data.get("items")
        
        # Check if there are search items and use the first item's link
        image_url = search_items[0]['link'] if search_items else None

        return render(request, 'weatherapp/index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'exception_occurred': False,
            'image_url': image_url
        })

    except Exception as e:
        exception_occurred = True
        messages.error(request, 'Entered data is not available from the API')

        day = datetime.date.today()

        return render(request, 'weatherapp/index.html', {
            'description': 'clear sky',
            'icon': '01d',
            'temp': 25,
            'day': day,
            'city': 'indore',
            'exception_occurred': exception_occurred
        })
               
    
    