from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
import os
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, oauth2
from ..import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
# Use public key file with os as secret

SECRET_KEY = "6$V4vyqIWQe!w7BEEds1t}wLDG5v!d0GDvQ?rGKIuvuPILrBRwLuf9#QAXHx19HGNx6bsmgS?zW5lJeTyIQ66ReYB!scZZZV1no?xuUm31}pATpBZfU5TSmf?zhZcBTz5HoBsaLqbGaiynNKqNrKW98Dkrq4PR3hlqRnFfhgLZ15NRiknwn12NXyCRKLp?x7j424Eo20asLV0BxOC!rFtJ7vlTiEP9cyrpoc}?XxsLx7NwWD3oYsv6O0c6zbhooU"

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expires = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expires})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return {"token", encoded_jwt}

def verify_access_token(token: str, credentila_exception):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        id: str = payload.get("users_id")

        if id is None:
            raise credentila_exception
        token_data = schemas.Tokenout(id=id)
    except JWTError:
        raise credentila_exception

def get_current_user(token: str = Depends()):
    verify_access_token()