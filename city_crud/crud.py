from fastapi import HTTPException, Depends, Query

from city_crud import models, schemas

from sqlalchemy.orm import Session

from db.engine import get_db


def get_cities(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    return db.query(models.City).offset(skip).limit(limit).all()


def get_city(db: Session, city_id: int):
    city = db.query(models.City).filter_by(id=city_id).first()

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return city


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info
    )

    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def update_city(db: Session, city_id: int, updated_city: schemas.CityCreate):
    db_city = get_city(db=db, city_id=city_id)

    db_city.name = updated_city.name
    db_city.additional_info = updated_city.additional_info

    db.commit()
    db.refresh(db_city)

    return db_city


def delete_city(db: Session, city_id: int):
    db_city = get_city(db=db, city_id=city_id)

    db.delete(db_city)
    db.commit()

    return {"detail": f"City with id {city_id} has been deleted"}
