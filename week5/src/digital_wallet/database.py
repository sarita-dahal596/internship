from sqlalchemy import create_engine
# declarative_base = base class used for creating database models/tables
from sqlalchemy.orm import sessionmaker, declarative_base


# MySQL database connection
DATABASE_URL = (
    "mysql+pymysql://root:password@localhost/digital_wallet_db"
)


# Create connection between Python and MySQL
engine = create_engine(
    DATABASE_URL,
    echo=True
)


# Create database session
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,  # Do not automatically send changes before necessary
    autocommit=False  # We will manually use db.commit()
)


# Base class for database tables
Base = declarative_base()