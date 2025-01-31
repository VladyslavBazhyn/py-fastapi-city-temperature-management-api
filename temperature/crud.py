from datetime import datetime

import requests
import os
from dotenv import load_dotenv

from fastapi import HTTPException, Depends, Query

from sqlalchemy.orm import Session

from db.engine import get_db
from temperature import models
from city_crud.models import City

load_dotenv()

WEATHER_API_URL = os.environ.get("WEATHER_API_URL")
API_KEY = os.environ.get("API_KEY")


def temperature_create(
    city_id: int,
    date_time: datetime,
    temperature: int,
    db: Session
):
    db_temperature = models.Temperature(
        city_id=city_id,
        date_time=date_time,
        temperature=temperature
    )

    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)

    return db_temperature


def get_temperature(city_id: int, db: Session):
    db_temperature = db.query(
        models.Temperature
    ).filter_by(city_id=city_id).first()

    if db_temperature is None:
        return None

    return db_temperature


def get_temperatures(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    return db.query(models.Temperature).offset(skip).limit(limit).all()


def temperature_update_all(db: Session):

    cities = db.query(City).all()

    for city in cities:

        try:
            response = requests.get(
                WEATHER_API_URL, params={"key": API_KEY, "q": city.name}
            )
            response.raise_for_status()

            data = response.json()

            temperature_to_update = round(data.get("current").get("temp_c"))
            print(temperature_to_update)
            datetime_to_update = datetime.strptime(
                data.get("location").get("localtime"), "%Y-%m-%d %H:%M"
            )
            print(datetime_to_update)

            if temperature_to_update is None or datetime_to_update is None:
                continue

            db_temperature = get_temperature(city_id=city.id, db=db)

            if db_temperature:
                db_temperature.temperature = temperature_to_update
                db_temperature.date_time = datetime_to_update
            else:
                print("This city don't have a temperature yet.")
                db_temperature = temperature_create(
                    db=db,
                    city_id=city.id,
                    temperature=temperature_to_update,
                    date_time=datetime_to_update
                )
                print("Temperature fot this city have been created.")

            db.commit()
            db.refresh(db_temperature)

            return db_temperature

        except Exception as e:

            print(f"Error updating temperature for {city.name}: {e}")
