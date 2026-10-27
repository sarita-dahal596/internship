
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# MySQL database connection
DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/week7_banking_db"

# Create database engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# Create database session
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

# Base class for SQLAlchemy models
Base = declarative_base()


# Open and close database session
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
