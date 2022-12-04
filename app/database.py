from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
# from time import time
# from .routers import posts, users, auth
# import psycopg2
# from psycopg2.extras import RealDictCursor

# import app

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@localhost/{settings.database_name}"

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
        
        
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fast-api-project', user='postgres', password='Iaple312$', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print(f'Database connection was succesful')
#         break
#     except Exception as err:
#         print(f"Connection to database failed - {err}")
#         time.sleep(2)

# app.include_router(posts.router)
# app.include_router(users.router)
# app.include_router(auth.router)

