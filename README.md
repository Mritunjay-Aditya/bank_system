# Bank Loan Management System

## Overview

The **Bank Loan Management System** is an API-based application built using FastAPI and MongoDB. It allows users to manage bank loans and customer accounts with secure authentication and authorization. Customers can register, apply for loans, make payments, and view their account details, while administrators can manage and track loan accounts.

### Features:
- **User Authentication**: Register, login, and protected routes.
- **Loan Management**: Apply for loans, make EMI or lump sum payments, view loan details, and track transactions.
- **Customer Management**: Register new customers and view customer profiles.
- **MongoDB Integration**: All data is stored and retrieved using MongoDB via Motor (async MongoDB driver).

---

### Key Components

- **`api/routers/`**: FastAPI routers for handling customer and loan API endpoints.
- **`api/dependencies/db.py`**: MongoDB connection setup using Motor.
- **`models/`**: Data models for customer and loan entities.
- **`schemas/`**: Pydantic models for data validation of API requests and responses.
- **`services/`**: Business logic for handling loans and customers.
- **`utils/`**: Utility functions for calculations like interest and EMI.
- **`app/main.py`**: The entry point of the FastAPI application.


---

## Prerequisites

- **Python 3.8+**
- **MongoDB (Local or MongoDB Atlas)**
- **pip** (Python package manager)

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/bank-loan-management-system.git
   cd bank-loan-management-system
2. **Create a Virtual Environment (optional but recommended):**:
   ```bash
   python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
3. **Install Dependencies:**:
   ```bash
   pip install -r requirements.txt
4. **Set Up MongoDB:**:
- **If you don’t have MongoDB set up locally, you can create a free MongoDB Atlas cluster and get the connection string.**
- **Set the MongoDB URL and database name in .env file:**
   ```bash
    MONGODB_URL="mongodb+srv://<your-cluster-url>"
    MONGODB_DB_NAME="bank_system"
---
## Running the Application

1. **Start the FastAPI Application:**:
   ```bash
   uvicorn app.main:app --reload
The API will be running at http://127.0.0.1:8000.

2. **Access the API Documentation:**:
- **FastAPI provides interactive API documentation at /docs:**
   ```bash
    http://127.0.0.1:8000/docs
- **Alternative documentation can be accessed at /redoc:**
    ```bash
    http://127.0.0.1:8000/redocs
---
## API Endpoints
- **Authentication Endpoints:**:
   ```bash
   POST /auth/signup

- **Request Body**:
   ```bash
   {
  "username": "string",
  "email": "string",
  "password": "string"
    }
- **Login a customer**:
    ```bash
    POST /auth/login
- **Request Body**:
    ```bash
    {
     "email": "john.doe@example.com",
     "password": "strongpassword123"
   }
## Loan Endpoints:
- **Apply for a loan**:
    ```bash
    POST /loans/lend
- **Request Body**:
    ```bash
    {
    "customer_id": "605c73e8e517f1a4c03984d9",
    "principal": 50000,
    "loan_period": 5,
    "interest_rate": 5.5
    }
- **Make a loan payment**:
    ```bash
    POST /loans/payment
- **Request Body**:
    ```bash
    {
    "loan_id": "605c73e8e517f1a4c03984d9",
    "amount": 10000,
    "type": "EMI"
    }
- **Get loan ledger (loan details)**:
    ```bash
    GET /loans/ledger/{loan_id}
- **Response Example**:
    ```bash
    {
        "loan_id": "605c73e8e517f1a4c03984d9",
        "principal": 50000,
        "total_amount": 62500,
        "monthly_emi": 1041.67,
        "total_interest": 12500,
        "amount_paid": 10000,
        "emi_left": 48,
        "transactions": [
            {
                "date": "2024-01-01T00:00:00",
                "amount": 10000,
                "type": "EMI"
            }
        ]
    }
---