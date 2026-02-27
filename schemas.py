from pydantic import BaseModel
from typing import Optional

class MovieBase(BaseModel):
    title: str
    year: int
    rating: Optional[float] = None

class MovieCreate(MovieBase):
    pass

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    year: Optional[int] = None
    rating: Optional[float] = None

class Movie(MovieBase):
    id: int
    
    class Config:
        from_attributes = True