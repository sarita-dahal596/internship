# Import FastAPI
from fastapi import FastAPI
from pydantic import BaseModel

# Import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker


# Create FastAPI application
app = FastAPI()



# DATABASE CONNECTION


# MySQL database connection
DATABASE_URL = "mysql+pymysql://root:password@localhost/book_db"

# Create connection between Python and MySQL
engine = create_engine(DATABASE_URL)

# Create session
SessionLocal = sessionmaker(bind=engine)

# Base class for database tables
Base = declarative_base()


# BOOK TABLE


class BookDB(Base):

    # Table name in MySQL
    __tablename__ = "books"

    # Primary key
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    # Book title
    title = Column(
        String(100),
        nullable=False
    )

    # Author name
    author = Column(
        String(100),
        nullable=False
    )

    # Book price
    price = Column(
        Float,
        nullable=False
    )

    # Number of books
    quantity = Column(
        Integer,
        nullable=False
    )


# Create books table inside book_db
Base.metadata.create_all(bind=engine)

# PYDANTIC MODEL / SCHEMA


# This defines the data that the client must send
class Book(BaseModel):


    title: str

    author: str

    price: float

    quantity: int

# 1. GET - GET ALL BOOKS

@app.get("/books")
def get_books():

    # Open database session
    db = SessionLocal()

    try:

        # Get all records from books table
        books = db.query(BookDB).all()

        return books

    finally:

        # Close database session
        db.close()

# 2. GET - GET ONE BOOK BY ID



# GET /books/1
@app.get("/books/{book_id}")
def get_book(book_id: int):

    # Open database session
    db = SessionLocal()

    try:

        # Search book using its ID
        book = db.query(BookDB).filter(
            BookDB.id == book_id
        ).first()

        # Check if book exists
        if not book:

            # Return 404 if book is not found
            raise HTTPException(
                status_code=404,
                detail="Book not found"
            )

        # Return selected book
        return book

    finally:

        # Close database session
        db.close()

# 3. POST - ADD NEW BOOK

@app.post("/books")
def add_book(book: Book):

    # Open database session
    db = SessionLocal()

    try:

        # Create new BookDB object
        new_book = BookDB(
            title=book.title,
            author=book.author,
            price=book.price,
            quantity=book.quantity
        )

        # Add new book to database session
        db.add(new_book)

        # Save the new book permanently in MySQL
        db.commit()

        # Refresh object to get generated ID
        db.refresh(new_book)

        # Return success message
        return {
            "message": "Book added successfully",
            "book": new_book
        }

    finally:

        # Close database session
        db.close()

# 4. PUT - FULL UPDATE

# PUT is used to completely update a book
#  ex:PUT /books/1
@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):

    # Open database session
    db = SessionLocal()

    try:

        # Find existing book using ID
        existing_book = db.query(BookDB).filter(
            BookDB.id == book_id
        ).first()

        # Check whether book exists
        if not existing_book:

            # Return 404 if book does not exist
            raise HTTPException(
                status_code=404,
                detail="Book not found"
            )

        # Update ALL fields
        existing_book.title = book.title
        existing_book.author = book.author
        existing_book.price = book.price
        existing_book.quantity = book.quantity

        # Save changes permanently
        db.commit()

        # Refresh updated data
        db.refresh(existing_book)

        # Return updated book
        return {
            "message": "Book updated successfully",
            "book": existing_book
        }

    finally:

        # Close database session
        db.close()

# 5. PATCH - PARTIAL UPDATE


# PATCH is used to update only selected fields
# Ex:Only update price or quantity
@app.patch("/books/{book_id}")
def patch_book(book_id: int, data: dict):

    # Open database session
    db = SessionLocal()

    try:

        # Find book using ID
        book = db.query(BookDB).filter(
            BookDB.id == book_id
        ).first()

        # Check whether book exists
        if not book:

            # Return 404 error
            raise HTTPException(
                status_code=404,
                detail="Book not found"
            )

        # Loop through the fields sent by client
        for key, value in data.items():

            # Check whether that field exists in BookDB
            if hasattr(book, key):

                # Change the value
                setattr(book, key, value)

        # Save changes permanently
        db.commit()

        # Refresh updated book
        db.refresh(book)

        # Return updated book
        return {
            "message": "Book partially updated",
            "book": book
        }

    finally:

        # Close database session
        db.close()

# 6. DELETE - DELETE BOOK
# Ex:DELETE /books/1
@app.delete("/books/{book_id}")
def delete_book(book_id: int):

    # Open database session
    db = SessionLocal()

    try:

        # Search book using ID
        book = db.query(BookDB).filter(
            BookDB.id == book_id
        ).first()

        # Check whether book exists
        if not book:

            # Return 404 if book doesn't exist
            raise HTTPException(
                status_code=404,
                detail="Book not found"
            )

        # Delete book from database session
        db.delete(book)

        # Save deletion permanently in MySQL
        db.commit()

        # Return success message
        return {
            "message": "Book deleted successfully"
        }

    finally:

        # Close database session
        db.close()