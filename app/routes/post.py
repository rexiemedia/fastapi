from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

from typing import List
from starlette.responses import Response
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from .. database import get_db

router = APIRouter()
  
@router.get("/")
async def root():
    return {"message": "Hello World!!"}


# Using SqlAlchemy to perfom queries

@router.get("/sqlalchemy", response_model=List[schemas.Post])
async def get_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return  posts


# Create a post
@router.post("/sqlalchemy", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
# **post.dict() will unpack the model instead of doing post.title
   new_post =  models.Post(**post.dict())

   db.add(new_post)
   db.commit()
   db.refresh(new_post)
   return new_post

# Get one post with id
@router.get("/sqlalchemy/{id}", response_model=schemas.PostId)
def get_post(id: int, db: Session= Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} was not found")
    return post


# Delete a post
@router.delete("/sqlalchemy/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with the ID: {id} does not exist")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update a post
@router.put("/sqlalchemy/{id}", status_code=status.HTTP_201_CREATED)
def update_post(id: int, update_post: schemas.PostCreate,  db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with the ID: {id} does not exist")

    post_query.update(update_post.dict(), synchronize_session=False)
    
    db.commit()

    return post_query.first()
