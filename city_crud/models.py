from typing import Optional

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, orm
from sqlmodel import SQLModel

from db import engine
from db.engine import Base


class City(Base):
    __tablename__ = "cities"

    id: int = Column(Integer, primary_key=True, index=True, )
    name: str = Column(String(128), unique=True, nullable=False, index=True)
    additional_info: Optional[str] = Column(String(255), unique=False, nullable=True)


def create_db_and_tables():
    Base.metadata.create_all(engine)
