from fastapi import APIRouter, Depends, HTTPException, status
from app.utils import hash_password, verify_password, create_access_token
from app.database import users_collection
from app.models import User
from fastapi.security import OAuth2PasswordRequestForm
import random

router = APIRouter()

def generate_customer_id() -> str:
    """Generate a random 8-digit customer ID."""
    return str(random.randint(10000000, 99999999))

@router.post("/signup")
async def signup(username: str, email: str, password: str):
    user = users_collection.find_one({"email": email})
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(password)
    customer_id = generate_customer_id()
    user_data = {
        "username": username,
        "email": email,
        "hashed_password": hashed_password,
        "customer_id": customer_id  # Include the customer ID in the user data
    }
    users_collection.insert_one(user_data)

    return {"message": "User created successfully", "customer_id": customer_id}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_collection.find_one({"email": form_data.username})

    if not user:
        print("User not found in database")
        raise HTTPException(status_code=400, detail="Invalid credentials")

    print(f"Attempting to verify password for user: {user['email']}")
    print(f"Stored hashed password: {user['hashed_password']}")
    print(f"Provided password: {form_data.password}")

    if not verify_password(form_data.password, user["hashed_password"]):
        print("Password verification failed")
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token({"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}
