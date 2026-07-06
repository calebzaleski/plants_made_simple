from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional, List

class UserCreate(BaseModel):
    username: str
    nickname: Optional[str] = None
    firstname: str
    lastname: str
    password: str
    email: str

class UserLogin(BaseModel):
    username: str
    password: str

class Image(BaseModel):
    username: str
    plant_number: int

class GetUser(BaseModel):
    username: str

class PlantCreate(BaseModel):
    plant_name: str
    scientific_name: str
    age: int  # years
    image_url: Optional[str] = None
    health: Optional[str] = None
    notes: Optional[str] = None
    # Care Needs
    light_needs: Optional[str] = None
    fertilizer_needs: Optional[str] = None
    # Dates
    date_acquired: Optional[date] = None
    date_last_water: Optional[date] = None
    date_next_water: Optional[date] = None
    date_last_pot: Optional[date] = None
    pot_frequency: Optional[int] = None
    date_next_pot: Optional[date] = None
    water_frequency: Optional[int] = None
    date_last_fertilized: Optional[date] = None
    fertilizer_frequency: Optional[int] = None
    date_next_fertilized: Optional[date] = None

class PlantUpdate(BaseModel):
    plant_name: Optional[str] = None
    scientific_name: Optional[str] = None
    age: Optional[int] = None
    image_url: Optional[str] = None
    health: Optional[str] = None
    notes: Optional[str] = None
    light_needs: Optional[str] = None
    fertilizer_needs: Optional[str] = None
    date_acquired: Optional[date] = None
    date_last_water: Optional[date] = None
    date_next_water: Optional[date] = None
    water_frequency: Optional[int] = None
    date_last_pot: Optional[date] = None
    pot_frequency: Optional[int] = None
    date_next_pot: Optional[date] = None
    date_last_fertilized: Optional[date] = None
    fertilizer_frequency: Optional[int] = None
    date_next_fertilized: Optional[date] = None

class UserUpdate(BaseModel):
    password: str
    username: Optional[str] = None
    nickname: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None

class PlantOut(BaseModel):
    success: Optional[bool] = None
    plant_id: Optional[int] = None
    plant_name: str
    scientific_name: str
    age: int  # years
    image_url: Optional[str] = None
    health: Optional[str] = None
    notes: Optional[str] = None
    light_needs: Optional[str] = None
    fertilizer_needs: Optional[str] = None
    date_acquired: Optional[date] = None
    date_last_water: Optional[date] = None
    date_next_water: Optional[date] = None
    date_last_pot: Optional[date] = None
    pot_frequency: Optional[int] = None
    date_next_pot: Optional[date] = None
    water_frequency: Optional[int] = None
    date_last_fertilized: Optional[date] = None
    fertilizer_frequency: Optional[int] = None
    date_next_fertilized: Optional[date] = None
    model_config = ConfigDict(from_attributes=True)
