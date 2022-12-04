from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, schema, oauth2
from ..database import get_db
from ..utils import hash, verify

router = APIRouter(prefix="/login", tags=["Authentication"])

@router.post("/", response_model=schema.Token)
def login_user(login: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_credentials = db.query(models.Users).filter(models.Users.email == login.username).first()
    if user_credentials is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid credentials')
    
    if not verify(login.password, user_credentials.password):
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid credentials')
     
    access_token = oauth2.create_access_token(data= {"user_id": user_credentials.id})     
    return {'access_token': access_token, "token_type": "bearer"}