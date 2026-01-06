from fastapi import APIRouter
from app.api.v1 import products, users

router = APIRouter(prefix="/api/v1")

router.include_router(products.router, tags=["Products"])
router.include_router(users.router, tags=["Auth"])
