from fastapi import (
    FastAPI,
    Request,
    status
)

from fastapi.responses import JSONResponse

from database import Base, engine

# IMPORTANT:
# Import models so SQLAlchemy knows about the tables
import models

from routes import users, transactions

from exceptions import ( #import our  custom exceptions
    InvalidAmountError,
    InsufficientBalanceError,
    TransactionLimitError,
    UserNotFoundError,
    EmailAlreadyExistsError,
    InvalidTransferError
)


# Create tables in MySQL # It will NOT recreate existing tables every time.
Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="Digital Wallet REST API",
    description="Digital Wallet using FastAPI, SQLAlchemy and MySQL",
    version="1.0"
)

# CONNECT ROUTES
 # Add routes/users.py endpoints to application
app.include_router(
    users.router
)
# Add routes/transactions.py endpoints
app.include_router(
    transactions.router
)

# HOME ENDPOINT
@app.get("/")
def home():

    return {
        "message": "Digital Wallet API is running"
    }
# USER NOT FOUND
# Whenever UserNotFoundError occurs,FastAPI will run this function.

@app.exception_handler(UserNotFoundError)
async def user_not_found(request: Request, exc: UserNotFoundError):

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)}
    )

# INVALID AMOUNT
@app.exception_handler(InvalidAmountError)
async def invalid_amount(request: Request, exc: InvalidAmountError):

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )

# INSUFFICIENT BALANCE
@app.exception_handler(InsufficientBalanceError)
async def insufficient_balance(
    request: Request,
    exc: InsufficientBalanceError
):

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )

# TRANSACTION LIMIT EXCEEDED
@app.exception_handler(TransactionLimitError)
async def transaction_limit(
    request: Request,
    exc: TransactionLimitError
):

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )

# INVALID TRANSFER
@app.exception_handler(InvalidTransferError)
async def invalid_transfer(
    request: Request,
    exc: InvalidTransferError
):

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )

# DUPLICATE EMAIL
@app.exception_handler(EmailAlreadyExistsError)
async def duplicate_email(
    request: Request,
    exc: EmailAlreadyExistsError
):

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)}
    )