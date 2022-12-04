from fastapi import FastAPI
from . import models
from .database import engine
from .routers import posts, users, auth
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# Creates the DB if it doesnt exists if it does then does nothing
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"home": "Welcome to my Fast API project"}

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
