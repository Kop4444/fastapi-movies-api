from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

import models
import schemas
import crud
from database import SessionLocal, engine

# Импорт планировщика
from app.scheduler import lifespan

# Импорт состояния
from app.state import email_sending_enabled, set_email_status, get_email_status

# Создание таблиц в БД
models.Base.metadata.create_all(bind=engine)

# 1. СНАЧАЛА создаем app с lifespan
app = FastAPI(lifespan=lifespan)

# 2. ПОТОМ настраиваем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174", 
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    return {"message": "Movie API with Database and Scheduler"}

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

# 11. Текущее время
@app.get("/current-time")
async def get_current_time():
    return {'current_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

# ============= ЭНДПОЙНТЫ ДЛЯ УПРАВЛЕНИЯ ПОЧТОЙ =============

# Эндпойнт для включения отправки
@app.post("/email/enable")
async def enable_email():
    """Включить отправку отчетов на почту"""
    set_email_status(True)
    current_status = get_email_status()
    print(f"\n{'='*50}")
    print(f"✅ EMAIL SENDING ENABLED")
    print(f"   Текущий статус: {current_status}")
    print(f"{'='*50}\n")
    return {
        "status": "success", 
        "message": "✅ Email sending ENABLED",
        "current_status": "enabled"
    }

# Эндпойнт для отключения отправки
@app.post("/email/disable")
async def disable_email():
    """Отключить отправку отчетов на почту"""
    set_email_status(False)
    current_status = get_email_status()
    print(f"\n{'='*50}")
    print(f"❌ EMAIL SENDING DISABLED")
    print(f"   Текущий статус: {current_status}")
    print(f"{'='*50}\n")
    return {
        "status": "success", 
        "message": "❌ Email sending DISABLED",
        "current_status": "disabled"
    }

# Эндпойнт для проверки статуса
@app.get("/email/status")
async def email_status():
    """Проверить статус отправки отчетов"""
    current_status = get_email_status()
    status_text = "enabled" if current_status else "disabled"
    return {
        "email_sending_enabled": current_status,
        "status_text": status_text,
        "admin_email": "Yugrinkd@mail.ru",
        "next_run": "Every 5 minutes",
        "message": f"Email sending is {status_text}"
    }

# Эндпойнт для ручной отправки
@app.post("/email/send-now")
async def send_email_now():
    """Отправить отчет прямо сейчас"""
    from app.scheduler import send_movie_report_job
    import threading
    thread = threading.Thread(target=send_movie_report_job)
    thread.daemon = True
    thread.start()
    return {"message": "📧 Report is being sent to Yugrinkd@mail.ru"}

# Эндпойнт для проверки настроек почты
@app.get("/check-email")
async def check_email_settings():
    """Проверка настроек почты"""
    from app.email_service import email_service
    current_status = get_email_status()
    return {
        "admin_email": email_service.admin_email,
        "smtp_server": email_service.smtp_server,
        "smtp_port": email_service.smtp_port,
        "username": email_service.username,
        "from_email": email_service.from_email,
        "email_sending_enabled": current_status
    }