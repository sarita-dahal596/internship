# Import FastAPI
from fastapi import FastAPI

app = FastAPI()


# eSewa payment class
class EsewaPayment:

    def pay(self, amount):
        return f"Rs. {amount} paid using eSewa"


# Khalti payment class
class KhaltiPayment:

    def pay(self, amount):
        return f"Rs. {amount} paid using Khalti"


# Factory function
def payment_factory(method):

    # Create eSewa object
    if method == "esewa":
        return EsewaPayment()

    # Create Khalti object
    elif method == "khalti":
        return KhaltiPayment()

    # Invalid method
    return None


# Payment endpoint
@app.post("/pay")
def make_payment(method: str, amount: float):

    # Ask factory to create required payment object
    payment = payment_factory(method)

    # Check invalid payment method
    if payment is None:
        return {"message": "Invalid payment method"}

    # Use created object
    return {
        "message": payment.pay(amount)
    }