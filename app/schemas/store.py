from datetime import datetime

from pydantic import BaseModel, ConfigDict


class StoreBase(BaseModel):
    name: str
    owner_id: int
    address_id: int


class StoreCreate(StoreBase):
    pass


class StoreRead(StoreBase):
    id: int
    create_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
