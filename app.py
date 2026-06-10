from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import string
import random

url = {}
app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "url shortner"
    }

@app.get("/generate")
def shortner(long_url: str):
    code = ''.join(
        random.choices(
            string.ascii_letters + string.digits,
            k=6
        )
    )

    url[code] = long_url

    return {
        "short_code": code,
        "long_url": long_url
    }

@app.get("/{code}")
def get_url(code: str):
    long_url= url.get(code)
   
    if long_url:
        return RedirectResponse(long_url)

    return {"error": "Invalid code"}