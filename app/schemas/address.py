from typing import Optional

from pydantic import BaseModel, ConfigDict


class AddressBase(BaseModel):
    line1: str
    line2: Optional[str] = None
    suburb: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    pincode: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class AddressCreate(AddressBase):
    pass


class AddressCreateRequired(BaseModel):
    line1: str
    line2: Optional[str] = None
    suburb: str
    city: str
    state: str
    country: str
    pincode: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class AddressRead(AddressBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
