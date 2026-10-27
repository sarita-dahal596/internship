# Import FastAPI
from fastapi import FastAPI, Depends

# Import async database session
from sqlalchemy.ext.asyncio import AsyncSession

# Import select
from sqlalchemy import select

# Database
from payment_project.database import (
    get_db,
    engine,
    Base
)

# Import model
from payment_project.models import Payment

# Import schema
from payment_project.schemas import PaymentRequest

# Import Facade
from payment_project.facade import PaymentFacade


# Create FastAPI application
app = FastAPI(
    title="Payment Processing Backend"
)



# CREATE TABLE WHEN APPLICATION STARTS


@app.on_event("startup")
async def startup():

    # Open database connection
    async with engine.begin() as connection:

        # Create payments table if it doesn't exist
        await connection.run_sync(
            Base.metadata.create_all
        )



# HOME


@app.get("/")
async def home():

    return {
        "message": "Payment Processing Backend API"
    }



# PROCESS PAYMENT


@app.post("/payments")
async def process_payment(

    # Request body from Swagger
    payment: PaymentRequest,

    # Async database session
    db: AsyncSession = Depends(get_db)
):

    # Create Facade
    facade = PaymentFacade(db)


    # Facade handles complete workflow
    result = await facade.process_payment(

        user_id=payment.user_id,

        method=payment.method,

        amount=payment.amount
    )


    return result



# GET ALL PAYMENTS


@app.get("/payments")
async def get_payments(

    db: AsyncSession = Depends(get_db)
):

    # SELECT * FROM payments
    result = await db.execute(
        select(Payment)
    )


    payments = result.scalars().all()


    # Convert objects into response
    return [
        {
            "payment_id": payment.payment_id,
            "user_id": payment.user_id,
            "payment_method": payment.payment_method,
            "amount": payment.amount,
            "status": payment.status,
            "created_at": payment.created_at
        }

        for payment in payments
    ]