from pydantic import BaseModel,ConfigDict, EmailStr
from typing import Optional
from datetime import datetime
from pydantic.types import conint


class HostelsBase(BaseModel):
    hostelname : str
    city : str
    allowanceperday : float
    urgentrecruitment : bool
    
    # district : str
    # pincode : int
    # state : str
    # contactnumber : int
    # englishprofeciency : Optional[int] = None

class user_Out(BaseModel):
    userid : int
    username : str 
    emailid : EmailStr
    
    model_config = ConfigDict(from_attributes=True)


class Hostel_Create(HostelsBase):
    pass 

class Hostels_Retrival(BaseModel):
    hostelid : int
    created_at : datetime
    hostelname : str
    city : str
    owner : user_Out
    Reviews : Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)

class User_Creation(BaseModel):
    username : str 
    emailid : EmailStr
    password : str



class usercredentials(BaseModel):
    emailid : str
    password : str


class Token(BaseModel):
    access_token: str
    token_type : str

class Tokendata(BaseModel):
    id : Optional[int] = None

class Vote(BaseModel):
    hostel_id : int
    review : Optional[str] = "Good Hostel"
    dir : conint(strict= True,le=1) # type: ignore 