import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import status, Depends, HTTPException
from datetime import datetime, timedelta, timezone
from . import schemas, models,config
from sqlalchemy.orm import Session
from .database import get_db
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# Sceret_key 
#Algorithm
#expreationtime

SECRET_KEY = config.settings.secret_key 
ALGORITHM = config.settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = config.settings.access_token_expire_minutes


def create_access_token(data : dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta

    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM )

    return { 'access_token' : encoded_jwt, "token_type" : "bearer"} 


def verify_access_token(token :str , credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        
        id: int = payload.get("userid")
        
        if id is None:
            raise credentials_exception

        token_data = schemas.Tokendata(id = id)
        
    except InvalidTokenError:
        raise credentials_exception

    return token_data

oauth2_scheme  = OAuth2PasswordBearer(tokenUrl= 'login')
def get_current_user(token : str = Depends(oauth2_scheme),db:Session =  Depends(get_db) ):
    credentials_exception =HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                         detail=f"Could Not Validate Credentials", headers={'WWW-Authenticate': "Bearer"})
    token = verify_access_token(token, credentials_exception)
   
    user_detail = db.query(models.User).filter(models.User.userid == token.id).first()

    
    return user_detail
    
    