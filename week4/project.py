#1.Import libraries
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Numeric,
    func
)

from sqlalchemy.orm import (
    declarative_base,
    relationship,
    sessionmaker
)

from contextlib import contextmanager
from datetime import datetime
from decimal import Decimal

#2.Connect to MySQL
DATABASE_URL = "mysql+pymysql://root:password@localhost/financial_db"

engine = create_engine(
    DATABASE_URL,
    echo=False
)

Base = declarative_base()

# 3. CUSTOMER MODEL


class Customer(Base): #“Classes that inherit from base represent database tables.”

    __tablename__ = "customers"  #species the actual table name in mysql

    customer_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False
    )

    phone = Column(String(20))

    address = Column(String(200))

    # One customer can have many accounts
    accounts = relationship(
        "Account",
        back_populates="customer", #conect the relationship to account and account model
        cascade="all, delete-orphan"
    )


# 4. ACCOUNT MODEL


class Account(Base):

    __tablename__ = "accounts"

    account_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    account_number = Column(
        String(30),
        unique=True,
        nullable=False
    )

    account_type = Column(
        String(50),
        nullable=False
    )

    balance = Column(
        Numeric(12, 2),
        default=0
    )

    # Foreign key connecting account with customer
    customer_id = Column(
        Integer,
        ForeignKey("customers.customer_id"),
        nullable=False
    )

    # Relationship with Customer
    customer = relationship(
        "Customer",
        back_populates="accounts"
    )

    # One account can have many transactions
    transactions = relationship(
        "Transaction",
        back_populates="account",
        cascade="all, delete-orphan" #SQLAlchemy will delete that orphaned Account row from the database.
    )


# 5. CATEGORY MODEL


class Category(Base):

    __tablename__ = "categories"

    category_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    category_name = Column(
        String(100),
        unique=True,
        nullable=False
    )

    transactions = relationship(
        "Transaction",
        back_populates="category"
    )

# 6. TRANSACTION STATUS MODEL


class TransactionStatus(Base):

    __tablename__ = "transaction_statuses"

    status_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    status_name = Column(
        String(50),
        unique=True,
        nullable=False
    )

    transactions = relationship(
        "Transaction",
        back_populates="status"
    )


# 7. TRANSACTION MODEL


class Transaction(Base):

    __tablename__ = "transactions"

    transaction_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    account_id = Column(
        Integer,
        ForeignKey("accounts.account_id"),
        nullable=False
    )

    category_id = Column(
        Integer,
        ForeignKey("categories.category_id")
    )

    status_id = Column(
        Integer,
        ForeignKey("transaction_statuses.status_id")
    )

    transaction_type = Column(
        String(20),
        nullable=False
    )

    amount = Column(
        Numeric(12, 2),
        nullable=False
    )

    description = Column(
        String(200)
    )

    transaction_date = Column(
        DateTime,
        default=datetime.now
    )

    # Relationships
    account = relationship(
        "Account",
        back_populates="transactions"
    )

    category = relationship(
        "Category",
        back_populates="transactions"
    )

    status = relationship(
        "TransactionStatus",
        back_populates="transactions"
    )


# 8. CREATE TABLES


Base.metadata.create_all(engine)


# 9. CREATE SESSION


SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False
)

# 10. CONTEXT MANAGER FOR SESSION
#automatically manages  database session

@contextmanager
def get_session():

    session = SessionLocal()

    try:
        yield session  #Here is the session. Use it inside the with block.

        # Save changes
        session.commit()

    except Exception:
        # Undo changes if error occurs
        session.rollback()
        raise

    finally:
        # Always close the session
        session.close()

# 11. ADD CUSTOMER


def add_customer(name, email, phone, address):

    with get_session() as session:

        customer = Customer(
            name=name,
            email=email,
            phone=phone,
            address=address
        )

        session.add(customer)

        print("Customer added successfully.")


# 12. DISPLAY ALL CUSTOMERS


