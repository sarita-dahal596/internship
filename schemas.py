
from decimal import Decimal

from pydantic import (
    BaseModel,
    EmailStr,
    Field
)


# User registration
class RegisterRequest(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128
    )


# User login
class LoginRequest(BaseModel):
    username: str
    password: str


# Create a bank account
class AccountRequest(BaseModel):
    account_number: str = Field(
        min_length=4,
        max_length=30
    )


# Deposit and withdraw money
class MoneyRequest(BaseModel):
    account_id: int = Field(gt=0)

    # Decimal avoids floating-point errors in money calculations
    amount: Decimal = Field(
        gt=0,
        max_digits=15,
        decimal_places=2
    )


# Transfer money between two accounts
class TransferRequest(BaseModel):
    from_account_id: int = Field(gt=0)
    to_account_id: int = Field(gt=0)

    amount: Decimal = Field(
        gt=0,
        max_digits=15,
        decimal_places=2
    )



# Payment request
class PaymentRequest(BaseModel):
    user_id: int = Field(gt=0)
    merchant: str = Field(min_length=2, max_length=100)
    amount: Decimal = Field(
        gt=0,
        max_digits=15,
        decimal_places=2
    )



# Merchant registration request
class MerchantRequest(BaseModel):
    merchant_name: str = Field(min_length=2, max_length=100)
    merchant_code: str = Field(min_length=3, max_length=30)
