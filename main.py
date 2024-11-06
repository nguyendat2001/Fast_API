import os
import sys

from fastapi import FastAPI

from controllers import example
from middlewares import corsMiddlewares
from middlewares import staticMiddlewares

sys.path.append('c:\\users\\ntien\\appdata\\local\\programs\\python\\python312\\lib\\site-packages')
sys.path.append('c:\\users\\ntien\\appdata\\Roaming\\python\\python312\\site-packages')

app = FastAPI()

corsMiddlewares.add(app)
staticMiddlewares.add(app)

app.include_router(example.router)