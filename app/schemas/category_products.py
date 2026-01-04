from pydantic import BaseModel, ConfigDict


class CategoryProductsBase(BaseModel):
    category_id: int
    product_id: int


class CategoryProductsCreate(CategoryProductsBase):
    pass


class CategoryProductsRead(CategoryProductsBase):
    model_config = ConfigDict(from_attributes=True)
