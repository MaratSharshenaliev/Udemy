import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, validator, constr


class Reset_password(BaseModel):
    id: Optional[str] = None
    email: EmailStr
    reset_code: str
    status: str = "1"
    reset_code_created_at: datetime.datetime


class confirm(BaseModel):
    token: str
    password: constr(min_length=8)
    password2: str

    @validator("password2")
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values["password"]:
            raise ValueError("Пароли не совпадают")
        return v


class TemplateCorfirmSzhema(BaseModel):
    firstname: str
    url_confirm: str

