# Import async SQLAlchemy tools
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession
)

from sqlalchemy.orm import (
    sessionmaker,
    declarative_base
)


# MySQL database connection
DATABASE_URL = (
    "mysql+asyncmy://root:password@localhost/digital_wallet_db"
)


# Create asynchronous database engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True
)


# Create asynchronous session
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# Base class for database models
Base = declarative_base()


# Database dependency
async def get_db():

    # Create async database session
    async with AsyncSessionLocal() as session:

        # Give session to FastAPI
        yield session