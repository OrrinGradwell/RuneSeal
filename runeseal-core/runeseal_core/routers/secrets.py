import os
from typing import Annotated, List

from fastapi import APIRouter, Depends, Header, HTTPException, status
from jose import JWTError, jwt
from pydantic import BaseModel
from runeseal_core import models
from runeseal_core.database import SessionLocal
from runeseal_core.models import User
from runeseal_core.security import oauth2_scheme
from sqlalchemy.orm import Session

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Auth handling (simplified for now) ---
def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
) -> User:
    try:
        payload = jwt.decode(
            token,
            os.getenv("JWT_SECRET", "changeme_this_is_dev_only"),
            algorithms=["HS256"],
        )
        sub = payload.get("sub")
        if sub is None:
            raise HTTPException(
                status_code=401, detail="Invalid token: missing subject"
            )
        user_id = int(sub)
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# --- Schemas ---
class SecretCreate(BaseModel):
    key: str
    value: str


class SecretOut(BaseModel):
    key: str
    created_at: str


class SecretResponse(BaseModel):
    message: str
    key: str


# --- Routes ---
@router.post("/", response_model=SecretResponse)
def add_secret(
    payload: SecretCreate,
    user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    encrypted_value = f"enc::{payload.value}"
    secret = models.Secret(
        key=payload.key, value_encrypted=encrypted_value, owner_id=user.id
    )
    db.add(secret)
    db.commit()
    return {"message": "Secret stored", "key": payload.key}


@router.get("/", response_model=List[SecretOut])
def list_secrets(
    user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)
):
    secrets = db.query(models.Secret).filter(models.Secret.owner_id == user.id).all()
    return [SecretOut(key=s.key, created_at=s.created_at.isoformat()) for s in secrets]


@router.delete("/{key}")
def delete_secret(
    key: str,
    user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    secret = (
        db.query(models.Secret)
        .filter(models.Secret.key == key, models.Secret.owner_id == user.id)
        .first()
    )

    if not secret:
        raise HTTPException(status_code=404, detail="Secret not found")

    db.delete(secret)
    db.commit()
    return {"message": "Secret deleted"}
