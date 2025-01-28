from city_crud import crud
from city_crud import schemas
from db.engine import get_db

from city_crud.models import create_db_and_tables

from fastapi import FastAPI, Depends, Query, HTTPException

from sqlalchemy.orm import Session

app = FastAPI()

# Create database tables
create_db_and_tables()


@app.post("/cities/", response_model=schemas.CityCreate)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    return crud.create_city(db=db, city=city)


@app.get("/cities/", response_model=list[schemas.CityResponse])
def get_cities(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    return crud.get_cities(db=db, skip=skip, limit=limit)


@app.get("/cities/{city_id}/", response_model=schemas.CityResponse)
def get_city(db: Session, city_id: int):
    return crud.get_city(db=db, city_id=city_id)


@app.put("/cities/{city_id}/", response_model=schemas.CityResponse)
def update_city(db: Session, city_id: int, updated_city: schemas.CityCreate):
    db_city = crud.update_city(db=db, city_id=city_id, updated_city=updated_city)

    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@app.delete("/cities/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    deleted_city = crud.delete_city(db=db, city_id=city_id)
    if not deleted_city:
        raise HTTPException(status_code=404, detail=f"City with id {city_id} not found")
    return deleted_city
