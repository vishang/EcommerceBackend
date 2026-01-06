from fastapi import APIRouter, Depends
from app.api.v1 import products, users, stores
from app.core.security import oauth2_scheme

router = APIRouter(prefix="/api/v1")

router.include_router(
    products.router,
    tags=["Products"],
    dependencies=[Depends(oauth2_scheme)],
)
router.include_router(users.router, tags=["Auth"])
router.include_router(
    stores.router,
    tags=["Stores"],
    dependencies=[Depends(oauth2_scheme)],
)
