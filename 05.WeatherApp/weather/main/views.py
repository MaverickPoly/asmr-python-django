from django.shortcuts import render
from django.http import HttpRequest
import requests

API_KEY = "API_KEY"


def get_weather(request: HttpRequest):
    city = request.GET.get("city", "Moscow")
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    weather_data = response.json()

    context = {
        "city": city,
        "temperature": weather_data.get("main", {}).get("temp", "N/A"),
        "description": weather_data.get("weather", [{}])[0].get("description", "N/A"),
        "icon": weather_data.get("weather", [{}])[0].get("icon", ""),
    }
    return render(request, "home.html", context)
