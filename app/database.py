from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Iaple312$@localhost/fast-api-project"

# An engine is responsible for sqlalchemy to connect to a db
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#  A session is created to talk to database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency used to connect to db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
