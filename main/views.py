import requests
from django.shortcuts import render
from .models import searchHistory

API_KEY = 'efd6a633e8fc7a53833b61d8afdafd35'

def index(request):
    weather= None
    error= None
    recent_searches= searchHistory.objects.all().order_by('-searched_at')[:5]
    
    if request.method == 'POST':
        city_name= request.POST.get('city_name','').strip()
        if city_name:
            url= f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
            try:
                response = requests.get(url,timeout=5)
                weather_data = response.json()
                if response.status_code == 200:
                    weather ={
                    'city': weather_data['name'],
                    'temperature': weather_data['main']['temp'],
                    'humidity': weather_data['main']['humidity'],
                    'pressure': weather_data['main']['pressure'],
                    'description': weather_data['weather'][0]['description'].title(),
                    'icon': weather_data['weather'][0]['icon'],
                    }
                
                    # Save the search history
                    searchHistory.objects.create(
                        city_name= weather_data['name'],
                        temperature= weather_data['main']['temp'],
                        humidity= weather_data['main']['humidity'],
                        pressure=weather_data['main']['pressure'],
                        description= weather_data['weather'][0]['description'].title()
                    )

                    #refresh the recent searches after saving the new search
                    recent_searches= searchHistory.objects.order_by('-searched_at')[:5]
                else:
                    
                    error= weather_data.get("message", "Could not retrieve weather data. Please try again.")
            except requests.exceptions.RequestException as e:
                error= "An error occurred while fetching weather data. Please try again later."
        
        else:
            error= "Please enter a city name."

    return render(request, 'index.html', {
            'weather': weather, 
            'error': error, 
            'recent_searches': recent_searches
            })
# Create your views here.
