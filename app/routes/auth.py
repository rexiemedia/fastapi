from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import schemas, database, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
def login(users_credentials: OAuth2PasswordRequestForm = Depends(),  db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == users_credentials.username).first()


    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credential")
    
    if not utils.authenticate(users_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credential")

    # create a token
    access_token = oauth2.create_access_token(data = {"user_id": user.id, "user_email": user.email})

    return {"access_token": access_token, "token_type": "bearer"}
    



