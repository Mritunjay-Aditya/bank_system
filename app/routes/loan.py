from fastapi import APIRouter, Depends, HTTPException
from app.models import Loan, Payment
from app.database import loans_collection
import random
from pydantic import BaseModel

router = APIRouter()

class PaymentRequest(BaseModel):
    loan_id: str
    amount_paid: float
    payment_type: str

class LoanRequest(BaseModel):
    customer_id: str
    loan_amount: float
    loan_period: int
    rate_of_interest: float

def generate_loan_id(customer_id: str) -> str:
    random_number = random.randint(1000, 9999)
    return f"{random_number}{customer_id}"

@router.post("/lend")
async def lend(loan_request: LoanRequest):
    customer_id = loan_request.customer_id
    loan_amount = loan_request.loan_amount
    loan_period = loan_request.loan_period
    rate_of_interest = loan_request.rate_of_interest

    interest = loan_amount * (loan_period / 12) * rate_of_interest / 100
    total_amount = loan_amount + interest
    emi = round(total_amount / loan_period, 2)

    loan_id = generate_loan_id(customer_id)
    loan_data = Loan(
        loan_id=loan_id,
        customer_id=customer_id,
        loan_amount=loan_amount,
        loan_period=loan_period,
        rate_of_interest=rate_of_interest,
        total_amount=total_amount,
        emi=emi,
        balance_amount=total_amount,
        emi_left=loan_period
    ).dict()

    result = loans_collection.insert_one(loan_data)
    loan_data["loan_id"] = str(result.inserted_id)

    return {
        "loan_id": loan_data["loan_id"],
        "total_amount": total_amount,
        "emi": emi
    }

@router.post("/payment")
async def payment(payment_request: PaymentRequest):
    loan_id = payment_request.loan_id
    amount_paid = payment_request.amount_paid
    payment_type = payment_request.payment_type

    loan = loans_collection.find_one({"loan_id": loan_id})
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    loan["balance_amount"] = round(loan["balance_amount"], 2)

    if payment_type == "EMI":
        loan["balance_amount"] -= amount_paid
        loan["emi_left"] -= 1
    elif payment_type == "LUMP SUM":
        loan["balance_amount"] -= amount_paid

    if loan["balance_amount"] <= 0.99:
        loan["balance_amount"] = 0
        loan["emi_left"] = 0
        loan["emi"] = 0  
        loan["status"] = "Paid Off"
    else:
        remaining_loan_amount = loan["balance_amount"]
        emi = round(remaining_loan_amount / loan["emi_left"], 2) if loan["emi_left"] > 0 else 0
        loan["emi"] = emi

    loans_collection.update_one({"loan_id": loan_id}, {"$set": loan})

    payment = Payment(loan_id=loan_id, amount_paid=amount_paid, payment_type=payment_type).dict()
    loans_collection.update_one({"loan_id": loan_id}, {"$push": {"payments": payment}})

    return {
        "message": "Payment successful",
        "balance_amount": loan["balance_amount"],
        "emi_left": loan["emi_left"],
        "monthly_emi": loan.get("emi", 0)
    }
    
@router.get("/ledger/{loan_id}")
async def ledger(loan_id: str):
    loan = loans_collection.find_one({"loan_id": loan_id})
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    transactions = loan.get("payments", [])
    balance_amount = loan["balance_amount"]
    emi = loan["emi"]
    emi_left = loan["emi_left"]

    return {
        "loan_id": loan["loan_id"],
        "customer_id": loan["customer_id"],
        "loan_amount": loan["loan_amount"],
        "total_amount": loan["total_amount"],
        "balance_amount": round(balance_amount, 2),
        "monthly_emi": emi,
        "emi_left": emi_left,
        "transactions": transactions
    }

@router.get("/account_overview/{customer_id}")
async def account_overview(customer_id: str):
    loans = loans_collection.find({"customer_id": customer_id})
    overview = []
    for loan in loans:
        overview.append({
            "loan_id": loan["loan_id"],
            "loan_amount": loan["loan_amount"],
            "total_amount": loan["total_amount"],
            "emi": loan["emi"],
            "interest": loan["total_amount"] - loan["loan_amount"],
            "amount_paid": loan["loan_amount"] - loan["balance_amount"],
            "emi_left": loan["emi_left"],
            "status": loan.get("status", "Active")
        })
    return overview
