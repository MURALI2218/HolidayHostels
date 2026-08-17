from fastapi import FastAPI, Response,status,HTTPException, Depends, APIRouter
from ..database import engine,get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import utils, models, schemas,auth2
router = APIRouter( tags=['Users'])
 
@router.post("/createuser", status_code=status.HTTP_201_CREATED,response_model=schemas.user_Out )
def createuser(user:schemas.User_Creation, db:Session =Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    newuser = models.User(**user.model_dump())
    db.add(newuser)
    try:
        db.commit()
        db.refresh(newuser)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )

    return newuser

@router.get("/allusers", response_model=list[schemas.user_Out])
def users( db : Session = Depends(get_db)):
    all_users = db.query(models.User).all()
    return all_users

@router.get("/user/{id}/", response_model=schemas.user_Out)
def users(id:int, db : Session = Depends(get_db), current_user : dict= Depends(auth2.get_current_user)):
    user_detail= db.query(models.User).filter(models.User.userid == id).first()

    if user_detail is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"id: {id} is not available. Please enter a valid id"
            )
    return current_user