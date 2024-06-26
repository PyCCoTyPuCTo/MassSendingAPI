from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserView(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True
