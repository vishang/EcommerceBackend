from fastapi import APIRouter
from app.api.v1 import products

router = APIRouter(prefix="/api/v1")

router.include_router(products.router, tags=["Products"])