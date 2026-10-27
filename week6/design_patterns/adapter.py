from fastapi import FastAPI

app = FastAPI()


# Imagine this is an external Khalti API
class KhaltiAPI:

    # External system uses make_payment()
    def make_payment(self, amount):

        return f"Rs. {amount} paid through Khalti"


# Adapter class
class KhaltiAdapter:

    def __init__(self):

        # Create external API object
        self.khalti = KhaltiAPI()

    # Our application wants to use pay()
    def pay(self, amount):

        # Adapter converts pay()
        # into make_payment()
        return self.khalti.make_payment(amount)


@app.post("/payment")
def payment(amount: float):

    # Create adapter
    service = KhaltiAdapter()

    # Our backend simply calls pay()
    return {
        "message": service.pay(amount)
    }