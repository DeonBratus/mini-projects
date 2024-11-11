from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
app = FastAPI()
base_dir = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(base_dir / "static")), name="static")

@app.get('/')
def main_page() :
    return FileResponse(str(base_dir / "static/index.html"))