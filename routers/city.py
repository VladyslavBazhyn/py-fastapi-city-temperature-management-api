from city_crud import schemas as city_schemas
from city_crud import crud as city_crud
from db.engine import get_db


from fastapi import Depends, Query, HTTPException, APIRouter

from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", response_model=city_schemas.CityCreate)
def create_city(city_create: city_schemas.CityCreate, db: Session = Depends(get_db)):
    return city_crud.create_city(db=db, city=city_create)


@router.get("/", response_model=list[city_schemas.CityResponse])
def get_cities(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    return city_crud.get_cities(db=db, skip=skip, limit=limit)


@router.get("/{city_id}/", response_model=city_schemas.CityResponse)
def get_city(city_id: int, db: Session = Depends(get_db)):
    return city_crud.get_city(db=db, city_id=city_id)


@router.put("/{city_id}/", response_model=city_schemas.CityResponse)
def update_city(city_id: int, updated_city: city_schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = city_crud.update_city(db=db, city_id=city_id, updated_city=updated_city)

    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.delete("/{city_id}/")
def delete_city(city_delete_id: int, db: Session = Depends(get_db)):
    deleted_city = city_crud.delete_city(db=db, city_id=city_delete_id)
    if not deleted_city:
        raise HTTPException(status_code=404, detail=f"City with id {city_delete_id} not found")
    return deleted_city
