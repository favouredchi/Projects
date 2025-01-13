# Create a third-party weather service that returns the current weather for a given city.
# The service should have the following features: Return the current weather for a given city, state, country

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

class Weather(BaseModel):
    city: str
    state: str
    country: str

@app.get("/weather/")
def get_weather(weather: Weather):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={weather.city},{weather.state},{weather.country}&appid=YOUR_API_KEY"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="City not found")
    return response.json()


