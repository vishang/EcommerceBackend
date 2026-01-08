from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import create_access_token
from app.constants.roles import CUSTOMER, RETAILER
from app.models.role import Role
from app.models.user import User
from app.schemas.user import UserRead

router = APIRouter(prefix="/auth")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class RegisterRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    mobile_number: str
    password: str
    type: str


@router.post("/register", response_model=UserRead, status_code=201)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    if payload.type not in {CUSTOMER, RETAILER}:
        raise HTTPException(status_code=400, detail="Invalid role type")

    role = db.query(Role).filter(Role.name == payload.type).first()
    if not role:
        raise HTTPException(status_code=400, detail="Invalid role")

    user = User(
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        mobile_number=payload.mobile_number,
        password=payload.password,
        role_id=role.id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or user.password != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.role:
        raise HTTPException(status_code=400, detail="User has no role assigned")

    token = create_access_token(
        {"id": user.id, "email": user.email, "role": user.role.name}
    )
    return TokenResponse(access_token=token)


@router.post("/logout")
def logout():
    return {"detail": "Logged out"}
