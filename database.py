from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Define the database URL
DATABASE_URL = "postgresql://postgres:omsabnis@localhost:5432/personalized_learning_path"

# Replace 'your_password' with the password you set for the 'postgres' user
# Replace 'your_database_name' with the name of the database you want to connect to
# (You might need to create this database in pgAdmin or using psql)

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a SessionLocal class to create database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define a base for declarative models
Base = declarative_base()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    # Example usage: Create the database if it doesn't exist (optional, and usually done via pgAdmin or psql)
    from sqlalchemy import text
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("Successfully connected to the database!")
    except Exception as e:
        print(f"Error connecting to the database: {e}")