from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

from pathlib import Path


# ---------------------------------------
# Database Location
# ---------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = BASE_DIR / "enterprise_rag.db"

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"


# ---------------------------------------
# SQLAlchemy Engine
# ---------------------------------------

engine = create_engine(

    DATABASE_URL,

    connect_args={
        "check_same_thread": False
    }

)


# ---------------------------------------
# Session Factory
# ---------------------------------------

SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine

)


# ---------------------------------------
# Base Model
# ---------------------------------------

Base = declarative_base()


# ---------------------------------------
# Dependency
# ---------------------------------------

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()