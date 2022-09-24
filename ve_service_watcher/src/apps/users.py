from fastapi import APIRouter
from model import *

router = APIRouter()

@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}

@router.get("/users/us", tags=["users"])
async def read_user_me():
    return {"username": "LOOO"}

@router.post("/user/", response_model=User, tags=['users'])
async def create_user(user: User):
    return user
