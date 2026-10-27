# Used for type hinting the database session
from sqlalchemy.orm import Session

from models import User, Transaction

# Import custom errors
from exceptions import (
    InvalidAmountError,
    InsufficientBalanceError,
    TransactionLimitError,
    UserNotFoundError,
    EmailAlreadyExistsError,
    InvalidTransferError
)



# FIND USER


def find_user(db: Session, user_id: int):

    # Find user using primary key
    user = db.get(User, user_id)

    # If user doesn't exist
    if not user:
        raise UserNotFoundError(
            "User not found."
        )

    return user



# GET TRANSACTION LIMIT


def get_transaction_limit(tier):

    if tier == "Basic":
        return 10000

    elif tier == "Silver":
        return 50000

    elif tier == "Premium":
        return 100000

    return 10000



# VALIDATE TRANSACTION


def validate_transaction(user, amount):

    # Amount must be positive
    if amount <= 0:
        raise InvalidAmountError(
            "Amount must be greater than 0."
        )

    # Get limit according to user's tier
    limit = get_transaction_limit(
        user.tier
    )

    # Check whether amount exceeds limit
    if amount > limit:
        raise TransactionLimitError(
            f"{user.tier} transaction limit "
            f"is Rs. {limit}."
        )



# CREATE USER


def create_user(
    db: Session,
    name,
    email,
    tier
):

    # Check whether email already exists
    existing = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    # If email already exists, stop
    if existing:
        raise EmailAlreadyExistsError(
            "Email already exists."
        )

    # Create user object
    user = User(
        name=name,
        email=email,
        tier=tier,
        balance=0
    )

    # Add user to session
    db.add(user)

    # Send INSERT to MySQL without committing
    db.flush()

    # Refresh to get generated user_id
    db.refresh(user)

    return user



# DEPOSIT


def deposit(
    db: Session,
    user_id,
    amount
):

    # Find user
    user = find_user(
        db,
        user_id
    )

    # Validate amount and limit
    validate_transaction(
        user,
        amount
    )

    # Increase balance
    user.balance += amount

    # Create transaction history
    transaction = Transaction(
        user_id=user.user_id,
        transaction_type="DEPOSIT",
        amount=amount
    )

    # Add transaction
    db.add(transaction)

    # Send changes to database,
    # but DO NOT permanently commit yet
    db.flush()

    # Get generated transaction_id
    db.refresh(transaction)

    return user, transaction



# WITHDRAWAL


def withdraw(
    db: Session,
    user_id,
    amount
):

    # Find user
    user = find_user(
        db,
        user_id
    )

    # Validate amount and transaction limit
    validate_transaction(
        user,
        amount
    )

    # Check available balance
    if user.balance < amount:
        raise InsufficientBalanceError(
            "Insufficient balance."
        )

    # Subtract money
    user.balance -= amount

    # Create transaction history
    transaction = Transaction(
        user_id=user.user_id,
        transaction_type="WITHDRAWAL",
        amount=amount
    )

    # Add transaction
    db.add(transaction)

    # Execute SQL without committing
    db.flush()

    # Get transaction_id
    db.refresh(transaction)

    return user, transaction



# TRANSFER


def transfer(
    db: Session,
    sender_id,
    receiver_id,
    amount
):

    # Find sender
    sender = find_user(
        db,
        sender_id
    )

    # Find receiver
    receiver = find_user(
        db,
        receiver_id
    )

    # Sender and receiver cannot be same
    if sender.user_id == receiver.user_id:
        raise InvalidTransferError(
            "Sender and receiver cannot be same."
        )

    # Validate amount and limit
    validate_transaction(
        sender,
        amount
    )

    # Check sender's balance
    if sender.balance < amount:
        raise InsufficientBalanceError(
            "Insufficient balance."
        )

    # Subtract from sender
    sender.balance -= amount

    # Add to receiver
    receiver.balance += amount

    # Create transfer history
    transaction = Transaction(
        user_id=sender.user_id,
        receiver_id=receiver.user_id,
        transaction_type="TRANSFER",
        amount=amount
    )

    # Add transaction
    db.add(transaction)

    # Execute changes without commit
    db.flush()

    # Get transaction_id
    db.refresh(transaction)

    return sender, receiver, transaction



# PAYMENT


def payment(
    db: Session,
    user_id,
    amount,
    merchant
):

    # Find user
    user = find_user(
        db,
        user_id
    )

    # Validate amount and limit
    validate_transaction(
        user,
        amount
    )

    # Check balance
    if user.balance < amount:
        raise InsufficientBalanceError(
            "Insufficient balance."
        )

    # Subtract payment
    user.balance -= amount

    # Create payment history
    transaction = Transaction(
        user_id=user.user_id,
        transaction_type="PAYMENT",
        amount=amount,
        merchant=merchant
    )

    # Add transaction
    db.add(transaction)

    # Execute SQL without commit
    db.flush()

    # Get generated transaction_id
    db.refresh(transaction)

    return user, transaction