from typing import Optional

from pydantic import BaseModel, EmailStr, conint, constr


# №9.1

class ProductBase(BaseModel):
    title: str
    price: float
    count: int


class ProductCreate(ProductBase):
    description: str = ""


class ProductOut(ProductBase):
    id: int
    description: str

    model_config = {"from_attributes": True}


# №10.1

class ErrorResponse(BaseModel):
    error_code: int
    message: str
    detail: Optional[str] = None


# №10.2

class UserValidation(BaseModel):
    username: str
    age: conint(gt=18)
    email: EmailStr
    password: constr(min_length=8, max_length=16)
    phone: Optional[str] = "Unknown"


# №11.1 / №11.2

class UserIn(BaseModel):
    username: str
    age: int


class UserOut(BaseModel):
    id: int
    username: str
    age: int
