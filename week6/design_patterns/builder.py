from fastapi import FastAPI

app = FastAPI()


# Builder class
class TransactionBuilder:

    def __init__(self):

        # Empty transaction
        self.transaction = {}

    # Add transaction ID
    def add_id(self, transaction_id):

        self.transaction["id"] = transaction_id

        # Return self so another method can be called
        return self

    # Add amount
    def add_amount(self, amount):

        self.transaction["amount"] = amount

        return self

    # Add status
    def add_status(self, status):

        self.transaction["status"] = status

        return self

    # Return completed object
    def build(self):

        return self.transaction


@app.get("/transaction")
def get_transaction():

    # Build transaction step-by-step
    transaction = (
        TransactionBuilder()
        .add_id(101)
        .add_amount(5000)
        .add_status("Completed")
        .build()
    )

    return transaction