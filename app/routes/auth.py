from fastapi import APIRouter, Depends, HTTPException, status
from app.utils import hash_password, verify_password, create_access_token
from app.database import users_collection
from app.models import User
from fastapi.security import OAuth2PasswordRequestForm
import random
from pydantic import BaseModel

router = APIRouter()

class SignupRequest(BaseModel):
    username: str
    email: str
    password: str

def generate_customer_id() -> str:
    return str(random.randint(10000000, 99999999))

@router.post("/signup")
async def signup(request: SignupRequest):
    user = users_collection.find_one({"email": request.email})
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(request.password)
    customer_id = generate_customer_id()
    user_data = {
        "username": request.username,
        "email": request.email,
        "hashed_password": hashed_password,
        "customer_id": customer_id
    }
    users_collection.insert_one(user_data)

    return {"message": "User created successfully", "customer_id": customer_id}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_collection.find_one({"email": form_data.username})

    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token({"sub": user["email"]})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "customer_id": user["customer_id"],
        "username": user["username"]
    }
