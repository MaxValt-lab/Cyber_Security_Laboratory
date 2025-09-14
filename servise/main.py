# servise/main.py

from fastapi import FastAPI
from .router import router

app = FastAPI(
    title="Cyber Security Laboratory API",
    description="Сервис приёма и обработки событий безопасности",
    version="0.1.0",
)

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("servise.main:app", host="0.0.0.0", port=8000, reload=True)
