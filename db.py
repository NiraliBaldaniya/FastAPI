from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./urls.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

sessionlocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

base = declarative_base()