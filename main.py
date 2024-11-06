import os
import sys

sys.path.append('c:\\users\\ntien\\appdata\\local\\programs\\python\\python312\\lib\\site-packages')
sys.path.append('c:\\users\\ntien\\appdata\\Roaming\\python\\python312\\site-packages')
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}