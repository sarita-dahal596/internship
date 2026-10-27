
from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    BackgroundTasks,
    Request
)

from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from week7_project.database import (
    engine,
    Base,
    get_db
)

from week7_project.models import (
    User,
    Account,
    Transaction,
    Merchant
)

from week7_project.schemas import (
    RegisterRequest,
    LoginRequest,
    AccountRequest,
    MoneyRequest,
    TransferRequest,
    PaymentRequest,
    MerchantRequest
)

from week7_project.auth import (
    hash_password,
    verify_password,
    create_token
)

from week7_project.dependencies import (
    get_current_user,
    admin_required
)

from week7_project.services import (
    deposit,
    withdraw,
    transfer,
    payment
)


# Create database tables if they do not exist
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Secure Banking API",
    description="Week 7 Secure Banking REST API",
    version="1.0"
)


# Allow requests from the configured frontend origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:4200"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Log incoming requests and outgoing response status
@app.middleware("http")
async def logging_middleware(
    request: Request,
    call_next
):
    print(
        "Request:",
        request.method,
        request.url.path
    )

    response = await call_next(request)

    print(
        "Response:",
        response.status_code
    )

    return response


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "Secure Banking API is running"
    }


# Register a new user
@app.post("/users", tags=["Users"])
def create_user(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.username == data.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    existing_email = db.query(User).filter(
        User.email == data.email
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    # Hash password before storing it
    new_user = User(
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password),
        role="user"
    )

    db.add(new_user)

    try:
        db.commit()

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Username or email already exists"
        )

    db.refresh(new_user)

    return {
        "message": "User created successfully",
        "user_id": new_user.user_id,
        "username": new_user.username,
        "role": new_user.role
    }


# Login and generate a PASETO token
@app.post("/login", tags=["Authentication"])
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.username == data.username
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    # Compare entered password with stored password hash
    if not verify_password(
        data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = create_token(
        user.user_id,
        user.username,
        user.role
    )

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "Bearer"
    }


# Get the logged-in user's profile
@app.get("/users/me", tags=["Users"])
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return {
        "user_id": current_user.user_id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role
    }


# List all users; admin access only
@app.get("/users", tags=["Users"])
def get_users(
    current_user: User = Depends(admin_required),
    db: Session = Depends(get_db)
):
    users = db.query(User).all()

    return [
        {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
        for user in users
    ]


# Create a bank account for the logged-in user
@app.post("/accounts", tags=["Accounts"])
def create_account(
    data: AccountRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing_account = db.query(Account).filter(
        Account.account_number == data.account_number
    ).first()

    if existing_account:
        raise HTTPException(
            status_code=400,
            detail="Account number already exists"
        )

    account = Account(
        user_id=current_user.user_id,
        account_number=data.account_number,
        balance=0
    )

    db.add(account)

    try:
        db.commit()

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Account number already exists"
        )

    db.refresh(account)

    return {
        "message": "Account created successfully",
        "account_id": account.account_id,
        "account_number": account.account_number,
        "balance": account.balance
    }


# Check the balance of an account owned by the user
@app.get("/balance/{account_id}", tags=["Accounts"])
def get_balance(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    account = db.query(Account).filter(
        Account.account_id == account_id,
        Account.user_id == current_user.user_id
    ).first()

    if account is None:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )

    return {
        "account_id": account.account_id,
        "account_number": account.account_number,
        "balance": account.balance
    }


# Deposit money into the user's account
@app.post("/deposit", tags=["Transactions"])
def deposit_money(
    data: MoneyRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    account, error = deposit(
        db,
        current_user,
        data.account_id,
        data.amount
    )

    if error:
        raise HTTPException(
            status_code=400,
            detail=error
        )

    return {
        "message": "Deposit successful",
        "account_id": account.account_id,
        "balance": account.balance
    }


# Withdraw money if the account has sufficient funds
@app.post("/withdraw", tags=["Transactions"])
def withdraw_money(
    data: MoneyRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    account, error = withdraw(
        db,
        current_user,
        data.account_id,
        data.amount
    )

    if error:
        raise HTTPException(
            status_code=400,
            detail=error
        )

    return {
        "message": "Withdrawal successful",
        "account_id": account.account_id,
        "balance": account.balance
    }


# Transfer money from the user's account to another account
@app.post("/transfer", tags=["Transactions"])
def transfer_money(
    data: TransferRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    account, error = transfer(
        db,
        current_user,
        data.from_account_id,
        data.to_account_id,
        data.amount
    )

    if error:
        raise HTTPException(
            status_code=400,
            detail=error
        )

    return {
        "message": "Transfer successful",
        "account_id": account.account_id,
        "balance": account.balance
    }





# Get the user's transaction history with optional filtering
@app.get("/transactions", tags=["Transactions"])
def get_transactions(
    transaction_type: str | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Transaction).filter(
        Transaction.user_id == current_user.user_id
    )

    if transaction_type:
        query = query.filter(
            Transaction.transaction_type ==
            transaction_type.upper()
        )

    transactions = query.order_by(
        Transaction.transaction_id.desc()
    ).all()

    return [
        {
            "transaction_id": transaction.transaction_id,
            "account_id": transaction.account_id,
            "transaction_type": transaction.transaction_type,
            "amount": transaction.amount,
            "from_account": transaction.from_account,
            "to_account": transaction.to_account,
            "status": transaction.status,
            "created_at": transaction.created_at
        }
        for transaction in transactions
    ]

# Make a payment to a merchant
@app.post("/payment", tags=["Transactions"])
def make_payment(
    data: PaymentRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    account, error = payment(
        db,
        current_user,
        data.user_id,
        data.merchant,
        data.amount
    )

    if error:
        raise HTTPException(
            status_code=400,
            detail=error
        )

    background_tasks.add_task(
        print,
        f"Payment of {data.amount} completed to {data.merchant}"
    )

    return {
        "message": "Payment successful",
        "user_id": data.user_id,
        "merchant": data.merchant,
        "amount": data.amount,
        "remaining_balance": account.balance
    }
