from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.permissions import has_permission
from app.constants.roles import RETAILER
from app.constants.permissions import CAN_MANAGE_PRODUCTS
from app.models.product import Product
from app.models.store import Store
from app.models.store_products import StoreProduct
from app.schemas.product import ProductCreateForStore, ProductUpdate

router = APIRouter(prefix="/products")


@router.get('/')
def get_products(request: Request, db: Session = Depends(get_db)):
    user = request.state.user

    if user["role"] == RETAILER:
        user_id = user.get("id")
        if user_id is None:
            raise HTTPException(status_code=400, detail="Invalid user payload")
        products = (
            db.query(Product)
            .join(StoreProduct, StoreProduct.product_id == Product.id)
            .join(Store, Store.id == StoreProduct.store_id)
            .filter(Store.owner_id == user_id)
            .all()
        )
        return products

    products = db.query(Product).all()
    return products

@router.get("/{product_id}")
def get_product(product_id: int, request: Request, db: Session = Depends(get_db)):
    
    user = request.state.user
    
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product

@router.post("/")
def create_product(
    request: Request,
    product_in: ProductCreateForStore,
    db: Session = Depends(get_db),
):
    user = request.state.user
    
    if not has_permission(user["role"], CAN_MANAGE_PRODUCTS):
        raise HTTPException(status_code=403, detail="Access Denied")
    
    store = db.query(Store).filter(Store.id == product_in.store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")

    if user["role"] == RETAILER:
        user_id = user.get("id")
        if user_id is None:
            raise HTTPException(status_code=400, detail="Invalid user payload")
        if store.owner_id != user_id:
            raise HTTPException(status_code=403, detail="Access Denied")

    product = Product(
        name=product_in.name,
        description=product_in.description,
        height=product_in.height,
        width=product_in.width,
        length=product_in.length,
    )
    db.add(product)
    db.flush()

    store_product = StoreProduct(
        store_id=product_in.store_id,
        product_id=product.id,
        stock=product_in.stock,
        price=product_in.price,
    )
    db.add(store_product)
    db.commit()
    db.refresh(product)

    return product


@router.put("/{product_id}")
def update_product(
    product_id: int,
    request: Request,
    product_in: ProductUpdate,
    db: Session = Depends(get_db),
):
    user = request.state.user

    if not has_permission(user["role"], CAN_MANAGE_PRODUCTS):
        raise HTTPException(status_code=403, detail="Access Denied")

    if user["role"] == RETAILER:
        user_id = user.get("id")
        if user_id is None:
            raise HTTPException(status_code=400, detail="Invalid user payload")
        owner_link = (
            db.query(StoreProduct)
            .join(Store, Store.id == StoreProduct.store_id)
            .filter(StoreProduct.product_id == product_id)
            .filter(Store.owner_id == user_id)
            .first()
        )
        if not owner_link:
            raise HTTPException(status_code=403, detail="Access Denied")

    if user["role"] == RETAILER:
        user_id = user.get("id")
        if user_id is None:
            raise HTTPException(status_code=400, detail="Invalid user payload")
        product = (
            db.query(Product)
            .join(StoreProduct, StoreProduct.product_id == Product.id)
            .join(Store, Store.id == StoreProduct.store_id)
            .filter(Product.id == product_id)
            .filter(Store.owner_id == user_id)
            .first()
        )
    else:
        product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    updates = product_in.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product
