from fastapi import (
    APIRouter,  # separates routes from main.py
    Depends,  # dependency injection
    BackgroundTasks,  # = run work after response
    status  # = HTTP status code constants
)

# Database session type
from sqlalchemy.orm import Session

# Database dependency
from dependencies import get_db

# Pydantic request schema
from schemas import UserCreate

from models import User

# Database model
from services import (
    create_user,
    find_user
)

# Business logic
from background_tasks import (
    transaction_notification
)

# CREATE ROUTER
router = APIRouter(
    prefix="/users",  # All routes in this file begin with /users

    # Swagger heading
    tags=["Users"]

)


# Create user
@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
def add_user(
        # Request body is checked using UserCreate
        data: UserCreate,
        # FastAPI background task manager
        background_tasks: BackgroundTasks,

        # Automatically get database session
        db: Session = Depends(get_db)
):
    # Call service function to create user
    user = create_user(
        db,
        data.name,
        data.email,
        data.tier
    )
    # Run notification after response
    background_tasks.add_task(
        transaction_notification,
        f"User {user.user_id} created"
    )
    # Response returned to client
    return {
        "message": "User created successfully",
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email,
        "tier": user.tier,
        "balance": user.balance
    }


# Get all users
@router.get("")
def get_users(
        # Get database session automatically
        db: Session = Depends(get_db)
):
    # SELECT all users
    return db.query(User).all()


# Get one user
@router.get("/{user_id}")
def get_user(
        user_id: int,
        db: Session = Depends(get_db)
):
    return find_user(
        db,
        user_id
    )


# Check balance
@router.get("/{user_id}/balance")
def check_balance(
        user_id: int,
        db: Session = Depends(get_db)
):
    # Find requested user
    user = find_user(
        db,
        user_id
    )
    # Return only important balance information
    return {
        "user_id": user.user_id,
        "name": user.name,
        "balance": user.balance
    }
