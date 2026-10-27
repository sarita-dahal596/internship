
# IMPORTS


# Import FastAPI tools
from fastapi import FastAPI, Depends, HTTPException

# Import asynchronous SQLAlchemy session
from sqlalchemy.ext.asyncio import AsyncSession

# Import text() for writing SQL
from sqlalchemy import text

# Import our database dependency
from week6.async_db import get_db



# CREATE FASTAPI APP


app = FastAPI(
    title="Command Design Pattern API"
)



# HOME


@app.get("/")
async def home():

    return {
        "message": "Digital Wallet Command Pattern API"
    }



# DEPOSIT COMMAND


class DepositCommand:

    # Receive database session and transaction data
    def __init__(
        self,
        db,
        user_id,
        amount,
        merchant
    ):

        self.db = db
        self.user_id = user_id
        self.amount = amount
        self.merchant = merchant


    # Execute deposit command
    async def execute(self):

        # Amount cannot be zero or negative
        if self.amount <= 0:

            raise HTTPException(
                status_code=400,
                detail="Amount must be greater than 0"
            )


        # Insert deposit transaction into database
        await self.db.execute(

            text("""
                INSERT INTO transactions
                (
                    user_id,
                    transaction_type,
                    amount,
                    receiver_id,
                    merchant
                )
                VALUES
                (
                    :user_id,
                    :transaction_type,
                    :amount,
                    :receiver_id,
                    :merchant
                )
            """),

            {
                "user_id": self.user_id,
                "transaction_type": "DEPOSIT",
                "amount": self.amount,

                # Deposit does not need receiver
                "receiver_id": None,

                "merchant": self.merchant
            }
        )


        # Save transaction
        await self.db.commit()


        return "Deposit successful"



# WITHDRAW COMMAND


class WithdrawCommand:

    def __init__(
        self,
        db,
        user_id,
        amount,
        merchant
    ):

        self.db = db
        self.user_id = user_id
        self.amount = amount
        self.merchant = merchant


    async def execute(self):

        # Check amount
        if self.amount <= 0:

            raise HTTPException(
                status_code=400,
                detail="Amount must be greater than 0"
            )


        # Insert withdrawal transaction
        await self.db.execute(

            text("""
                INSERT INTO transactions
                (
                    user_id,
                    transaction_type,
                    amount,
                    receiver_id,
                    merchant
                )
                VALUES
                (
                    :user_id,
                    :transaction_type,
                    :amount,
                    :receiver_id,
                    :merchant
                )
            """),

            {
                "user_id": self.user_id,
                "transaction_type": "WITHDRAW",
                "amount": self.amount,

                # Withdraw does not need receiver
                "receiver_id": None,

                "merchant": self.merchant
            }
        )


        # Save transaction
        await self.db.commit()


        return "Withdrawal successful"



# TRANSFER COMMAND


class TransferCommand:

    def __init__(
        self,
        db,
        user_id,
        receiver_id,
        amount
    ):

        self.db = db
        self.user_id = user_id
        self.receiver_id = receiver_id
        self.amount = amount


    async def execute(self):

        # Check amount
        if self.amount <= 0:

            raise HTTPException(
                status_code=400,
                detail="Amount must be greater than 0"
            )


        # Receiver is required for transfer
        if self.receiver_id is None:

            raise HTTPException(
                status_code=400,
                detail="Receiver ID is required for transfer"
            )


        # User cannot transfer money to themselves
        if self.user_id == self.receiver_id:

            raise HTTPException(
                status_code=400,
                detail="Sender and receiver cannot be the same"
            )


        # Insert transfer transaction
        await self.db.execute(

            text("""
                INSERT INTO transactions
                (
                    user_id,
                    transaction_type,
                    amount,
                    receiver_id,
                    merchant
                )
                VALUES
                (
                    :user_id,
                    :transaction_type,
                    :amount,
                    :receiver_id,
                    :merchant
                )
            """),

            {
                "user_id": self.user_id,
                "transaction_type": "TRANSFER",
                "amount": self.amount,
                "receiver_id": self.receiver_id,

                # Transfer does not need merchant
                "merchant": None
            }
        )


        # Save transaction
        await self.db.commit()


        return "Transfer successful"



# POST TRANSACTION


@app.post("/transaction")
async def create_transaction(

    # User performing transaction
    user_id: int,

    # DEPOSIT / WITHDRAW / TRANSFER
    transaction_type: str,

    # Transaction amount
    amount: float,

    # Optional receiver
    receiver_id: int | None = None,

    # Optional merchant
    merchant: str | None = None,

    # Database session
    db: AsyncSession = Depends(get_db)
):


    # Clean transaction type


    # withdraw → WITHDRAW
    # Withdraw → WITHDRAW
    # WITHDRAW → WITHDRAW

    transaction_type = transaction_type.strip().upper()



    # CHECK USER EXISTS


    result = await db.execute(

        text("""
            SELECT user_id
            FROM users
            WHERE user_id = :user_id
        """),

        {
            "user_id": user_id
        }
    )


    user = result.first()


    # User does not exist
    if user is None:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )



    # DEPOSIT


    if transaction_type == "DEPOSIT":

        command = DepositCommand(
            db=db,
            user_id=user_id,
            amount=amount,
            merchant=merchant
        )



    # WITHDRAW


    elif transaction_type == "WITHDRAW":

        command = WithdrawCommand(
            db=db,
            user_id=user_id,
            amount=amount,
            merchant=merchant
        )



    # TRANSFER


    elif transaction_type == "TRANSFER":

        # Receiver must be provided
        if receiver_id is None:

            raise HTTPException(
                status_code=400,
                detail="Receiver ID is required for transfer"
            )


        # Check whether receiver exists
        receiver_result = await db.execute(

            text("""
                SELECT user_id
                FROM users
                WHERE user_id = :receiver_id
            """),

            {
                "receiver_id": receiver_id
            }
        )


        receiver = receiver_result.first()


        # Receiver not found
        if receiver is None:

            raise HTTPException(
                status_code=404,
                detail="Receiver not found"
            )


        # Create Transfer Command
        command = TransferCommand(
            db=db,
            user_id=user_id,
            receiver_id=receiver_id,
            amount=amount
        )



    # INVALID TRANSACTION


    else:

        raise HTTPException(
            status_code=400,
            detail="Use DEPOSIT, WITHDRAW or TRANSFER"
        )



    # EXECUTE COMMAND


    result = await command.execute()


    # Return response
    return {

        "message": result,

        "transaction_type": transaction_type,

        "user_id": user_id,

        "amount": amount,

        "receiver_id": receiver_id,

        "merchant": merchant
    }



# GET ALL TRANSACTIONS


@app.get("/transactions")
async def get_transactions(

    db: AsyncSession = Depends(get_db)
):

    # Select all transactions
    result = await db.execute(

        text("""
            SELECT *
            FROM transactions
            ORDER BY transaction_id DESC
        """)
    )


    # Convert rows into dictionary-like objects
    transactions = result.mappings().all()


    return transactions



# GET ONE USER'S TRANSACTIONS


@app.get("/transactions/{user_id}")
async def get_user_transactions(

    user_id: int,

    db: AsyncSession = Depends(get_db)
):

    # Get transactions belonging to user
    result = await db.execute(

        text("""
            SELECT *
            FROM transactions
            WHERE user_id = :user_id
            ORDER BY transaction_id DESC
        """),

        {
            "user_id": user_id
        }
    )


    transactions = result.mappings().all()


    return transactions