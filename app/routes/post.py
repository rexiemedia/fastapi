from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.sql.functions import func
from starlette.responses import Response
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from .. database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# Using SqlAlchemy to perfom queries

@router.get("/", response_model=List[schemas.PostOut])
async def get_post(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    new_view = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return new_view


# Get one post with id
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session= Depends(get_db)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    new_view = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not new_view:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} was not found")
    return new_view 


# Create a post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

# **post.dict() will unpack the model instead of doing post.title
   new_post =  models.Post(user_id = user_id.id, **post.dict())

   db.add(new_post)
   db.commit()
   db.refresh(new_post)
   return new_post


# Delete a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user), super_user: str = Depends(oauth2.get_admin)):

    post_q = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_q.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with the ID: {id} does not exist")

    if post.user_id != int(user_id.id) and super_user.email != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Unathorized Operation")
    
    post_q.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update a post
@router.put("/{id}", status_code=status.HTTP_201_CREATED)
def update_post(id: int, update_post: schemas.PostCreate,  db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()


    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with the ID: {id} does not exist")

    if post.user_id != int(user_id.id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Unathorized Operation")
    
    post_query.update(update_post.dict(), synchronize_session=False)
    
    db.commit()

    return post_query.first()
