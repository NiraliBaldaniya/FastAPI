from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
import string
import random
import qrcode
import base64
import os
import json
from io import BytesIO


app = FastAPI()

try:
    with open("data.json", "r") as file:
        url = json.load(file)
except:
    url = {}

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>URL Shortener</title>
        <style>
            body{
                font-family: Arial, sans-serif;
                background: #f4f4f4;
                text-align: center;
                margin-top:100px;
            }

            .box{
                background:white;
                width:500px;
                margin:auto;
                padding:30px;
                border-radius:10px;
                box-shadow:0 0 10px rgba(0,0,0,0.2);
            }

            input{
                width:80%;
                padding:10px;
                margin:10px;
            }

            button{
                padding:10px 20px;
                background:#007bff;
                color:white;
                border:none;
                border-radius:5px;
                cursor:pointer;
            }
        </style>
    </head>
    <body>
        <div class="box">
            <h1>URL Shortener</h1>

            <form action="/generate" method="get">
                <input type="text" name="long_url" placeholder="Enter URL" required>
                <br>
                <button type="submit">Shorten URL</button>
            </form>
        </div>
    </body>
    </html>
    """


@app.get("/generate", response_class=HTMLResponse)
def shortner(long_url: str):

    if "." not in long_url:
        long_url += ".com"
    if not long_url.startswith(("http://", "https://")):
        long_url = "https://" + long_url
    code = ''.join(
        random.choices(
            string.ascii_letters + string.digits,
            k=7
        )
   )

    url[code] = long_url

    with open("data.json", "w") as file:
        json.dump(url, file, indent=4)

    BASE_URL = "http://127.0.0.1:8000"
    short_url = f"{BASE_URL}/{code}"

    qr = qrcode.make(short_url)

    buffer = BytesIO()
    qr.save(buffer, format="PNG")

    img_base64 = base64.b64encode(buffer.getvalue()).decode()

    return f"""
    <html>
   
    <body style="font-family:Arial;text-align:center;margin-top:100px;">
    <h3>QR Code</h3>

    <img
    src="data:image/png;base64,{img_base64}"
    width="200"
    >
    <h1>URL Generated Successfully!</h1>

    <p><b>Original URL:</b></p>
    <p>{long_url}</p>

    <p><b>Short URL:</b></p>
    <a href="{short_url}" target="_blank">
        {short_url}
    </a>

    <br><br>

    <a href="/">
        <button>Generate Another</button>
    </a>
    <input type="text" value="{short_url}" id="shortUrl" readonly style= "width:350px; padding:10px;">

    <button onclick="copyUrl()"> Copy </button>

<script>
function copyUrl() {{
    let copyText = document.getElementById("shortUrl");
    navigator.clipboard.writeText(copyText.value);
    alert("Copied!");
}}
</script>
</body>
</html>
"""

@app.get("/{code}")
def get_url(code: str):
    long_url = url.get(code)

    if long_url:
        return RedirectResponse(long_url)

    return {"error": "Invalid code"}