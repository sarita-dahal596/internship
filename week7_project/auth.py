
import os
import json
import time

import pyseto

from pyseto import Key
from pwdlib import PasswordHash
from dotenv import load_dotenv

load_dotenv()

# Argon2 password hashing
password_hasher = PasswordHash.recommended()

# Load PASETO secret from environment variables
secret_hex = os.getenv("PASETO_KEY_HEX", "")

if len(secret_hex) != 64:
    raise RuntimeError(
        "PASETO_KEY_HEX must contain 64 hexadecimal characters"
    )

try:
    secret_key = Key.new(
        version=4,
        purpose="local",
        key=bytes.fromhex(secret_hex)
    )

except ValueError as error:
    raise RuntimeError(
        "Invalid PASETO secret key"
    ) from error


# Token expires after one hour
TOKEN_LIFETIME_SECONDS = 3600


def hash_password(password):
    return password_hasher.hash(password)


def verify_password(plain_password, hashed_password):
    return password_hasher.verify(
        plain_password,
        hashed_password
    )


# Generate token after successful login
def create_token(user_id, username, role):
    payload = {
        "user_id": user_id,
        "username": username,
        "role": role,
        "exp": int(time.time()) + TOKEN_LIFETIME_SECONDS
    }

    token = pyseto.encode(
        secret_key,
        json.dumps(payload).encode("utf-8")
    )

    return token.decode("utf-8")


# Verify token and check expiration
def verify_token(token):
    try:
        decoded = pyseto.decode(
            secret_key,
            token
        )

        data = json.loads(decoded.payload)

        if not isinstance(data.get("user_id"), int):
            return None

        if not isinstance(data.get("exp"), int):
            return None

        if data["exp"] <= int(time.time()):
            return None

        return data

    except Exception:
        return None
