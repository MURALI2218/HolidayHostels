from .. import models, database, auth2, schemas
from fastapi import FastAPI, Depends , APIRouter, status, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix ='/votes',tags= ['Vote'])


@router.post('/', status_code=status.HTTP_201_CREATED)
def Review_system(vote : schemas.Vote, db : Session = Depends(database.get_db), current_user : int = Depends(auth2.get_current_user)):
    
    vote_query =db.query(models.Votes).filter(
                models.Votes.hostel_id == vote.hostel_id, models.Votes.user_id == current_user.userid)
    
    vote_found = vote_query.first()
   
    
    if (vote.dir == 1):
        if vote_found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{current_user.userid, current_user.username} : You Already Reviwed the Hostel : {vote.hostel_id}")

        new_vote = models.Votes(hostel_id = vote.hostel_id, user_id = current_user.userid, hostel_review = vote.review)
        db.add(new_vote)
        db.commit()
        return {'messege' : " Review Successful"}

    else:
        if not vote_found and vote.dir != 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Please Enter Valid HOSTEL ID!!!")
        else:
            if not vote_found and vote.dir == 0 :
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Please Review the hostel First")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {'message': "Reveiew Deleted !!!"}