def display_customers():

    with get_session() as session:

        customers = session.query(Customer).all()

        print("\nCUSTOMERS")
        print("-" * 50)  #creates 50 dashes

        for customer in customers:

            print("ID:", customer.customer_id)
            print("Name:", customer.name)
            print("Email:", customer.email)
            print("Phone:", customer.phone)
            print("Address:", customer.address)

            print("-" * 50)  #creates 50 dashes



# 13. ADD ACCOUNT


def add_account(
    account_number,
    account_type,
    balance,
    customer_id
):

    with get_session() as session:

        customer = session.get(Customer, customer_id)

        if customer is None:
            print("Customer not found.")
            return

        account = Account(
            account_number=account_number,
            account_type=account_type,
            balance=Decimal(str(balance)),
            customer_id=customer_id
        )

        session.add(account)

        print("Account added successfully.")

# 14. DISPLAY ACCOUNTS


def display_accounts():

    with get_session() as session:

        accounts = session.query(Account).all()

        print("\nACCOUNTS")
        print("-" * 50)

        for account in accounts:

            print("Account ID:", account.account_id)

            print(
                "Account Number:",
                account.account_number
            )

            print(
                "Account Type:",
                account.account_type
            )

            print(
                "Balance:",
                account.balance
            )

            print(
                "Customer:",
                account.customer.name
            )

            print("-" * 50)


# 15. ADD CATEGORY


def add_category(category_name):

    with get_session() as session:

        category = Category(
            category_name=category_name
        )

        session.add(category)

        print("Category added successfully.")


# 16. ADD TRANSACTION STATUS


def add_status(status_name):

    # Remove extra spaces and make first letter capital
    status_name = status_name.strip().capitalize()

    with get_session() as session:

        # Check whether status already exists
        existing_status = (
            session.query(TransactionStatus)
            .filter_by(status_name=status_name)
            .first()
        )

        if existing_status:
            print("Status already exists.")
            return

        # Create new status
        status = TransactionStatus(
            status_name=status_name
        )

        session.add(status)

        print("Status added successfully.")

# 17. ADD TRANSACTION


def add_transaction(
    account_id,
    category_id,
    status_id,
    transaction_type,
    amount,
    description
):

    amount = Decimal(str(amount)) #converts that string into an exact decimal value

    with get_session() as session: #Open a database session

        account = session.get(  #Find the account
            Account,
            account_id
        )
        #Check whether the account exists
        if account is None:
            raise ValueError(
                "Account not found."
            )

        transaction_type = transaction_type.upper() #Convert transaction type to uppercase

        # Deposit
        if transaction_type == "DEPOSIT":

            account.balance += amount

        # Withdrawal
        elif transaction_type == "WITHDRAWAL":

            if account.balance < amount:

                raise ValueError(
                    "Insufficient balance."
                )

            account.balance -= amount  #Subtract the withdrawal

        else:

            raise ValueError(
                "Transaction type must be "
                "DEPOSIT or WITHDRAWAL."
            )
        #Create the transaction record
        transaction = Transaction(
            account_id=account_id,
            category_id=category_id,
            status_id=status_id,
            transaction_type=transaction_type,
            amount=amount,
            description=description
        )

        session.add(transaction) #Add transaction to the session

        print("Transaction completed successfully.")

        print(
            "New Balance:",
            account.balance
        )


# 18. DISPLAY ALL TRANSACTIONS


def display_transactions():

    with get_session() as session:  #Open a database session

  #retrieves every transaction from the database.
        transactions = (
            session.query(Transaction)
            .all()
        )

        print("\nTRANSACTIONS")
        print("-" * 60)

        for transaction in transactions:

            print(
                "Transaction ID:",
                transaction.transaction_id
            )

            print(
                "Account:",
                transaction.account.account_number
            )

            print(
                "Type:",
                transaction.transaction_type
            )

            print(
                "Amount:",
                transaction.amount
            )

            print(
                "Category:",
                transaction.category.category_name
            )

            print(
                "Status:",
                transaction.status.status_name
            )

            print(
                "Description:",
                transaction.description
            )

            print(
                "Date:",
                transaction.transaction_date
            )

            print("-" * 60)


