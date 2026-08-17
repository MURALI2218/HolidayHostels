from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, Double, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import Relationship


class Hostel(Base):
    __tablename__ = "hostels"

    hostelid = Column(Integer, primary_key = True, nullable = False)
    hostelname = Column(String, nullable = False)
    city = Column(String, nullable = False)
    urgentrecruitment = Column(Boolean, nullable = True)
    allowanceperday = Column(Double, nullable =True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    user_id = Column(ForeignKey('users.userid',ondelete='CASCADE'),nullable = False)
    owner = Relationship("User")

class User(Base):
    __tablename__ = "users"
    userid = Column(Integer, primary_key=True, nullable=False)
    username = Column(String,nullable=False)
    emailid = Column(String, unique=True,nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)


class Votes(Base):
    __tablename__ = "reviews"
    user_id = Column(Integer,ForeignKey('users.userid', ondelete='CASCADE'), primary_key=True)
    hostel_id = Column(Integer, ForeignKey('hostels.hostelid', ondelete='CASCADE'), nullable=False, primary_key=True)
    hostel_review = Column(String, nullable=True)

