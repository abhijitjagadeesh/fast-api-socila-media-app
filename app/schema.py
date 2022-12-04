from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Request schema
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserBase(BaseModel):
    email: EmailStr
    password: str
    
class UserCreate(UserBase):
    pass

class LoginUser(UserBase):
    pass 

# Response schema
class UserCreateResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    # To help pydantic understand this is a orm model as it expects a dict
    class Config:
        orm_mode = True

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserCreateResponse
    # To help pydantic understand this is a orm model as it expects a dict
    class Config:
        orm_mode = True
        
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str]