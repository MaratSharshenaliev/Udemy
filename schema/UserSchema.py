import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, validator, constr


class User(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    hashed_password: str
    created_at: datetime.datetime
    is_mentor: bool = False
    is_superuser: bool = False
    avatar: str
    type: str

    firstname: str
    lastname: str
    audience: int = 1


class UserIn(BaseModel):
    email: EmailStr
    firstname: str
    lastname: str = " "
    password: constr(min_length=8)
    password2: str
    is_mentor: bool = False
    audience: int = 0

    @validator('firstname')
    def first_name(cls, v):
        if ' ' not in v and not len(v):
            raise ValueError("firs name is not valid")
        return v.title()

    @validator('lastname')
    def last_name(cls, v):
        if not len(v):
            raise ValueError('lastname is not valid')
        return v

    @validator("password2")
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values["password"]:
            raise ValueError("Пароли не совпадают")
        return v

