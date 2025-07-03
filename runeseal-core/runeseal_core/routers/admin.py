from fastapi import APIRouter, Depends, HTTPException, status
from passlib.hash import argon2
from pydantic import BaseModel
from runeseal_core import models
from runeseal_core.database import SessionLocal
from sqlalchemy.orm import Session

router = APIRouter()


# DB session dep
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Payload schema
class InitRequest(BaseModel):
    admin_username: str
    admin_password: str
    system_password: str
    x_api_key: str = None


@router.post("/init")
def initialize_vault(payload: InitRequest, db: Session = Depends(get_db)):
    existing = db.query(models.User).first()
    if existing:
        raise HTTPException(status_code=400, detail="Vault already initialized")

    new_user = models.User(
        username=payload.admin_username,
        password_hash=argon2.hash(payload.admin_password),
        is_admin=True,
    )
    db.add(new_user)
    db.commit()

    # Optionally store system_password or api_key (future feature)
    return {"message": "Vault initialized", "admin": payload.admin_username}
