# Raised when amount is 0 or negative
class InvalidAmountError(Exception):
    pass

# Raised when user does not have enough balance
class InsufficientBalanceError(Exception):
    pass

# Raised when transaction exceeds user's allowed limit
class TransactionLimitError(Exception):
    pass

# Raised when user_id doesn't exist
class UserNotFoundError(Exception):
    pass


# Raised when someone creates another account
# using an email that already exists
class EmailAlreadyExistsError(Exception):
    pass

# Raised for invalid transfers
class InvalidTransferError(Exception):
    pass