# Import SQLAlchemy columns
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime
)

# Used for automatic date/time
from datetime import datetime

# Import Base
from payment_project.database import Base


# Payment database model
class Payment(Base):

    # Table name
    __tablename__ = "payments"

    # Primary key
    payment_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    # User making payment
    user_id = Column(
        Integer,
        nullable=False
    )

    # Payment method:
    # ESEWA / KHALTI / CARD
    payment_method = Column(
        String(20),
        nullable=False
    )

    # Payment amount
    amount = Column(
        Float,
        nullable=False
    )

    # SUCCESS / FAILED
    status = Column(
        String(20),
        nullable=False
    )

    # Payment creation time
    created_at = Column(
        DateTime,
        default=datetime.now
    )