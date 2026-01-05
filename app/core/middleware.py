from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from app.core.security import decode_token

PUBLIC_PATHS = {
    "/",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/favicon.ico",
    "/api/v1/auth/login",
    "/api/v1/auth/register",
}

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        
        path = request.url.path
        
        if path in PUBLIC_PATHS:
            return await call_next(request)
        
        if request.url.path.endswith("/login"):
            return await call_next(request)
        
        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(status_code=401, detail="Missing Token")
        
        payload = decode_token(token.replace("Bearer ", ""))
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid Token")
        
        request.state.user = payload
        return await call_next(request)