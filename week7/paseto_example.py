# Import pyseto
import pyseto

# Import Key
from pyseto import Key

# Import json
import json



# SECRET KEY


# v4.local requires a 32-byte secret key
secret_key = b"12345678901234567890123456789012"


# Create PASETO key
key = Key.new(
    version=4,
    purpose="local",
    key=secret_key
)



# USER INFORMATION


user_data = {
    "user_id": 1,
    "email": "user@gmail.com",
    "role": "user"
}


# Convert dictionary into JSON
payload = json.dumps(user_data)



# CREATE PASETO TOKEN


token = pyseto.encode(
    key,
    payload
)


print("PASETO Token:")
print(token.decode())



# VERIFY / DECODE TOKEN


decoded = pyseto.decode(
    key,
    token
)


# Convert bytes into string
decoded_payload = decoded.payload.decode()


print("\nDecoded Payload:")
print(decoded_payload)


# Convert JSON back into Python dictionary
user = json.loads(decoded_payload)


print("\nUser ID:")
print(user["user_id"])

print("\nEmail:")
print(user["email"])

print("\nRole:")
print(user["role"])