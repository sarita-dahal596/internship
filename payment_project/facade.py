# Import HTTPException
from fastapi import HTTPException

# Import Payment model
from payment_project.models import Payment

# Import Factory
from payment_project.factory import PaymentFactory

# Import Observers
from payment_project.observers import (
    PaymentNotifier,
    EmailObserver,
    SMSObserver
)


# Payment Facade
class PaymentFacade:

    # Receive database session
    def __init__(self, db):

        self.db = db


    async def process_payment(
        self,
        user_id,
        method,
        amount
    ):


        # STEP 1: Validate amount


        if amount <= 0:

            raise HTTPException(
                status_code=400,
                detail="Amount must be greater than 0"
            )



        # STEP 2: Factory creates processor


        processor = (
            PaymentFactory.create_payment_processor(
                method
            )
        )


        # Invalid payment method
        if processor is None:

            raise HTTPException(
                status_code=400,
                detail="Use esewa, khalti or card"
            )



        # STEP 3: Strategy processes payment


        result = await processor.pay(amount)



        # STEP 4: Save payment in database


        payment = Payment(
            user_id=user_id,
            payment_method=method.upper(),
            amount=amount,
            status=result["status"]
        )


        # Add payment to database session
        self.db.add(payment)


        # Save payment
        await self.db.commit()


        # Refresh object to get payment_id
        await self.db.refresh(payment)



        # STEP 5: Observer notifications


        notifier = PaymentNotifier()


        # Subscribe Email observer
        notifier.subscribe(
            EmailObserver()
        )


        # Subscribe SMS observer
        notifier.subscribe(
            SMSObserver()
        )


        # Notify observers
        notifications = await notifier.notify(
            result["status"]
        )



        # STEP 6: Return final response


        return {

            "payment_id": payment.payment_id,

            "user_id": user_id,

            "payment_method": method.upper(),

            "amount": amount,

            "status": result["status"],

            "message": result["message"],

            "notifications": notifications
        }