# 19. FIND HIGH-VALUE TRANSACTIONS


def high_value_transactions(minimum_amount):

    with get_session() as session:  #Open the database session

        transactions = (
            session.query(Transaction)  #Query the Transaction table
            .filter(#Only get transactions where the amount is greater than the minimum amount.
                Transaction.amount >
                Decimal(str(minimum_amount))
            )
            .all()
        )

        print(
            "\nTransactions greater than",
            minimum_amount
        )

        for transaction in transactions:

            print(
                transaction.transaction_id,
                transaction.transaction_type,
                transaction.amount
            )



# 20. CUSTOMER + ACCOUNT JOIN


def customer_account_details():

    with get_session() as session:

        results = (
            session.query(
                Customer.name,
                Account.account_number,
                Account.account_type,
                Account.balance
            )
            .join(
                Account,
                Customer.customer_id ==
                Account.customer_id
            )
            .all()
        )

        print("\nCUSTOMER ACCOUNT DETAILS")

        for result in results:

            print(
                result.name,
                result.account_number,
                result.account_type,
                result.balance
            )


# 21. TOTAL TRANSACTION AMOUNT


def total_transaction_amount():

    with get_session() as session:

        total = (
            session.query(
                func.sum(Transaction.amount)
            )
            .scalar()
        )

        print(
            "Total Transaction Amount:",
            total
        )


# 22. TOTAL AMOUNT BY CATEGORY


def transaction_by_category():

    with get_session() as session:  #Open database session
        #Start the query
        results = (
            session.query(
                Category.category_name,  #select the category name
                func.sum(  #adds multiple transaction amounts together.
                    Transaction.amount
                ).label("total")  #gives the calculated column a name.
            )
            .join(
                Transaction,
                Category.category_id ==  #Connect a category with transactions that have the same category ID.
                Transaction.category_id
            )
            #puts rows having the same category together.
            .group_by(
                Category.category_id,
                Category.category_name
            )
            .all()
        )

        print("\nTRANSACTION BY CATEGORY")

        for category, total in results:

            print(
                category,
                "->",
                total
            )

# 23. TRANSACTION COUNT PER CUSTOMER


def transaction_count_per_customer():

    with get_session() as session:

        results = (
            session.query(
                Customer.name,
                func.count( #counts how many transaction records belong to each customer
                    Transaction.transaction_id
                ).label("transaction_count") #gives the calculated column a name
            )#connects the Customer table with the Account table.
            .join(
                Account,
                Customer.customer_id ==
                Account.customer_id
            )
            .join( #connect each account to its transactions.
                Transaction,
                Account.account_id ==
                Transaction.account_id
            )
            .group_by( #puts all records belonging to the same customer into one group
                Customer.customer_id,
                Customer.name
            )
            .all() #executes the query and retrieves all results.
        )

        print("\nTRANSACTIONS PER CUSTOMER")

        for name, count in results:

            print(
                name,
                "->",
                count,
                "transactions"
            )



# 24. MAIN PROGRAM

# ============================================================
# MAIN PROGRAM - TERMINAL MENU
# ============================================================

