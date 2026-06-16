from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from db import sessionlocal, engine
from models import Url,base
import string
import random
from datetime import datetime


base.metadata.create_all(bind=engine)


app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "home.html",{ "request":request, "short_url":None }
    )

@app.get("/generate", response_class=HTMLResponse)
def shortner(request: Request, long_url: str):

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

    db = sessionlocal()

    new_url = Url(
        long_url=long_url,
        code=code,
        created_at=datetime.now().strftime("%d-%m-%y %H:%M:%S"),
        clicks=0
    )

    db.add(new_url)
    db.commit()
    db.close()
    short_url = f"http://127.0.0.1:8000/{code}"
    return templates.TemplateResponse(
        "home.html",{ "request": request, "short_url": short_url }
    )
    
@app.get("/all", response_class=HTMLResponse)
def all_links(request: Request):

    db = sessionlocal()
    all_urls = db.query(Url).all()
    db.close()

    return templates.TemplateResponse(
        "all_links.html",
        { "request": request, "all_urls": all_urls }
    )
  
@app.get("/delete/{code}")
def delete_link(code: str):
    db = sessionlocal()

    data = db.query(Url).filter(Url.code == code).first()

    if data:
        db.delete(data)
        db.commit()

    db.close()

    return RedirectResponse("/all", status_code=303)

@app.get("/{code}")
def redirect(code: str):
    
    db = sessionlocal()
    data = db.query(Url).filter(Url.code == code).first()

    if data:
        data.clicks = data.clicks + 1
        db.commit()

        long_url = data.long_url
        db.close()

        return RedirectResponse(long_url)
    
    db.close()

    return {"error": "Invalid code"}
