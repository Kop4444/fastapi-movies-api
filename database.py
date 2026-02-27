from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Для PostgreSQL (раскомментируйте, если используете PostgreSQL)
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost/movies_db"

# Для SQLite (работает сразу без настройки)
SQLALCHEMY_DATABASE_URL = "sqlite:///./movies.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # только для SQLite
)

SessionLocal = sessionmaker(autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass