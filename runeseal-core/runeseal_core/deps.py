import os

from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

bearer_scheme = HTTPBearer(auto_error=False)


def admin_or_api_key(
    x_api_key: str = Header(None),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    # Prefer JWT if present
    if credentials:
        secret = os.getenv("JWT_SECRET")
        if not secret:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="JWT secret not configured",
            )
        try:
            payload = jwt.decode(credentials.credentials, secret, algorithms=["HS256"])
            if payload.get("is_admin"):
                return True
        except JWTError:
            pass
    # Fallback to API key
    expected_key = os.getenv("X_API_KEY")
    if x_api_key and x_api_key == expected_key:
        return True
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
