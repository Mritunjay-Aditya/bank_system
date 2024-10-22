from fastapi import APIRouter, Depends, HTTPException
from app.models import Loan, Payment
from app.database import loans_collection
from datetime import datetime
import random
from bson import ObjectId

router = APIRouter()

def generate_loan_id(customer_id: str) -> str:
    """Generate a loan ID using a random four-digit number and the customer ID."""
    random_number = random.randint(1000, 9999)
    return f"{random_number}{customer_id}"

@router.post("/lend")
async def lend(customer_id: str, loan_amount: float, loan_period: int, rate_of_interest: float):
    interest = loan_amount * (loan_period / 12) * rate_of_interest / 100  # Formula for Interest
    total_amount = loan_amount + interest  # Total Amount = Principal + Interest
    emi = total_amount / (loan_period )  # Monthly EMI

    loan_id = generate_loan_id(customer_id)  # Generate a unique loan ID
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

    return {"loan_id": loan_data["loan_id"], "total_amount": total_amount, "emi": emi}

@router.post("/payment")
async def payment(loan_id: str, amount_paid: float, payment_type: str):
    loan = loans_collection.find_one({"loan_id": loan_id})  # Find loan by loan_id
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    if payment_type == "EMI":
        # For EMI payments
        loan["balance_amount"] -= amount_paid
        loan["emi_left"] -= 1
    elif payment_type == "LUMP SUM":
        # For lump sum payments
        loan["balance_amount"] -= amount_paid
        
        # Check if the loan is fully paid off
        if loan["balance_amount"] <= 0:
            loan["balance_amount"] = 0  # Ensure balance is not negative
            loan["emi_left"] = 0  # No EMIs left
            loan["status"] = "Paid Off"  # Optional: Mark loan as paid off
        else:
            # Recalculate the EMI for the remaining balance
            remaining_loan_amount = loan["balance_amount"]
            emi = remaining_loan_amount / loan["emi_left"]  # New EMI calculation
            loan["emi"] = emi  # Update the EMI in loan document

    # Update the loan document
    loans_collection.update_one({"loan_id": loan_id}, {"$set": loan})

    # Record the payment
    payment = Payment(loan_id=loan_id, amount_paid=amount_paid, payment_type=payment_type).dict()
    loans_collection.update_one({"loan_id": loan_id}, {"$push": {"payments": payment}})

    return {"message": "Payment successful", "balance_amount": loan["balance_amount"], "emi_left": loan["emi_left"], "monthly_emi": loan["emi"]}


@router.get("/ledger/{loan_id}")
async def ledger(loan_id: str):
    loan = loans_collection.find_one({"loan_id": loan_id})  # Find loan by loan_id
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    # Extract necessary information
    transactions = loan.get("payments", [])  # Get all payments associated with the loan
    balance_amount = loan["balance_amount"]
    emi = loan["emi"]
    emi_left = loan["emi_left"]

    return {
        "loan_id": loan["loan_id"],
        "customer_id": loan["customer_id"],
        "loan_amount": loan["loan_amount"],
        "total_amount": loan["total_amount"],
        "balance_amount": balance_amount,
        "monthly_emi": emi,
        "emi_left": emi_left,
        "transactions": transactions
    }

@router.get("/account_overview/{customer_id}")
async def account_overview(customer_id: str):
    loans = loans_collection.find({"customer_id": customer_id})  # Find loans by customer_id
    overview = []
    for loan in loans:
        overview.append({
            "loan_id": loan["loan_id"],  # Include loan_id in the overview
            "loan_amount": loan["loan_amount"],
            "total_amount": loan["total_amount"],
            "emi": loan["emi"],
            "interest": loan["total_amount"] - loan["loan_amount"],
            "amount_paid": loan["loan_amount"] - loan["balance_amount"],
            "emi_left": loan["emi_left"],
            "status": loan.get("status", "Active")  # Include loan status, default to "Active" if not found
        })
    return overview
