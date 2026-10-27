# BaseModel is used to create Pydantic request schemas
from pydantic import BaseModel, EmailStr
from typing import Literal # Literal allows only specific values


# Create new user/account
class UserCreate(BaseModel):
    name: str
    email: EmailStr


    # User can only select one of these tiers
    # If no tier is provided, Basic is used
    tier: Literal[
        "Basic",
        "Silver",
        "Premium"
    ] = "Basic"


# Deposit request
class DepositRequest(BaseModel):
    user_id: int
    amount: float


# Withdrawal request
class WithdrawRequest(BaseModel):
    user_id: int
    amount: float


# Transfer request
class TransferRequest(BaseModel):
    sender_id: int
    receiver_id: int
    amount: float


# Payment request
class PaymentRequest(BaseModel):
    user_id: int
    merchant: str
    amount: float