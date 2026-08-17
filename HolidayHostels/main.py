from fastapi import FastAPI
from . import models
from .database import engine
from .routers import hostels, users, auth, reviews
# models.Base.metadata.create_all(bind = engine)
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins ,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(hostels.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(reviews.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
 
   