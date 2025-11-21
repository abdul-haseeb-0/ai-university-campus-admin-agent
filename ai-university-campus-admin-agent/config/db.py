from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()  # Load environment variables from a .env file
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Test database connection
if __name__ == "__main__":
    try:
        with engine.connect() as connection:
            print("Database connection successful.")
    except Exception as e:
        print(f"Database connection failed: {e}")

    print("Creating tables...")
    Base.metadata.create_all(engine)
    print("Tables created.")
  