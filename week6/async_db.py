from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


# MySQL database connection
DATABASE_URL = "mysql+asyncmy://root:password@localhost/digital_wallet_db"


# Create asynchronous engine
engine = create_async_engine(
    DATABASE_URL,

    # Show SQL queries in the terminal
    echo=True
)


# Create asynchronous session
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# Database dependency
async def get_db():

    async with AsyncSessionLocal() as session:
        yield session