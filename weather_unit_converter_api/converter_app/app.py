from fastapi import FastAPI, Body, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from .units import Units, convertData, unit_options
from pathlib import Path
import httpx

app = FastAPI()
base_dir = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(base_dir / "templates"))

@app.get("/")
def converter_main():
    return FileResponse(str(base_dir / "templates/index.html"))

@app.get('/{unit_type}', response_class=HTMLResponse)
def converter(request: Request, unit_type: str):
    units = unit_options.get(unit_type)
    return templates.TemplateResponse("converter.html", 
        {
            "request": request, 
            "title_name": unit_type.lower(),
            "units": units
        }
    )


@app.post('/{unit_type}', response_class=HTMLResponse)
def converter_handler(unit_type, request: Request,
    value: float = Form(...),
    unit_from: str = Form(...),
    unit_to: str = Form(...)
):
    data = {
        "unit_type": unit_type,
        "value": value,
        "unit_from": unit_from,
        "unit_to": unit_to
    }

    with httpx.Client() as client:
        response = client.post("http://127.0.0.1:8000/converter/api/converter", json=data)
    if response.status_code == 200:
        result = response.json()
        message = result["result"]
    else:
        message = response.status_code

    units = unit_options.get(unit_type)

    return templates.TemplateResponse("converter.html", {
        "request": request,
        "title_name": unit_type,
        "value": value,
        "message": message,
        "units": units
    })


@app.post('/api/converter')
def convert_units(data: convertData = Body(...)):
    
    created_unit_type = Units.create_unit_type(Units, data.unit_type)
    
    if data.unit_type != "temperature":
        unit_from_value = created_unit_type.units[data.unit_from]
        unit_to_value = created_unit_type.units[data.unit_to]
        result = data.value * (unit_from_value / unit_to_value)
    else:
        result = Units.Temperature().handle_temp_convert(data=data)

    return JSONResponse({"unit_type": data.unit_type, "result": result})


