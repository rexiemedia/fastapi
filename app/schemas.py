# importing basemodel to create a schema for incoming data
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from pydantic.types import conint

# Pydantic object schema defining the data to create a post
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    # created_by: str

# Inheriting Postbase properties
class PostCreate(PostBase):
    pass

# Return specific values including inherited from PostBase
class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Return specific values only
class PostId(BaseModel):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Users schema
class CreateUser(BaseModel):
    email: EmailStr
    password:  str
    firstname: str
    lastname: str

# Return specific values only
class UserOut(BaseModel):
    id: int
    email: str
    firstname: str
    lastname: str
    created_at: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

class Tokenout(BaseModel):
    id: Optional[str] = None
    