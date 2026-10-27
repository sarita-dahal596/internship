from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime
)

from sqlalchemy.sql import func # func.now() lets MySQL automatically store current date/time

from database import Base



# USER TABLE

# This class represents the "users" table in MySQL
class User(Base):

    __tablename__ = "users"

    user_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False
    )
    # Wallet/account tier
    tier = Column(
        String(20),
        default="Basic"
    )

    balance = Column(
        Float,
        default=0
    )



# TRANSACTION TABLE


class Transaction(Base):

    __tablename__ = "transactions"

    transaction_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    # Person performing transaction
    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )
    #transaction type
    # DEPOSIT
    # WITHDRAWAL
    # TRANSFER
    # PAYMENT
    transaction_type = Column(
        String(30),
        nullable=False
    )
    # Amount of transaction
    amount = Column(
        Float,
        nullable=False
    )
    # Used only when money is transferred to another user.
    # Used for transfer
    receiver_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=True
    )

    # Used for payment
    merchant = Column(
        String(100),
        nullable=True
    )
    # Automatically save transaction date/time
    created_at = Column(
        DateTime,
        server_default=func.now()
    )