from datetime import datetime

from pydantic import BaseModel, ConfigDict
from app.schemas.address import AddressCreateRequired, AddressRead
from app.schemas.user import UserRead


class StoreBase(BaseModel):
    name: str
    owner_id: int
    address_id: int


class StoreCreate(StoreBase):
    pass


class StoreCreateForOwner(BaseModel):
    name: str
    address: AddressCreateRequired


class StoreRead(StoreBase):
    id: int
    create_at: datetime | None = None
    owner: UserRead | None = None
    address: AddressRead | None = None

    model_config = ConfigDict(from_attributes=True)
