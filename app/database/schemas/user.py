from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserSchema(UserBase):
    class Config:
        orm_mode = True
