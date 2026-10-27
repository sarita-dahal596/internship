
from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    DateTime,
    ForeignKey
)

from week7_project.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    username = Column(
        String(50),
        unique=True,
        nullable=False
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False
    )

    # Store the hashed password, never plain text
    password_hash = Column(
        String(255),
        nullable=False
    )

    role = Column(
        String(20),
        default="user",
        nullable=False
    )


class Account(Base):
    __tablename__ = "accounts"

    account_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    account_number = Column(
        String(30),
        unique=True,
        nullable=False
    )

    # Numeric prevents floating-point rounding errors
    balance = Column(
        Numeric(15, 2),
        default=0,
        nullable=False
    )


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    account_id = Column(
        Integer,
        ForeignKey("accounts.account_id"),
        nullable=False
    )

    transaction_type = Column(
        String(30),
        nullable=False
    )

    amount = Column(
        Numeric(15, 2),
        nullable=False
    )

    from_account = Column(
        String(30),
        nullable=True
    )

    to_account = Column(
        String(30),
        nullable=True
    )

    status = Column(
        String(20),
        default="SUCCESS",
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Merchant receiving the payment
    merchant_id = Column(
        Integer,
        ForeignKey("merchants.merchant_id"),
        nullable=True
    )


# Store merchant details and available balance
class Merchant(Base):
    __tablename__ = "merchants"

    merchant_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    merchant_name = Column(
        String(100),
        nullable=False
    )

    merchant_code = Column(
        String(30),
        unique=True,
        nullable=False
    )

    balance = Column(
        Numeric(15, 2),
        default=0,
        nullable=False
    )
