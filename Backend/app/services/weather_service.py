import requests
from app.core.config import settings

class WeatherService:
    BASE_URL = "http://api.weatherapi.com/v1/forecast.json"

    def get_weather(self, location: str, date: str):
        params = {
            "key": settings.WEATHERAPI_KEY,
            "q": location,
            "dt": date,
        }
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        # Extract weather info as needed
        condition = data["forecast"]["forecastday"][0]["day"]["condition"]["text"]
        temp_c = data["forecast"]["forecastday"][0]["day"]["avgtemp_c"]
        return {"condition": condition, "temp_c": temp_c} 