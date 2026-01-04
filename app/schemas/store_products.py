from pydantic import BaseModel, ConfigDict


class StoreProductsBase(BaseModel):
    store_id: int
    product_id: int
    stock: int = 0
    price: float


class StoreProductsCreate(StoreProductsBase):
    pass


class StoreProductsRead(StoreProductsBase):
    model_config = ConfigDict(from_attributes=True)
