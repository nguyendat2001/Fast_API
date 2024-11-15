import os
import sys

import uvicorn

from fastapi import FastAPI

# from controllers import idCard
# from controllers import document
from controllers import hos_invoice
from middlewares import corsMiddlewares
from middlewares import staticMiddlewares

from myConfig import loggingConfig

sys.path.append('c:\\users\\ntien\\appdata\\local\\programs\\python\\python312\\lib\\site-packages')
sys.path.append('c:\\users\\ntien\\appdata\\Roaming\\python\\python312\\site-packages')

if not os.path.exists("static"):
    os.makedirs("static")

app = FastAPI()
# app.include_router(idCard.router)
# app.include_router(document.router)
app.include_router(hos_invoice.router)

corsMiddlewares.add(app)
staticMiddlewares.add(app)

@app.get("/")
def root():
    return {"hello world": "xin chào"}

if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
