from pydantic import BaseModel

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
