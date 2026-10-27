from fastapi import FastAPI

app = FastAPI()


# Email observer
class EmailService:

    def update(self):

        return "Email notification sent"


# SMS observer
class SMSService:

    def update(self):

        return "SMS notification sent"


# Transaction class
class Transaction:

    def __init__(self):

        # Store observers
        self.observers = []

    # Add observer
    def subscribe(self, observer):

        self.observers.append(observer)

    # Complete transaction
    def complete(self):

        notifications = []

        # Notify every subscribed observer
        for observer in self.observers:

            notifications.append(
                observer.update()
            )

        return notifications


@app.post("/complete-transaction")
def complete_transaction():

    # Create transaction
    transaction = Transaction()

    # Subscribe email service
    transaction.subscribe(
        EmailService()
    )

    # Subscribe SMS service
    transaction.subscribe(
        SMSService()
    )

    # Complete transaction and notify observers
    messages = transaction.complete()

    return {
        "status": "Transaction completed",
        "notifications": messages
    }