from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
# Product-> defines what data a product should contain
class product(BaseModel):
    name : str
    price : float
    category :str
    quantity : str

#sample product data
# Dictionary used as temporary storage
# Here, 1 and 2 are product IDs
products= {
    1: {
        "name": "computer",
        "price":100000,
        "category":"Electronics",
        "quantity":"3",

    },
    2: {
        "name": "tablet",
        "price": 8000,
        "category": "Electronics",
        "quantity": "5",
        }
}

#get all products
# When the client sends GET /products,
# this function will execute
@app.get("/products")
def get_products():
    return products

#get product by id
# {product_id} is a path parameter
@app.get("/products/{product_id}")
def get_products(product_id: int):    # Check whether the given product ID exists
    if product_id not in products:    # If product does not exist,return 404 Not Found error
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    return products[product_id]

#post -> add new product
@app.post("/products")
def add_product(product : product):
    new_id = max(products.keys()) + 1

    products[new_id] = product.model_dump()

    return {
        "message": "Product added successfully",
        "product": products[new_id]
    }

#put->full update
@app.put("/products/{product_id}")
def update_product(product_id: int, product: product):

    # Check whether the product exists
    if product_id not in products:

        # Return 404 error if product is not found
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # Replace the old product data with the new complete product data

    products[product_id] = product.model_dump()

    # Return updated product
    return {
        "message": "Product updated successfully",
        "product": products[product_id]
    }
#patch->partially update
@app.patch("/products/{product_id}")
def patch_product(product_id: int, data: dict):

    # Check whether product exists
    if product_id not in products:

        # Return 404 error if product is not found
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # Update only the fields sent by the client
    products[product_id].update(data)

    # Return partially updated product
    return {
        "message": "Product partially updated",
        "product": products[product_id]
    }

@app.delete("/products/{product_id}")
def delete_product(product_id: int):

    # Check whether product exists
    if product_id not in products:

        # Return 404 error if product is not found
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # pop() removes the product from the dictionary  and also returns the deleted product

    deleted_product = products.pop(product_id)

    # Return success message and deleted product
    return {
        "message": "Product deleted successfully",
        "product": deleted_product
    }

