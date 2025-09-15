# servise/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .router import router
import os

app = FastAPI(
    title="Cyber Security Laboratory API",
    description="Сервис приёма и обработки событий безопасности",
    version="0.1.0",
)

app.include_router(router, prefix="/api")

# Статические файлы
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def dashboard():
    return FileResponse("static/dashboard.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("servise.main:app", host="0.0.0.0", port=8000, reload=True)
