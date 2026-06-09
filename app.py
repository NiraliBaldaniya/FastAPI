from fastapi import FastAPI
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
    return {
        "long_url": url.get(code)
    }