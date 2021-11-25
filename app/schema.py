# importing basemodel to create a schema for incoming data
from pydantic import BaseModel
from typing import Optional
from pydantic.types import OptionalInt
from datetime import datetime

from sqlalchemy import orm

# Pydantic object schema defining the data to create a post
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

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