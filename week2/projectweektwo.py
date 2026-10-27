from abc import ABC, abstractmethod
import os


print(os.getcwd())

# CUSTOM EXCEPTIONS


# Used when the amount is 0 or negative
class InvalidAmountError(Exception):
    pass


# Used when the user does not have enough balance
class InsufficientBalanceError(Exception):
    pass


# Used when the transaction exceeds the user's limit
class TransactionLimitError(Exception):
    pass


# Used when the requested user does not exist
class UserNotFoundError(Exception):
    pass

# This class stores information about a wallet user
class User:

    def __init__(self, user_id, name, email,
                 tier="Basic", balance=0):  #If the user doesn't tell us their tier, automatically make them Basic.

        self.user_id = user_id
        self.name = name
        self.email = email
        self.tier = tier
        self.balance = balance


    # This method returns the transaction limit
    # according to the user's tier
    def get_transaction_limit(self):

        if self.tier == "Basic":
            return 10000

        elif self.tier == "Silver":
            return 50000

        elif self.tier == "Premium":
            return 100000


    # Display user information
    def display(self):

        print("\n----- USER DETAILS -----")

        print("ID:", self.user_id)
        print("Name:", self.name)
        print("Email:", self.email)
        print("Tier:", self.tier)
        print("Balance: Rs.", self.balance)

        print(
            "Transaction Limit: Rs.",
            self.get_transaction_limit()
        )

# ABSTRACT TRANSACTION CLASS

# Transaction is an abstract class
# It provides common functionality for all transactions
class Transaction(ABC):

    # Every child transaction class must implement the process() method
    @abstractmethod
    def process(self):
        pass

    # Check whether the amount is valid
    def validate_amount(self, amount):

        # Amount cannot be 0 or negative
        if amount <= 0:

            raise InvalidAmountError(
                "Amount must be greater than 0."
            )

    # Check whether the amount is within  the user's transaction limit
    def validate_limit(self, user, amount):

        if amount > user.get_transaction_limit(): #If the amount is greater than the user's allowed limit..."

            raise TransactionLimitError(  #The transaction is too large, so generate a TransactionLimitError.
                f"{user.tier} user transaction limit is "
                f"Rs. {user.get_transaction_limit()}."
            )

#Deposit class
# Deposit inherits from Transaction
class Deposit(Transaction):

    # Process deposit
    def process(self, user, amount):

        # Check amount
        self.validate_amount(amount)

        # Check transaction limit
        self.validate_limit(user, amount)

        # Add amount to user's balance
        user.balance += amount

        print(
            f"Rs. {amount} deposited successfully."
        )

        # Return transaction information
        return (
            f"Deposit | User ID: {user.user_id} | "
            f"Amount: Rs. {amount}"
        )

#withdrawal class
# Withdrawal inherits from Transaction
class Withdrawal(Transaction):

    # Process withdrawal
    def process(self, user, amount):

        # Check amount
        self.validate_amount(amount)

        # Check transaction limit
        self.validate_limit(user, amount)

        # Check whether user has enough money
        if amount > user.balance:

            raise InsufficientBalanceError(
                "Insufficient balance."
            )

        # Subtract amount from balance
        user.balance -= amount

        print(
            f"Rs. {amount} withdrawn successfully."
        )

        return (
            f"Withdrawal | User ID: {user.user_id} | "
            f"Amount: Rs. {amount}"
        )

# TRANSFER CLASS

# Transfer is used to send money from one user to another
class Transfer(Transaction):

    def process(self, sender, receiver, amount):

        # Check amount
        self.validate_amount(amount)

        # Check sender's transaction limit
        self.validate_limit(sender, amount)

        # Sender and receiver cannot be the same
        if sender.user_id == receiver.user_id:

            raise ValueError(
                "Sender and receiver cannot be the same."
            )

        # Check sender's balance
        if amount > sender.balance:

            raise InsufficientBalanceError(
                "Sender has insufficient balance."
            )

        # Remove money from sender
        sender.balance -= amount

        # Add money to receiver
        receiver.balance += amount

        print(
            f"Rs. {amount} transferred successfully "
            f"from {sender.name} to {receiver.name}."
        )

        return (
            f"Transfer | Sender: {sender.user_id} | "
            f"Receiver: {receiver.user_id} | "
            f"Amount: Rs. {amount}"
        )

#payment class
# Payment is used to pay a merchant
class Payment(Transaction):

    def process(self, user, amount, merchant):

        # Check amount
        self.validate_amount(amount)

        # Check transaction limit
        self.validate_limit(user, amount)

        # Check user's balance
        if amount > user.balance:

            raise InsufficientBalanceError(
                "Insufficient balance."
            )

        # Deduct money from user's balance
        user.balance -= amount

        print(
            f"Payment of Rs. {amount} made to {merchant}."
        )

        return (
            #f-strings to insert variable values into a string.
            f"Payment | User ID: {user.user_id} | "
            f"Merchant: {merchant} | "  #merchant contains the name of the shop or business
            f"Amount: Rs. {amount}"
        )

