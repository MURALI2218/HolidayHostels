from fastapi import status,HTTPException, Depends, APIRouter
from ..database import engine,get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import models, schemas, auth2

from typing import List,Optional
from sqlalchemy import func

router = APIRouter(tags= ['Hostels'])


@router.get("/hostels", response_model=List[schemas.Hostels_Retrival])
async def all_hostels(db : Session = Depends(get_db),
                       limit: int = 10, skip  : int = 0, search :Optional[str] = ""
                       ):
      
   hostels_list = db.query(models.Hostel).filter(models.Hostel.hostelname.contains(search)).limit(limit).offset(skip).all()
   hostel_with_reviews = db.query(models.Hostel,  func.count(models.Votes.hostel_id).
                                  label("Reviews")).join(models.Votes, models.Votes.hostel_id== models.Hostel.hostelid, isouter=True).group_by(models.Hostel.hostelid).filter(models.Hostel.hostelname.contains(search)).limit(limit).offset(skip).all()
   
   result = []

   for hostel, reviews in hostel_with_reviews:
    result.append({
        "city" : hostel.city,
        "hostelname" : hostel.hostelname,
        "hostelid": hostel.hostelid,
        "created_at": hostel.created_at,
        "allowanceperday":hostel.allowanceperday,
        "urgentrecruitment":hostel.urgentrecruitment,
        "Reviews": reviews,
         "owner": hostel.owner
    })
   
   return  result

@router.get("/hostel_data/{id}", response_model=schemas.Hostels_Retrival)
async def single_hostel(id: int,db : Session = Depends(get_db)):
    hostel_data = db.query(models.Hostel).filter(models.Hostel.hostelid == id).first()
    if hostel_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"id: {id} is not available. Please enter a valid id"
            )

    else:
        return hostel_data
# def single_hostel(id:int):
#     cursor.execute("""SELECT * FROM hostels WHERE hostel_id = %s""", (str(id),))
#     hostel_data = cursor.fetchone()
#     if hostel_data:
#         return {"Hostel": hostel_data}

#     else :
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                 detail= f"hostel is not avail with id {id} please enter valid id")
        

 # cursor.execute("""INSERT INTO hostels (name, city, allowanceperday, urgentrecruitment)VALUES(%s,%s,%s,%s) RETURNING *""",
    #                (hostel.name, hostel.city, hostel.allowanceperday, hostel.urgentrecruitment))
    # hostel_dict = cursor.fetchone()
    # conn.commit()
@router.post("/createhostel",status_code=status.HTTP_201_CREATED, response_model=schemas.Hostels_Retrival)
async def new_hostels(hostel :schemas.Hostel_Create, db : Session = Depends(get_db), 
                      current_user : int = Depends(auth2.get_current_user)):
    
    new_hostel = models.Hostel( user_id = current_user.userid , **hostel.dict())
    db.add(new_hostel)
    db.commit()
    db.refresh(new_hostel)

    return new_hostel

@router.delete("/deletehostel/{id}/",status_code=status.HTTP_204_NO_CONTENT)
def deletehostel(id: int, db:Session= Depends(get_db),
                 current_user : int = Depends(auth2.get_current_user)):
    hostel_data = db.query(models.Hostel).filter(models.Hostel.hostelid == id)
    if hostel_data.first() is None:
        raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"id: {id} is not available. Please enter a valid id")
        # return {"Respect" :f"id: {id} is not available. Please enter a valid id" }
        
        
    hostel_data.delete(synchronize_session = False)
    db.commit()
    return hostel_data
    # cursor.execute("""DELETE FROM hostels WHERE hostel_id = %s RETURNING *""",(str(id),))
    # hostel_data = cursor.fetchone()
    # if hostel_data:
    #     conn.commit()
    #     return {"HOSTEL Delete Successful" : hostel_data}
    # else:
    #     raise HTTPException(
    #     status_code=status.HTTP_404_NOT_FOUND,
    #     detail=f"id: {id} is not available. Please enter a valid id")

@router.put("/updatehostel/{id}/")
async def update_hostel(id: int, updated_hostel:schemas.Hostel_Create,db : Session = Depends(get_db),
                        current_user : int = Depends(auth2.get_current_user)):
    hostel_data = db.query(models.Hostel).filter(models.Hostel.hostelid == id)
    hostel = hostel_data.first()
    if hostel is None:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"id: {id} is not available. Please enter a valid id"
            )

    else:
        hostel_data.update(updated_hostel.dict(), synchronize_session = False)
        db.commit()
        return hostel_data.first()

    # cursor.execute("""UPDATE hostels SET name =%s, city = %s, allowanceperday = %s , urgentrecruitment = %s  WHERE hostel_id = %s    RETURNING * """,
    #                    (hostel.name, hostel.city, hostel.allowanceperday, hostel.urgentrecruitment,str(id),) )
    # hostel_dict = cursor.fetchone()
    
    
    # if hostel_dict:
            
    #         conn.commit()
    #         return {"Update Successful": hostel_dict}
    # else:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"id: {id} is not available. Please enter a valid id"
    #         )
   