# Import FastAPI TestClient
from fastapi.testclient import TestClient

# Import our FastAPI application
from week7.testing_api import app


# Create test client
client = TestClient(app)



# TEST 1: HOME


def test_home():

    # Send GET request
    response = client.get("/")

    # Check status code
    assert response.status_code == 200

    # Check response data
    assert response.json() == {
        "message": "API is working"
    }



# TEST 2: GET EXISTING USER


def test_get_user():

    response = client.get("/users/1")

    assert response.status_code == 200

    assert response.json() == {
        "id": 1,
        "name": "Ram"
    }



# TEST 3: USER NOT FOUND


def test_user_not_found():

    response = client.get("/users/100")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "User not found"
    }



# TEST 4: SUCCESSFUL PAYMENT


def test_payment():

    response = client.post(
        "/payment",
        params={
            "amount": 500
        }
    )

    assert response.status_code == 200

    assert response.json() == {
        "message": "Payment successful",
        "amount": 500
    }



# TEST 5: INVALID PAYMENT


def test_invalid_payment():

    response = client.post(
        "/payment",
        params={
            "amount": -100
        }
    )

    assert response.status_code == 400

    assert response.json() == {
        "detail": "Amount must be greater than 0"
    }