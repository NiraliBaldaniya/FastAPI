from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
import string
import random
import qrcode
import base64
import os
import json
from io import BytesIO
from datetime import datetime


app = FastAPI()

try:
    with open("data.json", "r") as file:
        url = json.load(file)
except:
    url = {}

def render_home(short_url=None):
    result_html = ""

    if short_url:
        result_html = f"""
        <div class="result">
            <div class="url-info">
                <h2 style="color:#16a34a;">Your short URL</h2>
                <a href="{short_url}" target="_blank" style="color:white ;font-size: 20px;padding: 7px; text-decoration: none;">
                {short_url}
                </a>
            </div>
                <button class="copy-btn" onclick="navigator.clipboard.writeText('{short_url}')">
                Copy
                </button>
            </div>
            """
    else:
        result_html = f"""
        <div class="result">
            <div class="url-info">
                <h2 style="color:#16a34a;">Your short URL</h2>
                <a href="{short_url}" target="_blank">
                    {short_url}
                </a>
            </div>
            <button class="copy-btn" onclick="navigator.clipboard.writeText('{short_url}')">
                Copy
            </button>
        </div>
        """
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>URL Shortener</title>
        <style>
             body {{
                margin: 0;
                font-family: Arial, sans-serif;
                background: linear-gradient(to right, #0b1a6a, #0f2a5f, #3b1b75);
                color: white;
            }}

            .navbar {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 15px 40px;
                background: rgba(0.5, 0.3, 1, 0.3);
            }}

            .nav-links a {{
                color: white;
                text-decoration: none;
                margin-left: 20px;
                font-size: 20px;
            }}

            .nav-links a:hover {{
                color: #470bbe;
            }}

            .logo{{
            font-size: 40px;
            font-weight: bold;
            }}
             
            h1 {{
                text-align: center;
                margin-top: 100px;
            }}
            p{{
                text-align: center;
                font-size: 20px;
                color: #94909c;
            }}

            .box {{
                width: 100%;
                height: 180px;
                max-width: 700px;
                margin: 40px auto;
                background: rgba(255, 255, 255, 0.08);
                padding: 20px;
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}

             .input-box {{
                display: flex;
                flex-direction: column;
                background: rgba(255, 255, 255, 0.1);
                padding: 14px;
                margin-top: 10px;
                border-radius: 8px;
            }}

            .input-box input {{
                width: 100%;
                border: none;
                outline: none;
                background: transparent;
                color: white;
                font-size: 18px;
            }}

            h2{{
                padding: 10px;
                margin: 0px;
                font-size: 20px;
            }}

            button{{
                padding: 20px 30px;
                margin-top: 10px;
                background:#007bff;
                color:white;
                border:none;
                border-radius:5px;
                cursor:pointer;
            }}

            .btn {{
                width: 100%;
                margin-top: 15px;
                padding: 14px;
                border: none;
                border-radius: 8px;
                background: linear-gradient(to right, #3b82f6, #8b5cf6);
                color: white;
                font-size: 20px;
                cursor: pointer;
            }}
             .result {{
                width: 100%;
                max-width: 700px;
                margin: 20px auto;
                background: rgba(0, 255, 100, 0.15);
                border: 1px solid #22c55e;
                padding: 20px;
                border-radius: 10px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            .copy-btn {{
                background: #22c55e;
                border: none;
                padding: 10px 25px 10px 30px;
                border-radius: 6px;
                cursor: pointer;
                color: white;
                font-size: 20px;
            }}

            .copy-btn:hover {{
                background: #16a34a;
            }}

            .url-info {{
                display: flex;
                flex-direction: column;
            }}
            
        </style>
    </head>
    <body>
        <div class="navbar">
        <div class="logo">🔗 URL Shortener</div>
        <div class="nav-links">
           <a href="#">Home</a>
           <a href="/all">My Links</a>
           <a href="#">About</a>
        </div>
        </div>
            <h1>URL Shortener</h1>
            <p>enter long url to generate short url</p>
        <div class="box">
            <h2>Enter Long URL</h2>
            <form action="/generate" method="get">
            <div class="input-box">
            
                <input type="text" name="long_url" placeholder="https://www.example.com" required>
                </div>
                <button type="submit" class="btn">🔗 Shorten URL</button>
            </form>
        </div>
        
        {result_html}
    </body>
    </html>
    """


@app.get("/", response_class=HTMLResponse)
def home():
    return render_home()

@app.get("/generate", response_class=HTMLResponse)
def shortner(long_url: str):

    if "." not in long_url:
        long_url += ".com"
    if not long_url.startswith(("http://", "https://")):
        long_url = "https://" + long_url
    code = ''.join(
        random.choices(
            string.ascii_letters + string.digits,
            k=4
        )
   )

    url[code] = {
        "long_url": long_url,
        "created_at": datetime.now().strftime("%d-%m-%y %H:%M:%S")
    }

    with open("data.json", "w") as file:
        json.dump(url, file, indent=4)

    BASE_URL = "http://127.0.0.1:8000"
    short_url = f"{BASE_URL}/{code}"

   # qr = qrcode.make(short_url)

   # buffer = BytesIO()
   # qr.save(buffer, format="PNG")

   # img_base64 = base64.b64encode(buffer.getvalue()).decode()

    return render_home(short_url=short_url)
    
@app.get("/all", response_class=HTMLResponse)
def all_links():

    rows = ""

    for i, (code, data) in enumerate(url.items(), start=1):
        short_url = f"http://127.0.0.1:8000/{code}"
        long_url = data["long_url"]
        created_at = data["created_at"]

        rows += f"""
        <tr>
            <td>{i}</td>
            <td>{long_url}</td>
            <td>
                <a href="{short_url}" target="_blank">
                    {short_url}
                </a>
            </td>
            <td>{created_at}</td>
            <td class="delete">
                <a href="/delete/{code}">delete</a>
            </td>
        </tr>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>My Links</title>

        <style>
            body {{
                font-family: Arial;
                background: #f5f5f5;
                padding: 0px;
                margin: 0px;
            }}

            .top-bar {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin : 20px 20px;
                padding: 0px 10px;
            }}
             .new-btn {{
                padding: 20px 30px;
                background: #7c3aed;
                color: white;
                border: none;
                cursor: pointer;
                border-radius: 10px;
                display: flex;
                align-items: center;
                gap: 8px;
                text-decoration: none;
                font-size: 20px;
            }}

             .new-btn:hover {{
                background: #5c12d3;
            }}
            h1 {{
                
                margin-bottom: 50px;
                font-size: 40px;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                background: white;
                padding: 20px;
            }}

            th, td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }}

            th {{
                background: #7c3aed;
                color: white;
                font-size: 18px;
            }}

            .delete a {{
                color: black; 
                text-decoration: none;
                font-weight: bold;
                font-size: 18px;
            }}


            .navbar {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 15px 40px;
                margin-top: 0px; 
                color: white;
                background: linear-gradient(to right,#091B43,#101B45);
            
            }}

            .nav-links a {{
                color: white;
                text-decoration: none;
                margin-left: 20px;
                font-size: 20px;
            }}

            .nav-links a:hover {{
                color: #470bbe;
            }}

            .logo{{
            font-size: 40px;
            font-weight: bold;
            }}
             
            
        </style>

    </head>
    <body>
        <div class="navbar">
            <div class="logo">🔗 URL Shortener</div>

                <div class="nav-links">
                <a href="/">Home</a>
                <a href="/all">My Links</a>
                <a href="#">About</a>
            </div>
        </div>
        <div class="top-bar">
            <h1>My Links</h1>
            <a href="/" style="text-decoration: none;">
                <button class="new-btn">
                    <img src="https://img.icons8.com/ios-glyphs/30/ffffff/plus-math.png"/>
                    New Shorten URL
                </button>
            </a>
        </div>
        <table>
            <tr>
                <th>#</th>
                <th>Original URL</th>
                <th>Short URL</th>
                <th>created at</th>
                <th>Action</th>
            </tr>

            {rows}
            
        </table>

    </body>
    </html>
    """   
@app.get("/delete/{code}")
def delete_link(code: str):
    if code in url:
        del url[code]

        with open("data.json", "w") as file:
            json.dump(url, file, indent=4)

    return RedirectResponse("/all", status_code=303)

@app.get("/{code}")
def redirect(code: str):
    data = url.get(code)

    if data:
        return RedirectResponse(data["long_url"])

    return {"error": "Invalid code"}
