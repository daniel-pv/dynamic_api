from fastapi import APIRouter, status
from model import *


router = APIRouter()


#method=GET
@router.get("//two", tags=["apptwo"])
async def get_two():
    return {"Hello world!"}


