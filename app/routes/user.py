from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
from starlette.responses import Response
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from .. database import get_db



router = APIRouter(
    prefix="/users",
    # to group endpoints together in the Swagger UI at http://127.0.0.1:8000/docs
    tags=['Users']
)


# Users routes starts here

# Create a User
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
   
   hash_password = utils.hash(user.password)
   user.password = hash_password

   new_user =  models.User(**user.dict())
   
   db.add(new_user)
   db.commit()
   db.refresh(new_user)

   return new_user


# Get all users
@router.get("/", response_model=List[schemas.UserOut])
async def get_user(db: Session = Depends(get_db), user_role: str = Depends(oauth2.get_admin)):
    users = db.query(models.User).all()

    if user_role.isAdmin != True :
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Unauthorized Operation Activity will be logged to administratior!")
    

    return  users

# Get one user
@router.get("/{id}", response_model=schemas.UserOut)
async def get_user(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), admin_user: str = Depends(oauth2.get_admin)):
    user_querry = db.query(models.User).filter(models.User.id == id)

    user = user_querry.first()


    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist!")

    if user.id != int(current_user.id) and admin_user.isAdmin != True:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Unauthorized Operation Activity will be logged to administratior!")
    
    return  user

# delete a user
# Delete a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), admin_user: str = Depends(oauth2.get_admin), current_user: int = Depends(oauth2.get_current_user)):

    user_querry = db.query(models.User).filter(models.User.id == id)

    user = user_querry.first()

    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with the ID: {id} does not exist")

    if user.id != int(current_user.id) and admin_user.isAdmin != True:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Unauthorized Operation Activity will be logged to administratior!")

    user_querry.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Updating a user
@router.put("/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def update_user(id: int, update_post: schemas.CreateUser,  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), admin_user: str = Depends(oauth2.get_admin)):

    user_query = db.query(models.User).filter(models.User.id == id)

    user = user_query.first()

    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with the ID: {id} does not exist")

    if user.id != int(current_user.id) and admin_user.isAdmin != True:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Unauthorized Operation Activity will be logged to administratior!")

    hash_password = utils.hash(user.password)
    user.password = hash_password
    user_query.update(update_post.dict(), synchronize_session=False)
    
    db.commit()

    return user_query.first()
# SqlAlchemy ends here

