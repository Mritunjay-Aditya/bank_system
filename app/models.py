from pydantic import BaseModel
from bson import ObjectId
from typing import Optional, List
from datetime import datetime

class User(BaseModel):
    username: str
    email: str
    hashed_password: str
    is_active: bool = True
    customer_id: str

class Loan(BaseModel):
    customer_id: str
    loan_amount: float
    loan_period: int
    rate_of_interest: float
    total_amount: float
    emi: float
    payments: List[dict] = []
    balance_amount: float
    emi_left: int
    loan_id: Optional[str] = None

class Payment(BaseModel):
    loan_id: str
    amount_paid: float
    payment_date: datetime = datetime.now()
    payment_type: str
