from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import requests



app = FastAPI()
base_dir = Path(__file__).resolve().parent
appid = "864c4318180aba64438e754c17488c3c"

@app.get('/api/weather')
def weather_get(city_str: str = "moscow"):
    params = {
        'q': city_str,
        'type': 'like', 
        'units': 'metric', 
        'APPID': appid
    } 
    city_id = -1
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find", params=params)
        city_data = res.json()
        for i in city_data["list"]:
            if i["sys"]["country"] == "RU":
                city_id = i["id"]
                break
            else:
                return {"message": "city_is_not_found"}
    except RuntimeError as Err:
        pass
    weather_params = {
        'id': city_id, 
        'units': 'metric', 
        'lang': 'ru', 
        'APPID': appid
    }
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather", params=weather_params)
        weather_data = res.json()
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast", params=weather_params)
        forecast_weather_data = res.json()
        days_list = {}
        for i in range(1,6):
            days_list[f"{i}_day"] = {
                "weather": forecast_weather_data["list"][i]["weather"],
                "main": forecast_weather_data["list"][i]["main"],
                "wind": forecast_weather_data["list"][i]["wind"]
            } 
        return {
            "weather_now": weather_data["weather"],
            "weather_now_main": weather_data["main"],
            "weather_now_wind": weather_data["wind"],
            "day_list": days_list
            }
    except ConnectionAbortedError as err:
        raise (err.__format__(ConnectionAbortedError))

@app.get("/")
def show_weather(city_str: str = "moscow"):
    return FileResponse(str(base_dir / "static/weather.html"))
