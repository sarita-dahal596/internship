# Import FastAPI and HTTPException
from fastapi import FastAPI, HTTPException

# Import BaseModel for request body
from pydantic import BaseModel



# CREATE FASTAPI APPLICATION

#Create the FastAPI application
app = FastAPI(
    title="Authentication Example"
)



# USER SCHEMA


# This defines what the user must enter in Swagger
class LoginRequest(BaseModel):

    username: str
    password: str



# SAMPLE USER


# Sample user for learning
# Later this data can come from the database
user = {
    "username": "sarita",
    "password": "12345"
}



# HOME endpoints


@app.get("/")
async def home():

    return {
        "message": "Authentication API is running"
    }



# LOGIN / AUTHENTICATION


@app.post("/login")
async def login(data: LoginRequest):


    # CHECK USERNAME


    if data.username != user["username"]:

        raise HTTPException(
            status_code=401,
            detail="Invalid username"
        )



    # CHECK PASSWORD


    if data.password != user["password"]:

        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )





    return {
        "message": "Login successful",
        "username": data.username
    }