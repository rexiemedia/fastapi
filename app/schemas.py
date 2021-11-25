# importing basemodel to create a schema for incoming data
from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic.types import OptionalInt
from datetime import datetime

from app.models import User

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
    class Config:
        orm_mode = True