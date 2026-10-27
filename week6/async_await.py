from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from week6.async_db import get_db


# Create FastAPI application
app = FastAPI()


# Home endpoint
@app.get("/")
async def home():

    return {
        "message": "Welcome to FastAPI"
    }

# Endpoint for getting all users
# Get users asynchronously from MySQL
@app.get("/users")
async def get_users(
        # FastAPI calls get_db() and gives its AsyncSession to the variable "db"
    db: AsyncSession = Depends(get_db)
):


    # Execute SQL query asynchronously await waits for MySQL to return the result without blocking the event loop
    result = await db.execute(
        text("SELECT * FROM users")
    )
    # Convert database rows into dictionary-like objects
    # .all() gets all returned users
    users = result.mappings().all()

    return users