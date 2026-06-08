from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator
import re
from typing import Literal


class UserBase(BaseModel):
    username: str = Field(min_length=1)
    email: EmailStr

    @field_validator("username")
    @classmethod
    def validate_username(cls, val: str):
        if not re.fullmatch(r"[a-zA-Z0-9]+", val):
            raise ValueError(
                "Username can contains only alphabets and digits no special characters"
            )
        return val


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=500)

    @field_validator("password")
    @classmethod
    def validate_password(cls, val: str):
        if not any(char.isdigit() for char in val):
            raise ValueError("Password must contain one digit")
        if not any(char.isupper() for char in val):
            raise ValueError("Password must contain uppercase letter")
        return val


class UserCreateResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class LoginResponse(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    token: str
    type: Literal["bearer"] = "bearer"


class UserUpdate(UserBase):
    pass


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class AdminUserResponse(UserResponse):
    is_admin: bool
    is_active: bool
