from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.geocoding import geocode_address
from app.constants.roles import RETAILER
from app.models.address import Address
from app.models.store import Store
from app.schemas.store import StoreCreateForOwner, StoreRead

router = APIRouter(prefix="/stores")


@router.post("/", response_model=StoreRead, status_code=201)
def create_store(
    request: Request,
    payload: StoreCreateForOwner,
    db: Session = Depends(get_db),
):
    user = request.state.user
    if user.get("role") != RETAILER:
        raise HTTPException(status_code=403, detail="Access Denied")

    owner_id = user.get("id")
    if owner_id is None:
        raise HTTPException(status_code=400, detail="Invalid user payload")

    address = Address(
        line1=payload.address.line1,
        line2=payload.address.line2,
        suburb=payload.address.suburb,
        city=payload.address.city,
        state=payload.address.state,
        country=payload.address.country,
        pincode=payload.address.pincode,
        latitude=payload.address.latitude,
        longitude=payload.address.longitude,
    )

    if address.latitude is None or address.longitude is None:
        coords = geocode_address(
            line1=address.line1,
            line2=address.line2,
            suburb=address.suburb,
            city=address.city,
            state=address.state,
            country=address.country,
            pincode=address.pincode,
        )
        if not coords:
            raise HTTPException(status_code=400, detail="Unable to geocode address")
        address.latitude, address.longitude = coords

    db.add(address)
    db.flush()

    store = Store(
        name=payload.name,
        owner_id=owner_id,
        address_id=address.id,
    )
    db.add(store)
    db.commit()
    db.refresh(store)
    return store
