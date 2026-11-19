from fastapi import FastAPI
from .models import Product
from .database import session

app = FastAPI()

@app.get("/health")
def health_check():
    return "OK"

