from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

db_url = "sqlite:///./urls.db"

engine = create_engine(
	db_url,
	connect_args={"check_same_thread": False}
)

sessionlocal = sessionmaker(
	bind=engine,
 	autoflush=False,
 	autocommit=False
)

base = declarative_base()
