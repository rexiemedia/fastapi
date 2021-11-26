from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils
from . import outh2

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def loging(users_credential: OAuth2PasswordRequestForm = Depends(),  db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == users_credential.username).first()


    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credential")
    
    if not utils.authenticate(users_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credential")

    # create a token
    access_token = outh2.create_access_token(data = {"user_id": user.id})

    return {"token": access_token, "token_type": "bearer"}
    



