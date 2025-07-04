import os

from fastapi import Header, HTTPException, status


def verify_api_key(x_api_key: str = Header(None)):
    expected = os.getenv("X_API_KEY")
    if not x_api_key or x_api_key != expected:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or missing X-API-KEY"
        )
