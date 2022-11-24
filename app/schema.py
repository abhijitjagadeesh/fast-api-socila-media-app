from pydantic import BaseModel, EmailStr
from datetime import datetime

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

# Response schema
class Post(PostBase):
    id: int
    created_at: datetime
    # To help pydantic understand this is a orm model as it expects a dict
    class Config:
        orm_mode = True
        
class UserCreateResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    # To help pydantic understand this is a orm model as it expects a dict
    class Config:
        orm_mode = True