from fastapi import FastAPI

app = FastAPI()


# Balance service
class BalanceService:

    def check_balance(self):
        return "Balance checked"


# Transaction service
class TransactionService:

    def transfer(self):
        return "Money transferred"


# Notification service
class NotificationService:

    def send_notification(self):
        return "Notification sent"


# Facade
class TransferFacade:

    def transfer_money(self):

        # Call balance service
        balance = BalanceService().check_balance()

        # Call transaction service
        transaction = TransactionService().transfer()

        # Call notification service
        notification = NotificationService().send_notification()

        # Return combined result
        return {
            "balance": balance,
            "transaction": transaction,
            "notification": notification
        }


@app.post("/transfer")
def transfer():

    # Create facade
    facade = TransferFacade()

    # One simple method handles multiple services
    return facade.transfer_money()