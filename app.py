from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import requests
import sqlite3
import os
from dotenv import load_dotenv


load_dotenv()


app = FastAPI()

templates = Jinja2Templates(directory="templates")

API_KEY = os.getenv("OMDB_API_KEY")
BASE_URL = "http://www.omdbapi.com/"

#connect to the database and create the table if it doesn't exist
conn = sqlite3.connect("peliculas.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS peliculas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    year TEXT,
    director TEXT,
    actors TEXT,
    plot TEXT,
    rating TEXT,
    type TEXT,
    poster TEXT
)""")
conn.commit()
conn.close()    

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "request": request
        }
    )

#add route to show all movie titles in the database and show them in the index.html template with links to /detalle/{{ imdb_id }} to show the details of the movie
@app.get("/consultar_db")
def consultar_db(request: Request):
    conn = sqlite3.connect("peliculas.db")
    
    # ¡Agrega esta línea! Convierte los resultados en objetos similares a diccionarios
    conn.row_factory = sqlite3.Row 
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM peliculas")
    peliculas = cursor.fetchall()
    conn.close()

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "request": request,
            "peliculas_db": peliculas # Se envía como peliculas_db
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
    print(imdb_id)

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "request": request,
            "detalle": pelicula
        }
    )

@app.post("/guardar/{imdb_id}")
def guardar(request: Request, imdb_id: str):
    # 1. Obtenemos los datos de la película desde la API usando el ID
    params = {
        "apikey": API_KEY,
        "i": imdb_id,
        "plot": "full"
    }
    response = requests.get(BASE_URL, params=params)
    detalle = response.json()

    # 2. Guardamos en la base de datos usando .get() por seguridad
    conn = sqlite3.connect("peliculas.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO peliculas (title, year, director, actors, plot, rating, type, poster) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        detalle.get("Title"), 
        detalle.get("Year"), 
        detalle.get("Director"), 
        detalle.get("Actors"), 
        detalle.get("Plot"), 
        detalle.get("Rated"), 
        detalle.get("Type"), 
        detalle.get("Poster")
    ))
    conn.commit()
    conn.close()

    # 3. Retornamos la respuesta
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "request": request,
            "mensaje": "¡Película guardada en la base de datos exitosamente!"
        }
    )

@app.get("/detalle_db/{peli_id}")
def detalle_db(request: Request, peli_id: int):
    conn = sqlite3.connect("peliculas.db")
    conn.row_factory = sqlite3.Row  # Para acceder por nombre de columna
    cursor = conn.cursor()
    
    # Buscamos la película específica por su ID primario
    cursor.execute("SELECT * FROM peliculas WHERE id = ?", (peli_id,))
    pelicula = cursor.fetchone()
    conn.close()

    if pelicula is None:
        return {"error": "Película no encontrada"}

    return templates.TemplateResponse(
        request, 
        "index.html", 
        {
            "request": request, 
            "peli_db_detalle": pelicula
        }
    )

@app.get("/clear")
def limpiar_base_datos(request: Request):
    conn = sqlite3.connect("peliculas.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM peliculas")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='peliculas'") # Reinicia el contador de IDs
    conn.commit()
    conn.close()

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "request": request,
            "mensaje": "Base de datos vaciada correctamente."
        }
    )