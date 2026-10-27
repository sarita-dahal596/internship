from database import SessionLocal


def get_db():

    # Create database session
    db = SessionLocal()

    try:
        # Give session to the API endpoint
        yield db

        # If everything completed successfully,
        # save ALL changes to MySQL
        db.commit()

    except Exception:

        # If any error occurs,
        # cancel all unsaved database changes
        db.rollback()

        # Send the error back so FastAPI
        # exception handlers can handle it
        raise

    finally:

        # Always close database session
        db.close()