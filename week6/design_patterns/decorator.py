from fastapi import FastAPI
from functools import wraps

app = FastAPI()


# Create decorator
def add_logging(function):

    # Keep information about original function
    @wraps(function)
    def wrapper(*args, **kwargs):

        # Extra functionality before endpoint
        print("API request started")

        # Run original function
        result = function(*args, **kwargs)

        # Extra functionality after endpoint
        print("API request completed")

        return result

    return wrapper


@app.get("/user")
@add_logging
def get_user():

    # Original endpoint functionality
    return {
        "id": 1,
        "name": "Ram"
    }