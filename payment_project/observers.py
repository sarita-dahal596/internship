
# EMAIL OBSERVER


class EmailObserver:

    async def update(self, status):

        return f"Email notification: Payment {status}"



# SMS OBSERVER


class SMSObserver:

    async def update(self, status):

        return f"SMS notification: Payment {status}"



# PAYMENT NOTIFIER


class PaymentNotifier:

    def __init__(self):

        # List of observers
        self.observers = []


    # Add observer
    def subscribe(self, observer):

        self.observers.append(observer)


    # Notify every observer
    async def notify(self, status):

        messages = []

        # Send status to each observer
        for observer in self.observers:

            message = await observer.update(status)

            messages.append(message)

        return messages