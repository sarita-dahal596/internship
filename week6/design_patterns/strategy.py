from fastapi import FastAPI

app = FastAPI()


# First payment strategy
class EsewaStrategy:

    def pay(self, amount):

        return f"Rs. {amount} paid using eSewa"


# Second payment strategy
class KhaltiStrategy:

    def pay(self, amount):

        return f"Rs. {amount} paid using Khalti"


# Payment service
class PaymentService:

    def __init__(self, strategy):

        # Store selected strategy
        self.strategy = strategy

    def process_payment(self, amount):

        # Execute selected strategy
        return self.strategy.pay(amount)


@app.post("/payment")
def payment(method: str, amount: float):

    # Choose eSewa strategy
    if method == "esewa":

        strategy = EsewaStrategy()

    # Choose Khalti strategy
    elif method == "khalti":

        strategy = KhaltiStrategy()

    else:

        return {
            "message": "Invalid payment method"
        }

    # Give selected strategy to payment service
    service = PaymentService(strategy)

    # Process payment
    return {
        "message": service.process_payment(amount)
    }