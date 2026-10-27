# Import payment strategies
from payment_project.strategies import (
    EsewaStrategy,
    KhaltiStrategy,
    CardStrategy
)


# Payment Factory
class PaymentFactory:

    @staticmethod
    def create_payment_processor(method):

        # Clean input
        method = method.strip().lower()

        # Create eSewa processor
        if method == "esewa":

            return EsewaStrategy()

        # Create Khalti processor
        elif method == "khalti":

            return KhaltiStrategy()

        # Create Card processor
        elif method == "card":

            return CardStrategy()

        # Invalid payment method
        else:

            return None