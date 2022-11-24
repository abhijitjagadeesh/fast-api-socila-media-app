from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schema
from ..database import get_db
from ..utils import hash

router = APIRouter()


@router.get('/users/{id}', response_model = schema.UserCreateResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user {id} not found')
    return user

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model = schema.UserCreateResponse)
def create_user(users: schema.UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash(users.password)
    users.password = hashed_password
    new_user = models.Users(**users.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user