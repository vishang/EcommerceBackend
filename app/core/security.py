from jose import jwt, JWTError
from app.core.config import settings
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None

def create_access_token(payload: dict):
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
