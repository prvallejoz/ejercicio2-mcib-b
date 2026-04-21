from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()

templates = Jinja2Templates(directory="templates")

API_KEY = "992451dc"
BASE_URL = "http://www.omdbapi.com/"

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "request": request
        }
    )

@app.post("/buscar")
def buscar(request: Request, titulo: str = Form(...)):
    params = {
        "apikey": API_KEY,
        "s": titulo
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "request": request,
            "peliculas": data.get("Search", [])
        }
    )

@app.get("/detalle/{imdb_id}")
def detalle(request: Request, imdb_id: str):
    params = {
        "apikey": API_KEY,
        "i": imdb_id,
        "plot": "full"
    }

    response = requests.get(BASE_URL, params=params)
    pelicula = response.json()
    print(pelicula)

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "request": request,
            "detalle": pelicula
        }
    )