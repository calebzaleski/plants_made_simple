from pydantic import BaseModel
from datetime import date
from typing import Optional

class UserCreate(BaseModel):
    username: str
    nickname: str
    firstname: str
    lastname: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class GetImg(BaseModel):
    username: str
    plant_number: int


class GetUser(BaseModel):
    username: str

class PlantCreate(BaseModel):
    username: str
    plant_name: str
    scientific_name: str
    age: int  # years
    image_url: str
    health: str
    notes: str
    # Care Needs
    light_needs: str
    fertilizer_needs: str
    # Dates
    date_acquired: Optional[date] = None
    date_last_water: Optional[date] = None
    date_next_water: Optional[date] = None
    date_last_pot: Optional[date] = None
    date_next_pot: Optional[date] = None

