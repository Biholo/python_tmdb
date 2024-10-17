from sqlalchemy import Column, Integer, String
from ..services.database import Base

class Actor(Base):
    __tablename__ = 'actor'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    birth_date = Column(String(50), nullable=True)
