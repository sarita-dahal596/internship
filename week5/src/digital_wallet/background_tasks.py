from datetime import datetime


def transaction_notification(message):

    print(
        f"[{datetime.now()}] {message}"
    )