from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, status
from passlib.hash import argon2
from pydantic import BaseModel
from runeseal_core import models
from runeseal_core.database import SessionLocal
from runeseal_core.deps import verify_api_key
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


@router.post("/init", dependencies=[Depends(verify_api_key)])
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


class UserOut(BaseModel):
    id: int
    username: str
    is_admin: bool

    class Config:
        orm_mode = True


@router.get(
    "/users", response_model=List[UserOut], dependencies=[Depends(verify_api_key)]
)
def list_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.delete("/users/{user_id}", dependencies=[Depends(verify_api_key)])
def delete_user(user_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    if user_id == 1:
        raise HTTPException(
            status_code=403, detail="Cannot delete the initial admin user (id=1)"
        )
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": f"User {user_id} deleted"}
