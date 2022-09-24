from fastapi import APIRouter, status
from model import *


router = APIRouter()


#method=GET
@router.get("/root", tags=["appone"])
async def root():
    return {"Hello world!"}


