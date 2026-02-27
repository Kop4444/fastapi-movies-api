from sqlalchemy import Column, Integer, String, Float
from database import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    year = Column(Integer)
    rating = Column(Float, nullable=True)
    
    # Для книг (если хотите добавить)
    # book = Column(String)
    # price = Column(Float)
    # author = Column(String, nullable=True)