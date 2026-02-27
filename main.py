from fastapi import FastAPI, Query
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

@app.get('/')
async def home():
    return {'Hello!': 'API работает'}

@app.get('/current-time')
async def get_current_time():
    return {'current_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

movies = {
    "inception": {"title": "Inception", "year": 2010, "rating": 8.8},
    "matrix": {"title": "The Matrix", "year": 1999, "rating": 8.7}
}

@app.get('/movie/{name}')
async def get_movie(name: str):
    if name.lower() in movies:
        return movies[name.lower()]
    return {"error": "Movie not found"}

class Movie(BaseModel):
    title: str
    year: int
    rating: Optional[float] = None

@app.post('/movie/{name}')
async def create_movie(name: str, movie: Movie):
    movies[name.lower()] = movie
    return {name: movies[name.lower()]}

class UpdateMovie(BaseModel):
    title: Optional[str] = None
    year: Optional[int] = None
    rating: Optional[float] = None

@app.put('/movie/{name}')
async def update_movie(name: str, movie: UpdateMovie):
    if name.lower() not in movies:
        return {"error": "Movie not found"}
    if movie.title:
        movies[name.lower()].title = movie.title
    if movie.year:
        movies[name.lower()].year = movie.year
    if movie.rating:
        movies[name.lower()].rating = movie.rating
    return {name: movies[name.lower()]}

@app.delete('/movie')
async def delete_movie(name: str = Query(..., description="Movie name")):
    if name.lower() not in movies:
        return {"error": "Movie not found"}
    del movies[name.lower()]
    return {"message": "Movie deleted"}