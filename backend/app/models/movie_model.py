# /app/models/movie_model.py

from sqlalchemy import Column, Integer, String
from ..services.database import Base
from sqlalchemy import Column, Integer, String, Float, Boolean

class Movie(Base):
    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True, autoincrement=False)
    original_title = Column(String(100), nullable=False)
    popularity = Column(Float, nullable=True)
    adult = Column(Boolean, nullable=False, default=False)
    video = Column(Boolean, nullable=False, default=False)