# WALLET CLASS
# Wallet manages users and transactions
class Wallet:

    def __init__(self):

        # List to store all users
        self.users = []

        # List to store transaction history
        self.transactions = []

        # Load existing users from file
        self.load_users()

        # Load existing transactions from file
        self.load_transactions()

    def create_user(self):

        try:

            # Get user ID
            user_id = int(
                input("Enter user ID: ")
            )

            # Check whether ID already exists
            for user in self.users:

                if user.user_id == user_id:

                    print("User ID already exists.")
                    return

            # Get user's name
            name = input("Enter name: ")

            # Get user's email
            email = input("Enter email: ")

            # Display tier options
            print("\nChoose User Tier")
            print("1. Basic")
            print("2. Silver")
            print("3. Premium")

            choice = input("Enter choice: ")

            # Select tier
            if choice == "1":
                tier = "Basic"

            elif choice == "2":
                tier = "Silver"

            elif choice == "3":
                tier = "Premium"

            else:

                print("Invalid tier.")
                return

            # Create User object
            user = User(
                user_id,
                name,
                email,
                tier
            )


            # Add user to users list
            self.users.append(user)

            # Save user to file
            self.save_users()

            print("User created successfully.")

        except ValueError:

            # Handles invalid user ID
            print("User ID must be a number.")

    # FIND USER

    def find_user(self, user_id):

        # Search through all users
        for user in self.users:

            if user.user_id == user_id:

                return user

        # If user is not found
        raise UserNotFoundError(
            "User not found."
        )

        # DEPOSIT

    def deposit(self):

        try:

            # Get user ID
            user_id = int(
                input("Enter user ID: ")
            )

            # Get deposit amount
            amount = float(
                input("Enter deposit amount: ")
            )

            # Find the user
            user = self.find_user(user_id)

            # Create Deposit object
            transaction = Deposit()

            # Process deposit
            record = transaction.process(
                user,
                amount
            )

            # Add transaction to history
            self.transactions.append(record)

            # Save updated data
            self.save_users()
            self.save_transactions()

        except (
                ValueError,
                InvalidAmountError,
                TransactionLimitError,
                UserNotFoundError
        ) as e:

            print("Error:", e)



    # ==================================================
    # WITHDRAW
    # ==================================================

    def withdraw(self):

        try:
            # Get user ID
            user_id = int(
                input("Enter user ID: ")
            )

            # Get withdrawal amount
            amount = float(
                input("Enter withdrawal amount: ")
            )

            # Find user
            user = self.find_user(user_id)

            # Create Withdrawal object
            transaction = Withdrawal()

            # Process withdrawal
            record = transaction.process(
                user,
                amount
            )

            # Save transaction in history
            self.transactions.append(record)

            # Save updated data
            self.save_users()
            self.save_transactions()

        except (
            ValueError,
            InvalidAmountError,
            InsufficientBalanceError,
            TransactionLimitError,
            UserNotFoundError
        ) as e:

            print("Error:", e)


        # TRANSFER

    def transfer(self):

        try:

            # Get sender ID
            sender_id = int(
                input("Enter sender ID: ")
            )

            # Get receiver ID
            receiver_id = int(
                input("Enter receiver ID: ")
            )

            # Get transfer amount
            amount = float(
                input("Enter transfer amount: ")
            )

            # Find sender
            sender = self.find_user(sender_id)

            # Find receiver
            receiver = self.find_user(receiver_id)

            # Create Transfer object
            transaction = Transfer()

            # Process transfer
            record = transaction.process(
                sender,
                receiver,
                amount
            )

            # Add transaction to history
            self.transactions.append(record)

            # Save updated data
            self.save_users()
            self.save_transactions()

        except (
                ValueError,
                InvalidAmountError,
                InsufficientBalanceError,
                TransactionLimitError,
                UserNotFoundError
        ) as e:

            print("Error:", e)

    def payment(self):

        try:

            # Get user ID
            user_id = int(
                input("Enter user ID: ")
            )

            # Get merchant name
            merchant = input(
                "Enter merchant name: "
            )

            # Get payment amount
            amount = float(
                input("Enter payment amount: ")
            )

            # Find user
            user = self.find_user(user_id)

            # Create Payment object
            transaction = Payment()

            # Process payment
            record = transaction.process(
                user,
                amount,
                merchant
            )

            # Add transaction to history
            self.transactions.append(record)

            # Save updated data
            self.save_users()
            self.save_transactions()

        except (
                ValueError,
                InvalidAmountError,
                InsufficientBalanceError,
                TransactionLimitError,
                UserNotFoundError
        ) as e:

            print("Error:", e)

        # VIEW USER

    def view_user(self):

        try:

            # Get user ID
            user_id = int(
                input("Enter user ID: ")
            )

            # Find user
            user = self.find_user(user_id)

            # Display user information
            user.display()

        except (
                ValueError,
                UserNotFoundError
        ) as e:

            print("Error:", e)

    # VIEW ALL USERS


    def view_users(self):

        # Check whether users exist
        if not self.users:

            print("No users found.")
            return

        print("\n========== ALL USERS ==========")

        # Display every user
        for user in self.users:

            print(
                f"ID: {user.user_id} | "
                f"Name: {user.name} | "
                f"Tier: {user.tier} | "
                f"Balance: Rs. {user.balance}"
            )


    # TRANSACTION HISTORY

    def transaction_history(self):

        # Check whether transactions exist
        if not self.transactions:

            print("No transactions found.")
            return

        print("\n====== TRANSACTION HISTORY ======")

        # enumerate() gives transaction number
        for number, transaction in enumerate(
            self.transactions,
            start=1
        ):

            print(
                f"{number}. {transaction}"
            )


    #ave users
    def save_users(self):

        # Open users.txt in write mode
        with open("users.txt", "w") as file:

            # Write every user to the file
            for user in self.users:

                # | is used to separate the values
                file.write(
                    f"{user.user_id}|"
                    f"{user.name}|"
                    f"{user.email}|"
                    f"{user.tier}|"
                    f"{user.balance}\n"
                )

        # LOAD USERS
        # ==================================================

    def load_users(self):

        # Check whether users.txt exists
        if not os.path.exists("users.txt"):
            return

        try:

            # Open file in read mode
            with open("users.txt", "r") as file:

                # Read each line
                for line in file:

                    # Remove \n and extra spaces
                    line = line.strip()

                    # Skip empty lines
                    if line == "":
                        continue

                    # Separate values using |
                    data = line.split("|")

                    # Convert data to correct types
                    user_id = int(data[0])
                    name = data[1]
                    email = data[2]
                    tier = data[3]
                    balance = float(data[4])

                    # Create User object
                    user = User(
                        user_id,
                        name,
                        email,
                        tier,
                        int(balance)
                    )

                    # Add user to list
                    self.users.append(user)

        except (
                ValueError,
                IndexError
        ):

            print("Error loading users file.")

        # SAVE TRANSACTIONS

    def save_transactions(self):

        # Open transactions.txt in write mode
        with open(
                "transactions.txt",
                "w"
        ) as file:
            # Write every transaction
            for transaction in self.transactions:
                file.write(
                    transaction + "\n")

                # LOAD TRANSACTIONS
                # ==================================================

                def load_transactions(self):

                    # Check whether transaction file exists
                    if not os.path.exists(
                            "transactions.txt"
                    ):
                        return

                    # Open transaction file
                    with open(
                            "transactions.txt",
                            "r"
                    ) as file:

                        # Read every line
                        for line in file:

                            # Remove spaces and \n
                            line = line.strip()

                            # Don't add empty lines
                            if line != "":
                                self.transactions.append(line)

    # LOAD TRANSACTIONS

    def load_transactions(self):

        # Check whether transaction file exists
        if not os.path.exists(
                "transactions.txt"
        ):
            return


        #open transaction file
        with open(
                "transactions.txt",
                "r"
        ) as file:

            # Read every line
            for line in file:

                # Remove spaces and \n
                line = line.strip()

                # Don't add empty lines
                if line != "":

                    self.transactions.append(line)



