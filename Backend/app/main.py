import fastapi
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "backend is running"}