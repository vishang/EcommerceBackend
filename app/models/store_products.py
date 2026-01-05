from sqlalchemy import Integer, Column, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class StoreProduct(Base):
    
    __tablename__ = "store_products"
    
    store_id = Column(Integer, ForeignKey("stores.id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    stock = Column(Integer, nullable=False, default=0)
    price = Column(Float, nullable=False)
    
    store = relationship("Store", backref="store_products")
    product = relationship("Product", backref="store_products")