# MAIN PROGRAM

# Create Wallet object
wallet = Wallet()


# Keep showing menu until user chooses Exit
while True:

    print("\n")
    print("===================================")
    print("       DIGITAL WALLET SYSTEM")
    print("===================================")

    print("1. Create User")
    print("2. View All Users")
    print("3. View User")
    print("4. Deposit")
    print("5. Withdraw")
    print("6. Transfer")
    print("7. Payment")
    print("8. Transaction History")
    print("9. Exit")

    # Get menu choice
    choice = input(
        "Enter your choice: "
    )


    # Create user
    if choice == "1":

        wallet.create_user()


    # View all users
    elif choice == "2":

        wallet.view_users()


    # View one user
    elif choice == "3":

        wallet.view_user()


    # Deposit money
    elif choice == "4":

        wallet.deposit()


    # Withdraw money
    elif choice == "5":

        wallet.withdraw()


    # Transfer money
    elif choice == "6":

        wallet.transfer()


    # Make payment
    elif choice == "7":

        wallet.payment()


    # View transaction history
    elif choice == "8":

        wallet.transaction_history()


    # Exit program
    elif choice == "9":

        print(
            "Thank you for using Digital Wallet."
        )

        break


    # Invalid menu choice
    else:

        print("Invalid choice.")