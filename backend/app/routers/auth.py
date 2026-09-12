from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..security import create_token, hash_password, verify_password

router = APIRouter()
class AuthInput(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

@router.post("/register")
def register(payload: AuthInput, db: Session = Depends(get_db)):
    if db.query(User).filter_by(email=payload.email).first(): raise HTTPException(409, "Email already registered")
    user = User(email=payload.email, password_hash=hash_password(payload.password)); db.add(user); db.commit(); db.refresh(user)
    return {"access_token": create_token(user.id), "token_type": "bearer", "email": user.email}

@router.post("/login")
def login(payload: AuthInput, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash): raise HTTPException(401, "Invalid email or password")
    return {"access_token": create_token(user.id), "token_type": "bearer", "email": user.email}