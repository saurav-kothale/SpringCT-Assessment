from pydantic import BaseModel
from enum import Enum


class UserRegisterSchema(BaseModel):
    name : str
    email : str
    password : str

class UserLoginSchema(BaseModel):
    email : str
    password : str