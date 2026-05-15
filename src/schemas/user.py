from pydantic import BaseModel, ConfigDict, EmailStr, field_validator
from typing import Optional
import re

class UserBase(BaseModel):
    username: str
    email: EmailStr

    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Username must be alphanumeric')
        return v

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    is_staff: bool

    model_config = ConfigDict(from_attributes=True)
