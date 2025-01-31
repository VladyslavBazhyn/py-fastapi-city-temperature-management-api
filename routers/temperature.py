from fastapi import Depends, APIRouter, Query
from sqlalchemy.orm import Session

from temperature import schemas as temp_schemas
from temperature import crud as temp_crud
from db.engine import get_db

router = APIRouter()


@router.post("/update/", response_model=temp_schemas.TemperatureUpdate)
def update_temperature(db: Session = Depends(get_db)):
    return temp_crud.temperature_update_all(db=db)


@router.get("/", response_model=list[temp_schemas.TemperatureResponse])
def get_temperatures(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    return temp_crud.get_temperatures(db=db, skip=skip, limit=limit)
