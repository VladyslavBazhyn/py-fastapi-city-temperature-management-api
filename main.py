from city_crud import crud
from city_crud import schemas
from db.engine import Base, engine, get_db

from city_crud.models import create_db_and_tables

from fastapi import FastAPI, Depends, Query

from sqlalchemy.orm import Session

app = FastAPI()

# Create database tables
create_db_and_tables()
