from pydantic import BaseModel
from bson import ObjectId
from typing import Optional, List
from datetime import datetime

class User(BaseModel):
    username: str
    email: str
    hashed_password: str
    is_active: bool = True
    customer_id: str  # Include the customer_id field

class Loan(BaseModel):
    customer_id: str  # Associate loan with the customer_id
    loan_amount: float
    loan_period: int  # In months or years, specify as per your requirement
    rate_of_interest: float  # Annual interest rate as a percentage
    total_amount: float  # Total payable amount after interest
    emi: float  # Equated Monthly Installment
    payments: List[dict] = []  # List of payments made, could be detailed further
    balance_amount: float  # Remaining balance after payments
    emi_left: int  # Number of EMIs left to pay
    loan_id: Optional[str] = None  # Unique identifier for the loan

class Payment(BaseModel):
    loan_id: str  # ID of the loan this payment is associated with
    amount_paid: float  # Amount paid in this transaction
    payment_date: datetime = datetime.now()  # Date of the payment
    payment_type: str  # Type of payment: "EMI" or "Lump Sum"
