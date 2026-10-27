from fastapi import FastAPI, BackgroundTasks
import time
#Create the FastAPI app

app = FastAPI()



# BACKGROUND FUNCTION


def send_email(email: str):

    # Simulate time needed to send email
    time.sleep(5)

    print("Email sent successfully to:", email)



# API ENDPOINT


@app.post("/payment")
async def make_payment(
    email: str,
    amount: float,
    background_tasks: BackgroundTasks
):

    # Add send_email() to background task
    background_tasks.add_task(
        send_email,
        email
    )

    # This response is returned first
    return {
        "message": "Payment successful",
        "amount": amount,
        "email": email
    }