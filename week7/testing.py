from fastapi import FastAPI, HTTPException

app = FastAPI()





@app.get("/")
def home():

    return {
        "message": "API is working"
    }



# GET USER


@app.get("/users/{user_id}")
def get_user(user_id: int):

    # Example user
    if user_id == 1:

        return {
            "id": 1,
            "name": "Ram"
        }

    # User not found
    raise HTTPException(
        status_code=404,
        detail="User not found"
    )





@app.post("/payment")
def payment(amount: float):

    # Amount validation
    if amount <= 0:

        raise HTTPException(
            status_code=400,
            detail="Amount must be greater than 0"
        )

    return {
        "message": "Payment successful",
        "amount": amount
    }