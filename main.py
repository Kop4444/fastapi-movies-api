from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

import models
import schemas
import crud
from database import SessionLocal, engine

# Создание таблиц в БД
models.Base.metadata.create_all(bind=engine)

# 1. СНАЧАЛА создаем app
app = FastAPI()

# 2. ПОТОМ настраиваем CORS (разрешаем запросы с фронтенда)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174", 
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Разрешаем все заголовки
)

# 3. Dependency для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 4. Корневой эндпойнт
@app.get("/")
async def root():
    return {"message": "Movie API with Database"}

# 5. Получить все фильмы
@app.get("/movies/", response_model=List[schemas.Movie])
def read_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    movies = crud.get_movies(db, skip=skip, limit=limit)
    return movies

# 6. Получить фильм по ID
@app.get("/movies/{movie_id}", response_model=schemas.Movie)
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie = crud.get_movie(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie

# 7. Поиск фильма по названию
@app.get("/movies/search/", response_model=schemas.Movie)
def search_movie(title: str = Query(...), db: Session = Depends(get_db)):
    db_movie = crud.get_movie_by_title(db, title=title)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie

# 8. Создать фильм
@app.post("/movies/", response_model=schemas.Movie)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    return crud.create_movie(db=db, movie=movie)

# 9. Обновить фильм
@app.put("/movies/{movie_id}", response_model=schemas.Movie)
def update_movie(movie_id: int, movie: schemas.MovieUpdate, db: Session = Depends(get_db)):
    db_movie = crud.update_movie(db=db, movie_id=movie_id, movie=movie)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie

# 10. Удалить фильм
@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie = crud.delete_movie(db=db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"message": "Movie deleted successfully"}

# 11. Текущее время (из предыдущей работы)
@app.get("/current-time")
async def get_current_time():
    return {'current_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}