import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

def _build_engine():
    return create_engine(DATABASE_URL, echo=False, future=True)


engine = _build_engine()
Base = declarative_base()
Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)