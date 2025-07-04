import os

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from passlib.hash import argon2
from pydantic import BaseModel
from runeseal_core import models
from runeseal_core.database import SessionLocal
from runeseal_core.security import oauth2_scheme
from sqlalchemy.orm import Session

router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Request body
class RegisterRequest(BaseModel):
    username: str
    password: str


# Request payload
class LoginRequest(BaseModel):
    username: str
    password: str


# Response payload
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    # api_key: str = None  # Optional: include X-API-Key in response


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == data.username).first()
    if not user or not argon2.verify(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    jwt_secret = os.getenv("JWT_SECRET", "changeme_this_is_dev_only")
    token = jwt.encode(
        {"sub": str(user.id), "is_admin": user.is_admin},  # <-- add is_admin
        jwt_secret,
        algorithm="HS256",
    )

    return TokenResponse(
        access_token=token,
        # api_key=os.getenv("X_API_KEY"),  # Optional header used elsewhere
    )


@router.post("/register", status_code=201)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    existing = (
        db.query(models.User).filter(models.User.username == data.username).first()
    )
    if existing:
        raise HTTPException(status_code=409, detail="Username already taken")

    user = models.User(username=data.username, password_hash=argon2.hash(data.password))

    db.add(user)
    db.commit()
    return {"message": f"User '{data.username}' registered successfully"}
