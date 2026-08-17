from fastapi import FastAPI, Response,status,HTTPException, Depends, APIRouter
from ..database import engine,get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import utils, models, schemas, auth2
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter( tags=['Auth'])

@router.post("/login")
def loginuser(usercreds : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db) ):
    user = db.query(models.User).filter(models.User.emailid == usercreds.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Please Enter Valid Email ID")

    if not utils.verify_password(usercreds.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                    detail="Invalid Credentials")

    token = auth2.create_access_token(data = { "userid" :user.userid, "name":user.username})
    return token
