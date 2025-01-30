import temperature as temp
import city_crud as city
from db.engine import get_db, create_db_and_tables


from fastapi import FastAPI, Depends, Query, HTTPException

from sqlalchemy.orm import Session

app = FastAPI()

# Create database tables
create_db_and_tables()


@app.post("/cities/", response_model=city.schemas.CityCreate)
def create_city(city_create: city.schemas.CityCreate, db: Session = Depends(get_db)):
    return city.crud.create_city(db=db, city=city_create)


@app.get("/cities/", response_model=list[city.schemas.CityResponse])
def get_cities(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    return city.crud.get_cities(db=db, skip=skip, limit=limit)


@app.get("/cities/{city_id}/", response_model=city.schemas.CityResponse)
def get_city(db: Session, city_id: int):
    return city.crud.get_city(db=db, city_id=city_id)


@app.put("/cities/{city_id}/", response_model=city.schemas.CityResponse)
def update_city(db: Session, city_id: int, updated_city: city.schemas.CityCreate):
    db_city = city.crud.update_city(db=db, city_id=city_id, updated_city=updated_city)

    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@app.delete("/cities/{city_id}")
def delete_city(city_delete_id: int, db: Session = Depends(get_db)):
    deleted_city = city.crud.delete_city(db=db, city_id=city_delete_id)
    if not deleted_city:
        raise HTTPException(status_code=404, detail=f"City with id {city_delete_id} not found")
    return deleted_city


@app.post("/temperatures/update/", response_model=temp.schemas.TemperatureUpdate)
def update_temperature(db: Session = Depends(get_db)):
    return temp.crud.temperature_update(db=db)
