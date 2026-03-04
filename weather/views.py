import os

import requests
from django.shortcuts import render
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

API_KEY = os.environ.get('OPENWEATHER_API_KEY', '')


def home(request):
    """
    Handle the home page:
      • Show a search form for a city name.
      • If a city is submitted, fetch live weather
        data from OpenWeatherMap and display it.
    """
    city = request.GET.get('city', '').strip()

    # Default context – nothing to display yet
    context = {
        'city': city,
        'temperature': None,
        'description': None,
        'error': None,
    }

    if city:
        url = (
            'https://api.openweathermap.org/data/2.5/weather'
            f'?q={city}&appid={API_KEY}&units=metric'
        )

        try:
            response = requests.get(url, timeout=10)
            data = response.json()

            if response.status_code == 200:
                context['temperature'] = data['main']['temp']
                context['description'] = data['weather'][0]['description']
            else:
                # API returned an error (e.g. city not found)
                context['error'] = data.get('message', 'City not found.')

        except requests.exceptions.RequestException:
            context['error'] = 'Could not connect to the weather service.'

    return render(request, 'weather/home.html', context)
