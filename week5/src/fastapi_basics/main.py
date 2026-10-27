from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

#create customer schema
class Customer(BaseModel):
    name: str
    email: str
    phone: str
    address: str


customers = {
    1: {
        "name": "Ram Sharma",
        "email": "ram@gmail.com",
        "phone": "9800000000",
        "address": "Kathmandu"
    }
}
#get customer by id
@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):

    if customer_id not in customers:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customers[customer_id]

#get all customers
@app.get("/customers")
def get_customers():
    return customers

#add new customer
@app.post("/customers", status_code=201)
def create_customer(customer: Customer):

    customer_id = len(customers) + 1

    customers[customer_id] = customer.model_dump()

    return {
        "message": "Customer created successfully",
        "customer": customers[customer_id]
    }

#update customer
@app.put("/customers/{customer_id}")
def update_customer(customer_id: int, customer: Customer):

    if customer_id not in customers:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    customers[customer_id] = customer.model_dump()

    return {
        "message": "Customer updated successfully",
        "customer": customers[customer_id]
    }

class CustomerUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    address: str | None = None

@app.patch("/customers/{customer_id}")
def patch_customer(customer_id: int, customer: CustomerUpdate):

    if customer_id not in customers:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    update_data = customer.model_dump(exclude_unset=True)

    customers[customer_id].update(update_data)

    return {
        "message": "Customer updated successfully",
        "customer": customers[customer_id]
    }

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int):

    if customer_id not in customers:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    del customers[customer_id]

    return {
        "message": "Customer deleted successfully"
    }