if __name__ == "__main__":

    while True:

        print("\n" + "=" * 50)
        print("FINANCIAL TRANSACTION DATABASE SYSTEM")
        print("=" * 50)

        print("1. Add Customer")
        print("2. Display Customers")
        print("3. Add Account")
        print("4. Display Accounts")
        print("5. Add Category")
        print("6. Add Transaction Status")
        print("7. Add Transaction")
        print("8. Display Transactions")
        print("9. Find High Value Transactions")
        print("10. Customer Account Details")
        print("11. Total Transaction Amount")
        print("12. Transaction Amount by Category")
        print("13. Transaction Count per Customer")
        print("0. Exit")

        print("=" * 50)

        choice = input("Enter your choice: ")


        # ----------------------------------------------------
        # 1. ADD CUSTOMER
        # ----------------------------------------------------

        if choice == "1":

            print("\n--- ADD CUSTOMER ---")

            name = input("Enter customer name: ")
            email = input("Enter email: ")
            phone = input("Enter phone: ")
            address = input("Enter address: ")

            add_customer(
                name,
                email,
                phone,
                address
            )


        # ----------------------------------------------------
        # 2. DISPLAY CUSTOMERS
        # ----------------------------------------------------

        elif choice == "2":

            display_customers()


        # ----------------------------------------------------
        # 3. ADD ACCOUNT
        # ----------------------------------------------------

        elif choice == "3":

            print("\n--- ADD ACCOUNT ---")

            account_number = input(
                "Enter account number: "
            )

            account_type = input(
                "Enter account type (Savings/Current): "
            )

            balance = input(
                "Enter opening balance: "
            )

            customer_id = int(
                input("Enter customer ID: ")
            )

            add_account(
                account_number,
                account_type,
                balance,
                customer_id
            )


        # ----------------------------------------------------
        # 4. DISPLAY ACCOUNTS
        # ----------------------------------------------------

        elif choice == "4":

            display_accounts()


        # ----------------------------------------------------
        # 5. ADD CATEGORY
        # ----------------------------------------------------

        elif choice == "5":

            print("\n--- ADD CATEGORY ---")

            category_name = input(
                "Enter category name: "
            )

            add_category(category_name)


        # ----------------------------------------------------
        # 6. ADD TRANSACTION STATUS
        # ----------------------------------------------------

        elif choice == "6":

            print("\n--- ADD TRANSACTION STATUS ---")

            status_name = input(
                "Enter status (Completed/Pending/Failed): "
            )

            add_status(status_name)


        # ----------------------------------------------------
        # 7. ADD TRANSACTION
        # ----------------------------------------------------

        elif choice == "7":

            print("\n--- ADD TRANSACTION ---")

            account_id = int(
                input("Enter account ID: ")
            )

            category_id = int(
                input("Enter category ID: ")
            )

            status_id = int(
                input("Enter status ID: ")
            )

            transaction_type = input(
                "Enter transaction type "
                "(DEPOSIT/WITHDRAWAL): "
            )

            amount = input(
                "Enter amount: "
            )

            description = input(
                "Enter description: "
            )

            try:

                add_transaction(
                    account_id,
                    category_id,
                    status_id,
                    transaction_type,
                    amount,
                    description
                )

            except ValueError as error:

                print("Error:", error)


        # ----------------------------------------------------
        # 8. DISPLAY TRANSACTIONS
        # ----------------------------------------------------

        elif choice == "8":

            display_transactions()


        # ----------------------------------------------------
        # 9. HIGH VALUE TRANSACTIONS
        # ----------------------------------------------------

        elif choice == "9":

            minimum_amount = input(
                "Enter minimum amount: "
            )

            high_value_transactions(
                minimum_amount
            )


        # ----------------------------------------------------
        # 10. CUSTOMER ACCOUNT DETAILS
        # ----------------------------------------------------

        elif choice == "10":

            customer_account_details()


        # ----------------------------------------------------
        # 11. TOTAL TRANSACTION AMOUNT
        # ----------------------------------------------------

        elif choice == "11":

            total_transaction_amount()


        # ----------------------------------------------------
        # 12. TRANSACTION BY CATEGORY
        # ----------------------------------------------------

        elif choice == "12":

            transaction_by_category()


        # ----------------------------------------------------
        # 13. TRANSACTION COUNT PER CUSTOMER
        # ----------------------------------------------------

        elif choice == "13":

            transaction_count_per_customer()


        # ----------------------------------------------------
        # 0. EXIT
        # ----------------------------------------------------

        elif choice == "0":

            print("\nThank you for using the system.")
            print("Program closed.")

            break


        # ----------------------------------------------------
        # INVALID CHOICE
        # ----------------------------------------------------

        else:

            print("\nInvalid choice.")
            print("Please enter a number from the menu.")