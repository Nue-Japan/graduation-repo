from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Load database URL from environment variable or use default
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://myar_user:myar_password@localhost:5432/myar_db")

# WindowsにてSQLiteを使用する場合
# DATABASE_URL = "sqlite:///./sql_app.db"

# if DATABASE_URL.startswith("sqlite"):
#     engine = create_engine(
#         DATABASE_URL, connect_args={"check_same_thread": False}
#     )
# else:
#     engine = create_engine(DATABASE_URL)

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)

# Base class for declarative models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()