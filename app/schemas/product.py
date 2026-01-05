from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: str
    description: str
    height: float
    width: float
    length: float


class ProductCreate(ProductBase):
    pass


class ProductCreateForStore(ProductCreate):
    store_id: int
    stock: int = 0
    price: float


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    height: float | None = None
    width: float | None = None
    length: float | None = None


class ProductRead(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
