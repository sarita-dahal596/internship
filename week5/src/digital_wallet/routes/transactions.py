# optimal - value is not required
from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    BackgroundTasks
)

from sqlalchemy.orm import Session

# Database dependency
from dependencies import get_db
from models import Transaction

# Request schemas
from schemas import (
    DepositRequest,
    WithdrawRequest,
    TransferRequest,
    PaymentRequest
)

# Wallet business logic
from services import (
    deposit,
    withdraw,
    transfer,
    payment
)

# Background task function
from background_tasks import (
    transaction_notification
)

# Create router
router = APIRouter(
    tags=["Transactions"]
)


@router.post("/deposit")
def make_deposit(
        # Validate request body
        data: DepositRequest,
        background_tasks: BackgroundTasks,
        # Automatically create DB session
        db: Session = Depends(get_db)
):
    # Perform deposit
    user, transaction = deposit(
        db,
        data.user_id,
        data.amount
    )
    # Add notification to background
    background_tasks.add_task(
        transaction_notification,
        f"User {user.user_id} deposited Rs. {data.amount}"
    )
    # API response
    return {
        "message": "Deposit successful",
        "transaction_id": transaction.transaction_id,
        "amount": transaction.amount,
        "balance": user.balance
    }


@router.post("/withdraw")
def make_withdrawal(
        data: WithdrawRequest,
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db)
):
    # Call withdrawal logic from services.py
    user, transaction = withdraw(
        db,
        data.user_id,
        data.amount
    )

    background_tasks.add_task(
        transaction_notification,
        f"User {user.user_id} withdrew Rs. {data.amount}"
    )

    return {
        "message": "Withdrawal successful",
        "transaction_id": transaction.transaction_id,
        "amount": transaction.amount,
        "balance": user.balance
    }


@router.post("/transfer")
def make_transfer(
        data: TransferRequest,
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db)
):
    # Perform transfer
    sender, receiver, transaction = transfer(
        db,
        data.sender_id,
        data.receiver_id,
        data.amount
    )
    # Notification runs after response
    background_tasks.add_task(
        transaction_notification,
        f"User {sender.user_id} transferred "
        f"Rs. {data.amount} to User {receiver.user_id}"
    )

    return {
        "message": "Transfer successful",
        "transaction_id": transaction.transaction_id,
        "sender_balance": sender.balance,
        "receiver_balance": receiver.balance
    }


@router.post("/payment")
def make_payment(
        data: PaymentRequest,
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db)
):
    # Process payment
    user, transaction = payment(
        db,
        data.user_id,
        data.amount,
        data.merchant
    )

    background_tasks.add_task(
        transaction_notification,
        f"User {user.user_id} paid "
        f"Rs. {data.amount} to {data.merchant}"
    )

    return {
        "message": "Payment successful",
        "transaction_id": transaction.transaction_id,
        "merchant": transaction.merchant,
        "amount": transaction.amount,
        "balance": user.balance
    }


# Transaction history + filtering
@router.get("/transactions")
def transaction_history(
        user_id: Optional[int] = None,
        transaction_type: Optional[str] = None,
        db: Session = Depends(get_db)
):
    # SELECT * FROM transactions
    query = db.query(Transaction)

    # If user_id was provided
    if user_id is not None:
        # Show transactions where the user was sender/owner OR receiver

        query = query.filter(
            (Transaction.user_id == user_id)
            |
            (Transaction.receiver_id == user_id)
        )

    if transaction_type:
        # If transaction type was provided
        query = query.filter(
            Transaction.transaction_type
            == transaction_type.upper()
        )
    # Execute SQL query
    transactions = query.all()

    # Return results
    return {
        "count": len(transactions),
        "transactions": transactions
    }
