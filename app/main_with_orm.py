from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine
from .routers import posts, users

# Creates the DB if it doesnt exists if it does then does nothing
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fast-api-project', user='postgres', password='Iaple312$', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print(f'Database connection was succesful')
        break
    except Exception as err:
        print(f"Connection to database failed - {err}")
        time.sleep(2)

app.include_router(posts.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"home": "Welcome to my Fast API project"}


