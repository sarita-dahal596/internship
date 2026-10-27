# Import Pydantic
from pydantic import BaseModel


# Request body
class PaymentRequest(BaseModel):

    # User ID
    user_id: int

    # Payment method
    method: str

    # Payment amount
    amount: float