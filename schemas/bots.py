from pydantic import BaseModel


class BotsCreate(BaseModel):
    login: str
    password: str
    owner_id: int
    social_network_id: int

class BotsView(BaseModel):
    id: int
    login: str
    password: str
    owner_id: int
    social_network_id: int
    is_active: bool

    class Config:
        from_attributes = True

class BotsUpdate(BaseModel):
    login: str
    password: str
    is_active: bool
