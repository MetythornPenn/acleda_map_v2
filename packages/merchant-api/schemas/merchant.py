from datetime import date
from typing import Optional

from pydantic import BaseModel
from pydantic import root_validator


class CreateMerchant(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float



class UpdateMerchant(CreateMerchant):
    pass

class ShowMerchant(BaseModel):
    id: int
    name: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    class Config:
        orm_mode = True
        
        
class ShowMerchantWithLatLong(BaseModel):
    id: int
    name: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    class Config:
        orm_mode = True