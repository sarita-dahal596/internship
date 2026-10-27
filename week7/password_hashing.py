# Import PasswordHash from pwdlib
from pwdlib import PasswordHash



# CREATE PASSWORD HASHER


# recommended() uses a recommended secure
# password hashing configuration
password_hash = PasswordHash.recommended()



# ORIGINAL PASSWORD


password = "hello123"

print("Original Password:")
print(password)


# HASH PASSWORD


hashed_password = password_hash.hash(password)

print("\nHashed Password:")
print(hashed_password)


# VERIFY CORRECT PASSWORD


is_correct = password_hash.verify(
    "hello123",
    hashed_password
)

print("\nCorrect password result:")
print(is_correct)



# VERIFY WRONG PASSWORD


is_wrong = password_hash.verify(
    "wrong123",
    hashed_password
)

print("\nWrong password result:")
print(is_wrong)