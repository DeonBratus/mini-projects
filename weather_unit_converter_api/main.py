import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from converter_app.app import app as convapp
from start_app.app import app as startapp
from weather_app.app import app as wapp
app = FastAPI()

app.mount("/converter", convapp)
app.mount("/weather", wapp)
app.mount("/weather_static", StaticFiles(directory="weather_app/static/"), name="/static")
app.mount("/conv_static", StaticFiles(directory="converter_app/static/"), name="/static")
app.mount("/", startapp)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
